#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
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

version = "2.3.2"

distfiles = """
    README
    AUTHORS
    *.py
    *.desktop
    po/*.po
    po/*.pot
    help/*.css
    help/*/*.html
"""

def make_dist():
    distdir = "user-manager-%s" % version
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
    os.popen("tar -czf %s %s" % ("user-manager-" + version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    'user-manager.py',
    'um_mainview.py',
    'um_browser.py',
    'um_list.py',
    'useredit.py',
    'groupedit.py',
    'um_utility.py',
    'user-manager.desktop',
    'security-high.png',
    'security-medium.png',
    'security-low.png',
    'help'
]

kdedistutils.setup(
    name="user-manager",
    version=version,
    author="Gürer Özen",
    author_email="gurer@pardus.org.tr",
    url="http://www.pardus.org.tr/",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = app_data,
    executable_links = [('user-manager','user-manager.py')],
    i18n = ('po', ['.']),
    kcontrol_modules = [ ('user-manager.desktop','user-manager.py')],
)
