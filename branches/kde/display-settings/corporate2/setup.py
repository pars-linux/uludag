#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008-2009, TUBITAK/UEKAE
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

version = '0.5.80'

distfiles = """
    AUTHORS
    ChangeLog
    COPYING
    README
    TODO
    *.py
    src/*.ui
    src/*.png
    src/*.py
    src/*.desktop
    po/*.po
    po/*.pot
    pics/*.png
    help/*.css
    help/tr/*.html
    help/en/*.html
    xcb/*.py
    xcb/*.xml
"""

def make_dist():
    distdir = "display-settings-%s" % version
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
    os.popen("tar -czf %s %s" % ("display-settings-" + version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass

class Build(kdedistutils.BuildKDE):
    def run(self):
        kdedistutils.BuildKDE.run(self)

        # Clear all
        #os.system("rm -rf build")

        #makeDirs("build/app")
        makeDirs("build/lib/xcb")

        # Create xcb binding
        os.system("python xcb/py_client.py xcb/nvctrl.xml")
        self.move_file("nvctrl.py", "build/lib/xcb/")

class Install(kdedistutils.InstallKDE):
    def run(self):
        kdedistutils.InstallKDE.run(self)

        self.run_command("install_lib")


if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    'src/backend.py',
    'src/device.py',
    'src/display-manager.py',
    'src/dm_mainview.ui',
    'src/driverdialog.ui',
    'src/entryview.py',
    'src/helpdialog.ui',
    'src/monitordialog.ui',
    'src/nv.py',
    'src/randr.py',
    'src/randriface.py',
    'src/utility.py',
    'pics',
    'help'
]

kdedistutils.setup(
    name                = "display-manager",
    version             = version,
    author              = "Fatih Aşıcı",
    author_email        = "fatih@pardus.org.tr",
    url                 = "http://www.pardus.org.tr/",
    min_kde_version     = "3.5.0",
    min_qt_version      = "3.3.5",
    license             = "GPL",
    application_data    = app_data,
    executable_links    = [('display-manager','display-manager.py')],
    i18n                = ('po', ['src']),
    kcontrol_modules    = [ ('src/display-manager.desktop','src/display-manager.py')],
    cmdclass            = {
                            'build': Build,
                            'install': Install,
                          }
)
