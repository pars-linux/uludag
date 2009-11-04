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
                logging.debug("Applying policy: %s" % policy)
                # Pass settings to modules
                self.modmanager.updateSettings(policy)
                # Update timers
                self.updateTimers()
                # Apply settings
                self.modmanager.apply()
            else:
                # Update modules
                self.updateModules()
                # Run tasks
                self.taskmanager.fire()
            time.sleep(0.5)

    def updateTimers(self):
        for filename in self.taskmanager.tasks:
            if filename in self.modmanager.modules:
                self.taskmanager.update(filename, self.modmanager.getTimers(filename))
            else:
                self.taskmanager.delete(filename)

    def updateModules(self):
        fn_policy = os.path.join(self.options.policydir, "latest_policy")
        policy = utils.parseLDIF(open(fn_policy))
        files = []
        # Check for new/updated modules
        for fname in os.listdir(self.options.moddir):
            filename = os.path.join(self.options.moddir, fname)
            if fname.startswith("mod_") and fname.endswith(".py"):
                if self.modmanager.needUpdate(filename):
                    self.modmanager.update(filename, policy)
                    self.taskmanager.update(filename, self.modmanager.getTimers(filename))
                    logging.debug("Updated module: %s" % filename)
                files.append(filename)
        # Remove old modules
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
                ldif = utils.getLDIF(policy[0])
                fn_policy = os.path.join(self.options.policydir, "latest_policy")
                hash = utils.getFileHash(fn_policy)
                if hash != utils.getStrHash(ldif):
                    file(fn_policy, "w").write(ldif)
                    logging.debug("New policy fetched: %s" % policy[0][1])
                    self.queue_fetcher.put(("policy", policy[0][1]))
                else:
                    logging.debug("Policy is not changed.")
            else:
                logging.debug("No policy defined.")
            c = 0
            while c < self.options.interval and self.active:
                c += 0.5
                time.sleep(0.5)
