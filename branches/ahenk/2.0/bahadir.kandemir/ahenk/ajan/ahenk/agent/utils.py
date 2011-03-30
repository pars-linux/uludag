#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Ajan utils.
"""

# Standard modules
import simplejson
import logging
import os
from multiprocessing import Process


class Message:
    """
        Base class for policy and command objects.
    """
    def __init__(self, message, q_out=None):
        """
            Args:
                message: Message dictionary
                q_out: Message queue for outgoing messages
        """
        self.message = message
        self.q_out = q_out
        self.type = "message"

class Command(Message):
    """
        Command object.
    """
    def __init__(self, message, q_out):
        """
            Args:
                message: Message dictionary
                q_out: Message queue for outgoing messages
        """
        Message.__init__(self, message, q_out)
        self.type = "command"
        if " " in message["command"]:
            try:
                self.command, self.arguments = message["command"].split(" ", 1)
                self.arguments = simplejson.loads(self.arguments)
            except:
                self.type = "invalid-command"
        else:
            self.command = message["command"]
            self.arguments = None
        self.sender = message["from"]

    def reply(self, command, arguments=None):
        """
            Replies messages.

            Args:
                messages: Reply
        """
        if self.q_out:
            if arguments != None:
                message = "%s %s" % (command, simplejson.dumps(arguments))
            else:
                message = command
            self.q_out.put({"to": self.sender, "body": message})

class Policy(Message):
    """
        Policy object.
    """
    def __init__(self, message, first_run=False):
        """
            Args:
                message: Message dictionary
                first_run: If it's first run
        """
        Message.__init__(self, message)
        self.type = "policy"
        self.policy = message["policy"]
        self.policy_stack = message["policy_stack"]
        self.first_run = first_run


def compile_module(filename):
    """
        Compiles a Python module and returns locals.

        Args:
            filename: Path to Python module
        Returns: Dictionary of local objects
    """
    try:
        locals = globals = {}
        code = open(filename).read()
        exec compile(code, "error", "exec") in locals, globals
    except IOError, e:
        logging.warning("Module has errors: %s" % filename)
    except SyntaxError, e:
        logging.warning("Module has syntax errors: %s" % filename)
    except Exception, e:
        logging.warning("Module has errors: %s" % filename)
    return locals

def process_modules(options, message, children):
    """
        Processes all Python modules' specified method.

        If method is forked, process is added to "children" list.

        Args:
            options: Options
            message: Message object
            children: List of child processes
    """
    for filename in os.listdir(options.moddir):
        if filename.startswith("mod_") and filename.endswith(".py"):
            filename = os.path.join(options.moddir, filename)
            locals = compile_module(filename)
            if "process" in locals:
                if locals.get("forkProcess", False):
                    proc = Process(target=locals["process"], args=(message, options))
                    children.append(proc)
                    proc.start()
                else:
                    locals["process"](message, options)

def update_cron(command, schedule=None, username="root", noargs=False, filename="/etc/cron.d/ahenk"):
    """
        Updates an crontab record in /etc/crontab file.

        Arguments:
            command: Command to execute
            noargs: True if arguments will be ignored while matching commands
            username: Username to execute command as.
            filename: Path to crontab file

        Returns True if command was found in /etc/crontab
    """
    matched = False
    lines = []

    if os.path.exists(filename):
        for line in file(filename):
            line = line.strip("\n")
            if not matched:
                try:
                    c_min, c_hour, c_day, c_month, c_dayofweek, c_user, c_cmd = line.split(None, 6)
                except ValueError:
                    lines.append(line)
                    continue
                if (noargs and c_cmd.split()[0] == command.split()[0]) or c_cmd == command:
                    matched = True
                    if schedule:
                        lines.append("%s %s %s" % (schedule, username, command))
                else:
                    lines.append(line)
            else:
                lines.append(line)

    if not matched and schedule:
        lines.append("%s %s %s" % (schedule, username, command))

    lines = "\n".join(lines)
    file(filename, "w").write(lines)

    return matched
