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

version = '2.1.5'

distfiles = """
    README
    AUTHORS
    *.py
    src/*.ui
    src/*.png
    src/*.py
    src/*.desktop
    po/*.po
    po/*.pot
    help/*.css
    help/tr/*.html
    help/en/*.html
    help/es/*.html
"""

def make_dist():
    distdir = "service-manager-%s" % version
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
    os.popen("tar -cjf %s %s" % ("service-manager-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    'src/service-manager.py',
    ('/usr/kde/3.5/share/icons/hicolor/128x128/apps', ['src/service_manager.png']),
    'src/sm_mainview.py',
    'src/sm_backend.py',
    'src/service_manager.ui',
    'src/sm_utility.py',
    'src/handler.py',
    'src/service-manager.desktop',
    'help'
]

kdedistutils.setup(
    name="service-manager",
    version=version,
    author="Pardus Developers",
    author_email="info@pardus.org.tr",
    url="http://www.pardus.org.tr/",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = app_data,
    executable_links = [('service-manager', 'service-manager.py')],
    i18n = ('po', ['src']),
    kcontrol_modules = [ ('src/service-manager.desktop', 'src/service-manager.py')],
)
