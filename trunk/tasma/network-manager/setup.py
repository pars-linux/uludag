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
# Please read the COPYING file.
#

import kdedistutils

app_data = [
    'network-manager.py',
    'mainwin.py',
    'connection.py',
    'widgets.py',
    'links.py',
    'icons.py',
    'stack.py',
    'images/wireless-online.png',
    'images/wireless-connecting.png',
    'images/wireless-offline.png',
    'images/ethernet-online.png',
    'images/ethernet-connecting.png',
    'images/ethernet-offline.png',
    'images/dialup-online.png',
    'images/dialup-connecting.png',
    'images/dialup-offline.png',
    'help'
]

kdedistutils.setup(
    name="network-manager",
    version="1.1",
    author="Gürer Özen",
    author_email="gurer@pardus.org.tr",
    url="http://www.pardus.org.tr/projects/comar",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = app_data,
    executable_links = [('network-manager','network-manager.py')],
    i18n = ('po', ['.']),
    kcontrol_modules = [ ('network-manager.desktop','network-manager.py')],
    )
