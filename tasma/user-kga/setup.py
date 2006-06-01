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
# Authors:  Gürer Özen <gurer@uludag.org.tr>

import kdedistutils

app_data = [
    'SetupUsers.py',
    'setupuserswidget.py',
    'users.py',
    'users_kga.py',
    'users_kga.desktop',
]

kdedistutils.setup(
    name="users_kga",
    version="0.1",
    author="İsmail Dönmez",
    author_email="ismail@uludag.org.tr",
    url="http://www.uludag.org.tr/",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = app_data,
    executable_links = [('users-kga','users_kga.py')],
    i18n = ('po', ['.']),
    kcontrol_modules = [ ('users_kga.desktop','users_kga.py')],
    )
