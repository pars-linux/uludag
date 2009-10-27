#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007 TUBITAK/UEKAE
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

version = "0.1.2"

distfiles = """
    AUTHORS
    COPYING
    README
    *.py
    src/*.py
    src/*.ui
    src/*.desktop
    src/pics/*.png
    help/*.css
    help/*/*.html
    po/*.po
    po/*.pot
"""

def make_dist():
    distdir = "history-manager-%s" % version
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
    os.popen("tar -cjf %s %s" % ("history-manager-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

kdedistutils.setup(
    name="history-manager",
    version=version,
    author="İşbaran Akçayır",
    author_email="isbaran@gmail.com",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/historygui.ui', 'src/Progress.ui', 'src/progress.py', 'src/history-manager.py', 'src/historygui.py', 'src/ComarIface.py', 'src/Commander.py', 'src/handler.py', 'src/history_gui.py', 'src/utility.py', 'src/PisiIface.py',
                        ('/usr/kde/3.5/share/apps/history-manager/pics', ['src/pics/History_Manager.png', 'src/pics/details.png', 'src/pics/install.png', 'src/pics/remove.png', 'src/pics/snapshot.png', 'src/pics/takeback.png', 'src/pics/upgrade.png']),
                        'help'],
    executable_links = [('history-manager','history-manager.py')],
    i18n = ('po',['src']),
    kcontrol_modules = [ ('src/history-manager.desktop','src/history-manager.py')],
    )
