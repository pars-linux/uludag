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
    try:
        return raw_input("%s > " % label)
    except KeyboardInterrupt:
        return None


class Task:
    def __init__(self, callable, interval):
        self.callable = callable
        self.interval = interval
        self.last = time.time()

    def update(self, callable, interval):
        self.callable = callable
        self.interval = interval

    def is_ready(self):
        if (time.time() - self.last) > self.interval:
            return True
        return False

    def run(self):
        self.last = time.time()
        self.callable()


class TaskManager:
    def __init__(self):
        self.tasks = {}

    def update(self, filename, timers):
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
        del self.tasks[filename]

    def check(self):
        for filename in self.tasks:
            for name, task in self.tasks[filename].iteritems():
                if task.is_ready():
                    task.run()


class Mod:
    def __init__(self, filename):
        self.filename = filename
        self.ctime = os.path.getctime(filename)
        try:
            localSymbols = globalSymbols = {}
            code = open(filename).read()
            exec compile(code, "error", "exec") in localSymbols, globalSymbols
        except IOError, e:
            raise Error(_("Unable to read mod (%s): %s") %(filename, e))
        except SyntaxError, e:
            raise Error(_("SyntaxError in mod (%s): %s") %(filename, e))
        self.locals = localSymbols
        self.globals = globalSymbols
        self.policy = localSymbols["policy"]

    def updateSettings(self, settings={}):
        self.policy.updateSettings(settings)

    def apply(self):
        self.policy.apply()

    def getTimers(self):
        return self.policy.getTimers()


class ModManager:
    def __init__(self):
        self.modules = {}

    def update(self, filename):
        self.modules[filename] = Mod(filename)

    def delete(self, filename):
        del self.modules[filename]

    def need_update(self, filename):
        if filename not in self.modules:
            return True
        if self.modules[filename].ctime != os.path.getctime(filename):
            return True
        return False

    def updateSettings(self, settings={}):
        for filename, mod in self.modules.iteritems():
            mod.updateSettings(settings)

    def apply(self):
        for filename, mod in self.modules.iteritems():
            mod.apply()

    def getTimers(self, filename):
        return self.modules[filename].getTimers()


class LDAP:
    def __init__(self, hostname, domain, username=None, password=None):
        self.dc = "dc=" + domain.replace(".", ", dc=")
        self.connection = ldap.open(hostname)
        if username:
            self.cn = "cn=" + username + ", " + self.dc
            self.connection.simple_bind(self.cn, password)

    def getAll(self):
        return self.connection.search_s(self.dc, ldap.SCOPE_SUBTREE)

    def searchComputer(self, hostname=None):
        if not hostname:
            hostname = os.uname()[1]
        return self.connection.search_s(self.dc, ldap.SCOPE_SUBTREE, "(&(objectClass=pardusComputer)(cn=%s))" % hostname)

    def close(self):
        self.connection.unbind_s()
        self.connection.close()

    def getLDIF(self, value):
        output = StringIO.StringIO()
        writer = ldif.LDIFWriter(output)
        writer.unparse(value[0], value[1])
        text = output.getvalue()
        output.close()
        return text


def getStrHash(s):
    return hashlib.sha1(s).hexdigest()

def getFileHash(f):
    if not os.path.exists(f):
        return ""
    return hashlib.sha1(file(f).read()).hexdigest()


class Policy:
    label = ""

    def __init__(self):
        self.log = logging.getLogger(self.label)
        self.settings = {}
        self.init()

    def init(self):
        pass

    def settingsUpdated(self):
        pass

    def updateSettings(self, settings={}):
        self.settings = settings
        self.settingsUpdated()

    def getTimers(self):
        return {}

    def apply(self):
        pass
