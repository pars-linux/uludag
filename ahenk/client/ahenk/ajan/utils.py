#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import time


def getText(label):
    try:
        return raw_input("%s > " % label)
    except KeyboardInterrupt:
        return None


class Task:
    def __init__(self, interval, callable):
        self.interval = interval
        self.callable = callable
        self.last = time.time()

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
        self.tasks[filename] = []
        for callable, interval in timers.iteritems():
            self.tasks[filename].append(Task(interval, callable))

    def delete(self, filename):
        del self.tasks[filename]

    def check(self):
        for filename in self.tasks:
            for task in self.tasks[filename]:
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

    def get_timers(self):
        timers = self.locals.get("timers", {})
        if callable(timers):
            timers = timers()
        if isinstance(timers, dict):
            return timers
        return {}


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

    def get_timers(self, filename):
        return self.modules[filename].get_timers()
