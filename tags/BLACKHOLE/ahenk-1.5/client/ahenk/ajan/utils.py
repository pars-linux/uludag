#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import ldap
import ldif
import logging
import os
import StringIO
import time


def getText(label):
    """
        Prompts user for input.

        Args:
            label: Label for prompt.

        Returns:
            None on keyboard interrupt, else user input.
    """
    try:
        return raw_input("%s > " % label)
    except KeyboardInterrupt:
        return None

def getLDIF(value):
    """
        Converts a policy object to LDIF string.

        Args:
            value: Policy setting object
        Returns:
            LDIF string
    """
    output = StringIO.StringIO()
    writer = ldif.LDIFWriter(output)
    writer.unparse(value[0], value[1])
    text = output.getvalue()
    output.close()
    return text

def parseLDIF(_file):
    """
        Reads an LDIF file and converts it to a policy object.

        Args:
            _file: LDIF filename
        Returns:
            Policy object
    """
    class MyLDIF(ldif.LDIFParser):
       def handle(self, dn, entry):
            if self.comp:
                self.ou.append(entry)
            else:
                self.comp = entry

    parser = MyLDIF(_file)
    parser.comp = None
    parser.ou = []
    parser.parse()
    return parser.comp

def getStrHash(data):
    """
        Returns SHA1 hash of a text.

        Args:
            data: Text
        Returns:
            SHA1 sum
    """
    return hashlib.sha1(data).hexdigest()

def getFileHash(filename):
    """
        Returns SHA1 hash of a file.

        Args:
            filename: Filename
        Returns:
            SHA1 sum
    """
    if not os.path.exists(filename):
        return ""
    return hashlib.sha1(file(filename).read()).hexdigest()


class Task:
    """
        Class for a single job in task manager.

        Properties:
            callable: Function or method to be called.
            interval: Call interval in seconds.
            last: Last execution time
    """

    def __init__(self, callable, interval):
        """
            Inits Task class with callable and call interval.

            Args:
                callable: Function or method to be called.
                interval: Call interval in seconds.
        """
        self.callable = callable
        self.interval = interval
        self.last = time.time()

    def update(self, callable, interval):
        """
            Updates callable and call interval.
        """
        self.callable = callable
        self.interval = interval

    def isReady(self):
        """
            Returns if it's time to call method.
        """
        if (time.time() - self.last) > self.interval:
            return True
        return False

    def run(self):
        """
            Calls method and resets it's time.
        """
        self.last = time.time()
        self.callable()


class TaskManager:
    """
        Poor man's scheduled job manager.
    """

    def __init__(self):
        """
            Inits task manager.
        """
        self.tasks = {}

    def update(self, filename, timers):
        """
            Updates a Ahenk module's scheduled tasks without touching last execution times.

            Args:
                filename: Module filename
                timers: Timers object returned by Ahenk module.
        """
        if filename not in self.tasks:
            self.tasks[filename] = {}
        tasks = []
        # Check for new/updated tasks
        for name, (callable, interval) in timers.iteritems():
            if name in self.tasks[filename]:
                self.tasks[filename][name].update(callable, interval)
            else:
                self.tasks[filename][name] = Task(callable, interval)
            tasks.append(name)
        # Remove old tasks
        for name in set(self.tasks[filename].keys()) - set(tasks):
            del self.tasks[filename][name]

    def delete(self, filename):
        """
            Removes an Ahenk module from task manager.

            Args:
                filename: Module filename
        """
        del self.tasks[filename]

    def fire(self):
        """
            Executes tasks that are ready to run.
        """
        for filename in self.tasks:
            for name, task in self.tasks[filename].iteritems():
                if task.isReady():
                    task.run()


class Mod:
    """
        Ahenk module
    """

    def __init__(self, filename, options):
        """
            Inits ahenk module.

            Args:
                filename: Module filename
                options: Ahenk options
        """
        self.filename = filename
        self.ctime = os.path.getctime(filename)
        # Compile module
        try:
            localSymbols = globalSymbols = {}
            code = open(filename).read()
            exec compile(code, "error", "exec") in localSymbols, globalSymbols
        except IOError, e:
            raise Error(_("Unable to read mod (%s): %s") % (filename, e))
        except SyntaxError, e:
            raise Error(_("SyntaxError in mod (%s): %s") % (filename, e))
        # Save locals, globals and initiate policy class
        self.locals = localSymbols
        self.globals = globalSymbols
        self.policy = localSymbols["policy"](options)

    def updateSettings(self, settings={}):
        """
            Updates module's policy settings.
        """
        self.policy.updateSettings(settings)

    def apply(self):
        """
            Calls module's apply() method.
        """
        self.policy.apply()

    def getTimers(self):
        """
            Returns module's tasks.
        """
        return self.policy.getTimers()


class ModManager:
    """
        Module manager.
    """

    def __init__(self, options):
        """
            Inits module manager.

            Args:
                options: Ahenk options
        """
        self.modules = {}
        self.options = options

    def update(self, filename, settings):
        """
            Adds or updates a module.

            Args:
                filename: Module filename
                settings: Policy settings
        """
        self.modules[filename] = Mod(filename, self.options)
        self.modules[filename].updateSettings(settings)

    def delete(self, filename):
        """
            Removes a module.

            Args:
                filename: Module filename
        """
        del self.modules[filename]

    def needUpdate(self, filename):
        """
            Returns if module needs to be updated.

            Args:
                filename: Module filename
        """
        if filename not in self.modules:
            return True
        if self.modules[filename].ctime != os.path.getctime(filename):
            return True
        return False

    def updateSettings(self, settings={}):
        """
            Updates policies of all modules.

            Args:
                settings: Policy settings
        """
        for filename, mod in self.modules.iteritems():
            mod.updateSettings(settings)

    def apply(self):
        """
            Calls all modules' apply() methods
        """
        for filename, mod in self.modules.iteritems():
            mod.apply()

    def getTimers(self, filename):
        """
            Returns a module's scheduled tasks.

            Args:
                filename: Module filename
        """
        return self.modules[filename].getTimers()


class LDAP:
    """
        LDAP connection class.
    """

    def __init__(self, hostname, domain, username=None, password=None):
        """
            Inits LDAP class.

            Args:
                hostname: LDAP host address
                domain: Ahenk server domain
                username: Username
                password: Password
        """
        self.dc = "dc=" + domain.replace(".", ", dc=")
        self.username = username
        self.password = password
        self.connection = ldap.open(hostname)

    def bind(self):
        """
            Authenticates to LDAP server and returns result.
        """
        if self.username and self.password:
            try:
                self.connection.simple_bind(self.username, self.password)
                return self.connection.whoami_s() != ""
            except ldap.SERVER_DOWN:
                return False
        else:
            return True

    def getAll(self):
        """
            Returns whole domain content. Don't use this method in production code.
        """
        return self.connection.search_s(self.dc, ldap.SCOPE_SUBTREE)

    def searchComputer(self, hostname=None):
        """
            Returns a computer's policy settings.

            Args:
                hostname: Hostname for the client
        """
        if not hostname:
            hostname = os.uname()[1]
        try:
            return self.connection.search_s(self.dc, ldap.SCOPE_SUBTREE, "(&(objectClass=pardusComputer)(cn=%s))" % hostname)
        except (ldap.SERVER_DOWN, ldap.NO_SUCH_OBJECT) :
            return None

    def close(self):
        """
            Closes LDAP connection.
        """
        self.connection.unbind_s()
        self.connection.close()


class Policy:
    """
        Policy skeleton. Ahenk modules inherit this class.

        Properties:
            label: Policy module label.
    """

    label = ""

    def __init__(self, options):
        """
            Inits Policy class.
        """
        self.log = logging.getLogger(self.label)
        self.options = options
        self.settings = {}
        self.init()

    def init(self):
        """
            Method to be called after class initialization.
        """
        pass

    def settingsUpdated(self):
        """
            Method to be called after policy settings are updated.
        """
        pass

    def updateSettings(self, settings={}):
        """
            Updates policy settings.

            Args:
                settings: Policy settings
        """
        self.settings = settings
        self.settingsUpdated()

    def getTimers(self):
        """
            Returns module's scheduled tasks.
        """
        return {}

    def apply(self):
        """
            Method to be called after a new policy fetched.
        """
        pass

    def runCommand(self, command):
        """
            Safe method for running shell commands. Does nothing if dry-run is enabled.

            Args:
                command: Shell command to execute
        """
        if self.options.dryrun:
            self.log.debug("Running %s" % command)
        else:
            os.system(command)
