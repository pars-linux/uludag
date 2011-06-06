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

from PyQt4.QtCore import QObject
from PyQt4.QtCore import SIGNAL

DEFAULT_REPO_2011 = "pardus-2011"
DEFAULT_REPO_2009 = "pardus-2009.2"
FORCE_INSTALL = "http://svn.pardus.org.tr/uludag/trunk/pardus-upgrade/2009_to_2011.list"
REPO_TEMPLATE = "http://packages.pardus.org.tr/pardus/2011/%s/i686/pisi-index.xml.xz"

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

        # Make something crazy.
        # options.yes_all = True
        # options.ignore_safety = True

        self.ui = PisiUI()
        self.connect(self.ui,\
                SIGNAL("progress(PyQt_PyObject)"),\
                parent.updateProgress)

        self.connect(self.ui,\
                SIGNAL("notify(int, PyQt_PyObject)"),\
                parent.processNotify)

        self._nof_packgages = 0

        self.parent = parent
        pisi.api.set_userinterface(self.ui)
        pisi.api.set_options(options)
        pisi.api.set_signal_handling(False)

    def installPackages(self, packages, with_comar = True, reinstall = True, ignore_dep = False):

        print "PISI Installing : ", packages

        options = pisi.config.Options()
        options.ignore_dependency = ignore_dep
        pisi.api.set_options(options)

        pisi.api.set_comar(with_comar)
        pisi.api.install(packages, reinstall = reinstall)

    def upgradeSystem(self):
        print 'PISI VERSION in STEP 2 is', pisi.__version__

        options = pisi.config.Options()
        options.ignore_dependency = False
        pisi.api.set_options(options)
        pisi.api.set_comar(False)

        # Find the repository to upgrade system
        try:
            target_repo = file('/tmp/target_repo').read().strip()
        except:
            target_repo = REPO_TEMPLATE % "stable"

        print "ADDING REPO:", target_repo
        pisi.api.add_repo(DEFAULT_REPO_2011, target_repo)

        # Updating repo from cli
        # If I use api for this it breaks the repository consistency
        os.system('pisi ur %s' % DEFAULT_REPO_2011)

        # Try to rebuild the DB
        os.system('pisi rdb -y')

        upgrade_list = pisi.api.list_upgradable()
        self._nof_packgages = len(upgrade_list)
        print "I FOUND %d PACKAGES TO UPGRADE" % self._nof_packgages

        # Upgrade the system
        print "STARTING TO UPGRADE"
        pisi.api.upgrade(upgrade_list)

        # Install Required Packages
        pkgs_to_install = urlgrabber.urlread(FORCE_INSTALL).split()
        self._nof_packgages += len(pkgs_to_install)
        print "STARTING TO INSTALL FORCE LIST"
        pisi.api.install(pkgs_to_install, reinstall = True)

        # Write down Nof packages has been upgraded
        file('/tmp/nof_package_upgraded','w').write(str(self._nof_packgages))

    def configureSystem(self):
        # Configure Pending !

        # Set number of upgraded packages
        self._nof_packgages = int(file('/tmp/nof_package_upgraded').read())

        print "STARTING TO CONFIGURING"
        pisi.api.configure_pending(['baselayout'])
        pisi.api.configure_pending()

        self.parent.processNotify("STATE_3_FINISHED", {})

    def upgradeRepos(self):
        pisi.api.update_repo(DEFAULT_REPO_2011)

    def removeRepos(self):
        repos = pisi.api.list_repos()
        for repo in repos:
            pisi.api.remove_repo(repo)

