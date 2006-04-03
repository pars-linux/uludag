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
    name="fw-kwa",
    version="0.1",
    author="Bahadır Kandemir",
    author_email="bahadir@haftalik.net",
    min_kde_version = "3.5.0",
    min_qt_version = "3.3.5",
    license = "GPL",
    application_data = ['firewall.ui', 'fw.py'],
    executable_links = [('fw-kga','fw-kga.py')],
    i18n = ('po',['src'])
    )
