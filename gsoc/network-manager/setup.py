#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import sys
import glob
import shutil
import kdedistutils

version = "2.0.6"

distfiles = """
    README
    *.py
    *.desktop
    images/*.png
    help/*.css
    help/*/*.html
    po/*.po
    po/*.pot
"""

def make_dist():
    distdir = "network-manager-%s" % version
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
    os.popen("tar -czf %s %s" % ("network-manager-" + version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

app_data = [
    'network-manager.py',
    'network-applet.py',
    'browser.py',
    'autoswitch.py',
    'handler.py',
    'connection.py',
    'widgets.py',
    'newconn.py',
    'icons.py',
    'comariface.py',
    'nameconf.py',
    ('/usr/kde/3.5/share/autostart/', ['network-applet.desktop']),
    ('/usr/kde/3.5/share/applications/kde/', ['network-applet.desktop']),
    'images/wireless-online.png',
    'images/wireless-connecting.png',
    'images/wireless-offline.png',
    'images/ethernet-online.png',
    'images/ethernet-connecting.png',
    'images/ethernet-offline.png',
    'images/dialup-online.png',
    'images/dialup-connecting.png',
    'images/dialup-offline.png',
    'images/signal_0.png',
    'images/signal_1.png',
    'images/signal_2.png',
    'images/signal_3.png',
    'images/signal_4.png',
    'help'
]

kdedistutils.setup(
    name="network-manager",
    version=version,
    author="Gürer Özen",
    author_email="gurer@pardus.org.tr",
    url="http://www.pardus.org.tr/projects/comar",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = app_data,
    executable_links = [
        ('network-manager', 'network-manager.py'),
        ('network-applet', 'network-applet.py'),
    ],
    i18n = ('po', ['.']),
    kcontrol_modules = [ ('network-manager.desktop','network-manager.py')],
)
