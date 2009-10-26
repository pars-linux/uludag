#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import threading
import time

from ahenk.ajan import utils

class Applier(threading.Thread):
    def __init__(self, options, queue_applier, queue_fetcher):
        threading.Thread.__init__(self)
        self.active = True
        self.options = options
        self.queue_applier = queue_applier
        self.queue_fetcher = queue_fetcher
        self.taskmanager = utils.TaskManager()
        self.modmanager = utils.ModManager()

    def run(self):
        while self.active:
            if not self.queue_applier.empty():
                policy = self.queue_applier.get()
                # FIXME: Apply policy
                logging.debug("Applying policy...")
                # FIXME: Apply policy
            else:
                # Update modules
                self.update_modules()
                # Run tasks
                self.taskmanager.check()
            time.sleep(0.5)

    def update_modules(self):
        files = []
        # Check for new/updated modules
        for fname in os.listdir(self.options.moddir):
            filename = os.path.join(self.options.moddir, fname)
            if fname.startswith("mod_") and fname.endswith(".py"):
                if self.modmanager.need_update(filename):
                    self.modmanager.update(filename)
                    self.taskmanager.update(filename, self.modmanager.get_timers(filename))
                    logging.debug("Updated module: %s" % filename)
                files.append(filename)
        # Remove missing modules
        for fname in set(self.modmanager.modules.keys()) - set(files):
            self.modmanager.delete(fname)
            self.taskmanager.delete(fname)
            logging.debug("Removed module: %s" % fname)


class Fetcher(threading.Thread):
    def __init__(self, options, queue_fetcher):
        threading.Thread.__init__(self)
        self.active = True
        self.options = options
        self.queue_fetcher = queue_fetcher
        self.ldap = utils.LDAP(options.hostname, options.domain)

    def run(self):
        while self.active:
            logging.debug("Checking policy...")
            policy = self.ldap.searchComputer()
            if len(policy):
                logging.debug("New policy fetched: %s" % policy)
                self.queue_fetcher.put(("policy", "x"))
            c = 0
            while c < self.options.interval and self.active:
                c += 0.5
                time.sleep(0.5)
