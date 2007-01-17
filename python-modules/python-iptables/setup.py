#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import glob
import shutil
from distutils.core import setup
from distutils.command.install import install

version = "0.2"

distfiles = """
    setup.py
    iptables.py
    README
    COPYING
"""

def make_dist():
    distdir = "python-iptables-%s" % version
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
    os.popen("tar -czf %s %s" % ("python-iptables-" + version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)


setup(
    name = 'iptables',
    version = version,
    description = 'IPTables configuration module',
    license = 'GNU GPL2',
    py_modules=['iptables'],
)
