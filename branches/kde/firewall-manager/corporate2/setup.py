#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006,2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import sys
import glob
import shutil

import kdedistutils

version = "2.1.0"

distfiles = """
    AUTHORS
    README
    *.py
    src/*.py
    src/*.ui
    src/*.desktop
    src/*.png
    po/*.po
    po/*.pot
    profiles/*
"""

def make_dist():
    distdir = "firewall-config-%s" % version
    list = []
    for t in distfiles.split():
        list.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in list:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -cjf %s %s" % ("firewall-config-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

kdedistutils.setup(
    name="firewall-config",
    version=version,
    author="Pardus Developers",
    author_email="gokmen@pardus.org.tr",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = [ "src/dialog.ui", "src/firewall-config.py", "src/rules.py", "src/fw_handler.py", "src/fw_utils.py", "help",
                         "src/default.png", "src/user-defined.png", "src/apply.png",
                        ("/usr/kde/3.5/share/icons/hicolor/128x128/apps", ["src/firewall_config.png"]),
                        ("/usr/kde/3.5/share/icons/hicolor/48x48/apps", ["src/fw-locked.png"]),
                        ("/usr/kde/3.5/share/icons/hicolor/48x48/apps", ["src/fw-unlocked.png"]),
                        ("/var/lib/iptables", ["profiles/pardus"]),
                        ],
    executable_links = [("firewall-config", "firewall-config.py")],
    i18n = ("po", ["src"]),
    kcontrol_modules = [("src/firewall-config.desktop", "src/firewall-config.py")]
    )
