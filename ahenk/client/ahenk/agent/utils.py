#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Ajan utils.
"""


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
        self.command = message["command"]
        self.sender = message["from"]

    def reply(self, message):
        """
            Replies messages.

            Args:
                messages: Reply
        """
        if self.q_out:
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
    return locals

def process_modules(options, message, children):
    """
        Processes all Python modules' specified method.

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
                    proc = Process(target=locals["process"], args=(message,))
                    children.append(proc)
                    proc.start()
                else:
                    locals["process"](message, dryrun=options.dryrun)
