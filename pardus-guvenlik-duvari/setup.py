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
#
#
# Authors:  Bahadır Kandemir <bahadir@pardus.org.tr>

import kdedistutils

kdedistutils.setup(
    name="fw_kga",
    version="0.1",
    author="Bahadır Kandemir",
    author_email="bahadir@pardus.org.tr",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['src/firewall.ui', 'src/fw_kga.py'],
    executable_links = [('fw-kga','fw_kga.py')],
    i18n = ('po',['src']),
    kcontrol_modules = [ ('src/fw_kga.desktop','src/fw_kga.py')]
    )
