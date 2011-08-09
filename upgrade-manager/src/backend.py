#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2011, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import pisi
import time
import urlgrabber

from pds import Pds

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

DEFAULT_REPO_2011 = "pardus-2011"
DEFAULT_REPO_2009 = "pardus-2009.2"
FORCE_INSTALL = "http://svn.pardus.org.tr/uludag/trunk/pardus-upgrade/2009_to_2011.list"
REPO_TEMPLATE = "http://packages.pardus.org.tr/pardus/2011/%s/i686/pisi-index.xml.xz"

# Translations
_pds = Pds('upgrade-manager', debug = False)
_ = _pds.i18n

def cleanup_pisi():
    """Close the database cleanly and do other cleanup."""
    import pisi.context as ctx
    ctx.disable_keyboard_interrupts()
    if ctx.log:
        ctx.loghandler.flush()
        ctx.log.removeHandler(ctx.loghandler)

    filesdb = pisi.db.filesdb.FilesDB()
    if filesdb.is_initialized():
        filesdb.close()

    if ctx.build_leftover and os.path.exists(ctx.build_leftover):
        os.unlink(ctx.build_leftover)

    ctx.ui.close()
    ctx.enable_keyboard_interrupts()

class SimpleLogger(object):

    def __init__(self):
        log_file = "/tmp/um-log"

        try:
            self.log_file = file(log_file, 'a+')
            self.log_file.write('\n')
        except:
            self.log_file = None
            self.log("FAILED TO LOGGING TO FILE: %s" % log_file, "LOGGER")
            self.log("I WILL USE STDOUT", "LOGGER")
        self.log("STARTED TO LOGGING AT %s" % time.asctime(), "LOGGER")

    def log(self, message, sender = 'ANONYMOUS'):
        now = time.strftime("%H:%M:%S", time.localtime())
        message = now + ' ' + ('|%-6s|' % ('%.6s' % sender)) + ' ' + message
        if self.log_file:
            self.log_file.write(message + '\n')
        print message

    def close(self):
        self.log_file.close()

    def markStep(self, step):
        step_file = os.path.expanduser("~/.umstep")
        open(step_file, 'w').write(str(step))

class PisiUI(QObject, pisi.ui.UI):

    def __init__(self, *args):
        pisi.ui.UI.__init__(self)
        apply(QObject.__init__, (self,) + args)

    def notify(self, event, **keywords):
        self.emit(SIGNAL("notify(int, PyQt_PyObject)"), \
                  event, keywords)

    def info(self, message, verbose = False, noln = False):
        pass
        # print "MM:", message

    def warning(self, message):
        pass
        # print "WR:", message

    def display_progress(self, **keywords):
        self.emit(SIGNAL("progress(PyQt_PyObject)"), keywords)

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class Iface(QObject, Singleton):

    """ Pisi Iface for UM """

    def __init__(self, parent):
        apply(QObject.__init__, (self,))
        options = pisi.config.Options()

        self.ui = PisiUI()
        self.connect(self.ui,\
                SIGNAL("progress(PyQt_PyObject)"),\
                parent.updateProgress)

        self.connect(self.ui,\
                SIGNAL("notify(int, PyQt_PyObject)"),\
                parent.processNotify)

        self._nof_packgages = 0

        self.parent = parent
        self.log = parent.logger.log
        pisi.api.set_userinterface(self.ui)
        pisi.api.set_options(options)
        pisi.api.set_signal_handling(False)

    def installPackages(self, packages, with_comar = True, reinstall = True, ignore_dep = False):
        self.log("PISI Installing : %s " % (','.join(packages)))

        options = pisi.config.Options()
        options.ignore_dependency = ignore_dep
        pisi.api.set_options(options)

        pisi.api.set_comar(with_comar)
        pisi.api.install(packages, reinstall = reinstall)

    def removePackages(self, packages, ignore_dependency = True, ignore_safety = True):
        pisi.api.remove(packages, ignore_dependency, ignore_safety)

    def upgradeSystem(self):
        self.log('PISI VERSION in STEP 2 is %s' % str(pisi.__version__), "BACKEND")

        options = pisi.config.Options()
        options.yes_all = True
        options.ignore_dependency = False
        pisi.api.set_options(options)
        pisi.api.set_comar(False)

        # Find the repository to upgrade system
        try:
            target_repo = file('/tmp/target_repo').read().strip()
        except:
            target_repo = REPO_TEMPLATE % "stable"

        self.log("ADDING REPO: %s" % target_repo, "BACKEND")
        pisi.api.add_repo(DEFAULT_REPO_2011, target_repo)

        # Updating repo from cli
        # If I use api for this it breaks the repository consistency
        self.log("STARTING TO UPDATE REPOSITORIES", "BACKEND")
        os.system('pisi ur %s' % DEFAULT_REPO_2011)
        self.log("UPDATING REPOSITORIES COMPLETED", "BACKEND")

        self.emit(SIGNAL("notify(PyQt_PyObject)"), _("Re-building the Package DB..."))

        # Try to rebuild the DB
        self.log("STARTING TO RE-BUILD PISI DB", "BACKEND")
        os.system('pisi rdb -y')
        self.log("RE-BUILDING PISI DB COMPLETED", "BACKEND")

        try:
            self.log("GETTING UPGRADABLE PACKAGES", "PISI")
            upgrade_list = pisi.api.list_upgradable()
            self._nof_packgages = len(upgrade_list)
            self.log("I FOUND %d PACKAGES TO UPGRADE" % self._nof_packgages, "PISI")

            self.emit(SIGNAL("notify(PyQt_PyObject)"), _("Calculating dependencies..."))

            # Upgrade the system
            self.log("STARTING TO UPGRADE", "PISI")
            pisi.api.upgrade(upgrade_list)
            self.log("PACKAGE UPGRADE COMPLETED", "PISI")
        except:
            self.log("PACKAGE UPGRADE FAILED SOMETHING WENT WRONG PLEASE TRY AGAIN LATER", "PISI")
            return False

        # Write down Nof packages has been upgraded
        file('/tmp/nof_package_upgraded','w').write(str(self._nof_packgages))

        # Install Required Packages
        self.log("FETCHING FORCE INSTALL PACKAGE LIST", "BACKEND")

        try:
            pkgs_to_install = urlgrabber.urlread(FORCE_INSTALL).split()
        except:
            self.log("FETCHING FAILED !!", "BACKEND")
            pkgs_to_install = []

        # Filter not available packages from force install list
        availables = pisi.api.list_available()
        pkgs_to_install = filter(lambda x: x in availables, pkgs_to_install)

        self._nof_packgages += len(pkgs_to_install)

        self.log("I FOUND %d PACKAGES TO INSTALL" % len(pkgs_to_install), "BACKEND")
        self.log("STARTING TO INSTALL FORCE LIST", "PISI")
        pisi.api.install(pkgs_to_install, reinstall = False)
        self.log("FORCE LIST INSTALLATION COMPLETED", "PISI")

        # Write down Nof packages has been upgraded
        file('/tmp/nof_package_upgraded','w').write(str(self._nof_packgages))

        return True

    def configureSystem(self):
        # Configure Pending !

        # Set number of upgraded packages
        try:
            self._nof_packgages = int(file('/tmp/nof_package_upgraded').read())
        except:
            self._nof_packgages = 0

        self.log("I FOUND %d PACKAGES TO CONFIGURE" % self._nof_packgages, "BACKEND")
        self.log("STARTING TO CONFIGURING","PISI")
        pisi.api.configure_pending(['baselayout'])
        pisi.api.configure_pending()
        self.log("CONFIGURE PENDING COMPLETED", "PISI")

    def upgradeRepos(self):
        pisi.api.update_repo(DEFAULT_REPO_2011)

    def removeRepos(self):
        repos = pisi.api.list_repos()
        for repo in repos:
            pisi.api.remove_repo(repo)

