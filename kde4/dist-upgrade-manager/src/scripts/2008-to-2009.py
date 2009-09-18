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

import os
import pisi

import iface

class Upgrader(State):

    # Packages and Components that need to be fetched before upgrade
    PACKAGES = ["kdm", "xdm", "pardus-default-settings"]
    COMPONENTS = ["x11.driver"]

    def __init__(self):
        self.pisi = iface.Iface()

    def prepare(self):
        self.pisi.upgrade(["pisi"])

    def setrepos(self):
        self.pisi.remove_repos()
        self.pisi.add_repo("pardus-2009", "http://packages.pardus.org.tr/pardus-2009/pisi-index.xml.bz2")

    def download(self):
        packages = set(self.pisi.upgrade_order() + PACKAGES + self.pisi.component_packages(COMPONENTS))
        self.pisi.download(packages)

    def install(self):
        # Upgrade and configure packages
        self.pisi.upgrade(ignore_comar=True)
        self.pisi.configure_pending()

        # Install missing x11 drivers
        self.pisi.install(component="x11.drivers")

        # Reinstall kdm
        os.unlink('/etc/X11/kdm/kdmrc')
        self.pisi.install("kdm", "xdm")
        self.pisi.install("pardus-default-settings")

    def cleanup(self):
        pass
