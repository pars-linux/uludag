#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import kdedistutils

kdedistutils.setup(
    name="service-manager",
    version="1.1.1",
    author="Bahadır Kandemir",
    author_email="bahadir@pardus.org.tr",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/mainform.ui', 'src/service-manager.py',
                        ('/usr/kde/3.5/share/icons/hicolor/128x128/apps', ['src/service_manager.png']),
                        'help'],
    executable_links = [('service-manager','service-manager.py')],
    i18n = ('po',['src']),
    kcontrol_modules = [ ('src/service-manager.desktop','src/service-manager.py')],
    )
