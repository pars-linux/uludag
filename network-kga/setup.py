#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

import kdedistutils

kdedistutils.setup(name="network_kga",
    version="0.0.1",
    author="İsmail Dönmez",
    author_email="ismail@uludag.org.tr",
    url="http://www.uludag.org.tr/",
    min_kde_version = "3.4.0",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = ['src/NetworkKga.py','src/MainWindow.ui'],
    executable_links = [('network_kga','NetworkKga.py')],
    kcontrol_modules = [ ('src/network_kga.desktop','NetworkKga.py')] )
