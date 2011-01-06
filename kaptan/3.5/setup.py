#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) TUBITAK/UEKAE
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

# get version number
sys.path.append("src")
import screens
version = screens.version

distfiles = """
    README
    COPYING
    *.py
    pics/*.png
    src/screens/*.ui
    src/screens/*.py
    src/*.py
    src/*.desktop
    po/*.po
    po/*.pot
"""

def make_dist():
    distdir = "kaptan-%s" % version
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
    os.popen("tar -cjf %s %s" % ("kaptan-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    ('/usr/kde/3.5/share/apps/kaptan', ['src/kaptan.py']),
    ('/usr/kde/3.5/share/icons/hicolor/16x16/apps', ['pics/cr16-app-kaptan.png']),
    ('/usr/kde/3.5/share/apps/kaptan/pics', ['pics/']),
    ('/usr/kde/3.5/share/autostart/', ['src/kaptan.desktop']),
    ('/usr/kde/3.5/share/apps/kaptan/screens', ['src/screens']),
    ('/usr/kde/3.5/share/apps/kaptan/pics/themes', ['pics/themes/']),
    ('/usr/kde/3.5/share/apps/kaptan/pics/icons', ['pics/icons/'])
]

kdedistutils.setup(
    name="kaptan",
    version=version,
    author="Renan Çakırerk",
    author_email="renan@pardus.org.tr",
    url="http://www.pardus.org.tr/",
    #min_kde_version = "3.5.0",
    #min_qt_version = "3.3.5",
    license = "GPL",
    application_data = app_data,
    executable_links = [('kaptan', 'kaptan.py')],
    i18n = ('po', ['src', 'src/screens']),
)
