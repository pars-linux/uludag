#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
import os
import threading
import time

from ahenk.ajan import utils

class Applier(threading.Thread):
    """
        Policy applier thread.

        Properties:
            active: If thread is active and running
    """

    def __init__(self, options, queue_applier, queue_fetcher):
        """
            Inits policy applier thread.

            Args:
                options: Ahenk options
                queue_applier: Applier queue object
                queue_fetcher: Fetcher queue object
        """
        threading.Thread.__init__(self)
        self.active = True
        self.options = options
        self.queue_applier = queue_applier
        self.queue_fetcher = queue_fetcher
        self.taskmanager = utils.TaskManager()
        self.modmanager = utils.ModManager(options)

    def run(self):
        """
            Applier thread main loop.
        """
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
        """
            Reads modules and updates their scheduled tasks.
        """
        for filename in self.taskmanager.tasks:
            if filename in self.modmanager.modules:
                self.taskmanager.update(filename, self.modmanager.getTimers(filename))
            else:
                self.taskmanager.delete(filename)

    def updateModules(self):
        """
            Checks module directory and loads new/updated modules.
        """
        fn_policy = os.path.join(self.options.policydir, "latest_policy")
        if os.path.exists(fn_policy):
            policy = utils.parseLDIF(open(fn_policy))
        else:
            policy = {}
        files = []
        # Check for new/updated modules
        for fname in os.listdir(self.options.moddir):
            filename = os.path.join(self.options.moddir, fname)
            if fname.startswith("mod_") and fname.endswith(".py"):
                if self.modmanager.needUpdate(filename):
                    # Update new/updated modules
                    self.modmanager.update(filename, policy)
                    # Update scheduled tasks
                    self.taskmanager.update(filename, self.modmanager.getTimers(filename))
                    logging.debug("Updated module: %s" % filename)
                files.append(filename)
        # Remove old modules
        for fname in set(self.modmanager.modules.keys()) - set(files):
            self.modmanager.delete(fname)
            self.taskmanager.delete(fname)
            logging.debug("Removed module: %s" % fname)


class Fetcher(threading.Thread):
    """
        Policy fetcher thread.

        Properties:
            active: If thread is active and running
    """

    def __init__(self, options, queue_fetcher):
        """
            Inits policy fetcher thread.

            Args:
                options: Ahenk options
                queue_fetcher: Policy fetcher queue
        """
        threading.Thread.__init__(self)
        self.active = True
        self.options = options
        self.queue_fetcher = queue_fetcher
        self.connected = False

    def run(self):
        """
            Fetcher thread main loop.
        """
        def _sleep():
            c = 0
            while c < self.options.interval and self.active:
                c += 0.5
                time.sleep(0.5)

        while self.active:
            # Try to connect to LDAP server
            if not self.connected:
                self.ldap = utils.LDAP(self.options.hostname, self.options.domain, self.options.username, self.options.password)
                if self.ldap.bind():
                    self.connected = True
                    logging.debug("Connected to policy server.")
                else:
                    logging.error("Unable to connect to policy server.")
                    _sleep()
                    continue
            # Check policy
            logging.debug("Checking policy...")
            policy = self.ldap.searchComputer()
            if policy == None:
                logging.debug("Unable to query policy server, will try again.")
                self.connected = False
                _sleep()
                continue
            # Add to queue if policy is updated
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
            _sleep()
