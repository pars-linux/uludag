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

from distutils.core import Extension
import kdedistutils

app_data = [
    'user-manager.py',
    'mainview.py',
    'browser.py',
    'useredit.py',
    'groupedit.py',
    'utility.py',
    'user-manager.desktop',
]

capslockedmodule = Extension('capslocked',
                        sources = ['capslocked.c'],
                        extra_compile_args = ['-Wall -lX11'])

kdedistutils.setup(
    name="user-manager",
    version="0.5",
    author="Gürer Özen",
    author_email="gurer@pardus.org.tr",
    url="http://www.pardus.org.tr/",
    min_qt_version = "3.3.0",
    license = "GPL",
    application_data = app_data,
    executable_links = [('user-manager','user-manager.py')],
    i18n = ('po', ['.']),
    ext_modules = [capslockedmodule],
    kcontrol_modules = [ ('user-manager.desktop','user-manager.py')],
)
