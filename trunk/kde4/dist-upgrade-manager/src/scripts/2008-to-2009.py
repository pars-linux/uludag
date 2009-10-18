#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys
import os
import locale
import pisi

STATE = 0

def started(operation=""):
   notify("System.Upgrader", "started", operation)

def finished(operation=""):
   notify("System.Upgrader", "finished", operation)

def step(func):
    """
    Decorator for synchronizing privileged functions
    """
    def wrapper(*__args,**__kw):
        operation = "System.Upgrader.%s" % func.func_name

        started(operation)
        _init_pisi()
        try:
            func(*__args,**__kw)
        except KeyboardInterrupt:
            cancelled()
            return
        except Exception, e:
            notify("System.Upgrader", "error", str(e))
            return
        finished(operation)

    return wrapper

def reboot():
   notify("System.Upgrader", "needsreboot")
   sys.exit(0)
   # dbus-send --system --dest=org.freedesktop.Hal --type=method_call --print-reply /org/freedesktop/Hal/devices/computer  org.freedesktop.Hal.Device.SystemPowerManagement.Reboot

# Packages and Components that need to be fetched before upgrade
PACKAGES = ["kdm", "xdm", "pardus-default-settings"]
COMPONENTS = ["x11.driver"]

@step
def prepare():
    pisi.api.upgrade(["pisi"])

@step
def setrepos():
   for name in pisi.api.list_repos():
      pisi.api.remove_repo(name)

   pisi.api.add_repo("pardus-2009", "http://packages.pardus.org.tr/pardus-2009/pisi-index.xml.bz2")
   pisi.api.add_repo("contrib-2009", "http://packages.pardus.org.tr/contrib-2009/pisi-index.xml.bz2")

@step
def download():
   packages = set(pisi.api.get_upgrade_order() + PACKAGES)
   for component in COMPONENTS:
      packages = packages.union(pisi.db.componentdb.ComponentDB().get_union_packages(component))

   for package in packages:
      pisi.api.fetch(package, "/var/cache/pisi/packages")

@step
def upgrade():
   pisi.api.upgrade(ignore_comar=True)
   pisi.api.configure_pending()

   pisi.api.install(pisi.db.componentdb.ComponentDB().get_union_packages("x11.drivers"))

   os.unlink('/etc/X11/kdm/kdmrc')
   pisi.api.install(["kdm", "xdm"])
   pisi.api.install(["pardus-default-settings"])

@step
def cleanup(self):
    pass
