#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006,2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import sys
import glob
import shutil
from distutils.core import Extension
import kdedistutils

version = '1.1.1'

distfiles = """
    README
    AUTHORS
    *.py
    src/*.ui
    src/*.png
    src/*.py
    src/*.desktop
    src/icons/*.png
    src/help/*.css
    src/help/*/*.html
    po/*.po
    po/*.pot
"""

def make_dist():
    distdir = "boot-manager-%s" % version
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
    os.popen("tar -cjf %s %s" % ("boot-manager-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    'src/boot-manager.py',
    ('/usr/kde/3.5/share/icons/hicolor/128x128/apps', ['src/boot_manager.png']),
    'src/bm_mainview.py',
    'src/icons/pardus.png',
    'src/icons/linux.png',
    'src/icons/windows.png',
    'src/icons/other.png',
    'src/utility.py',
    'src/ui_elements.py',
    'src/backend.py',
    'src/boot-manager.desktop',
    'src/help',
]

kdedistutils.setup(
    name="boot-manager",
    version=version,
    author="Pardus Developers",
    author_email="info@pardus.org.tr",
    url="http://www.pardus.org.tr/",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = app_data,
    executable_links = [('boot-manager', 'boot-manager.py')],
    i18n = ('po', ['src']),
    kcontrol_modules = [ ('src/boot-manager.desktop', 'src/boot-manager.py')],
)
