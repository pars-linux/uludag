#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


import pds

PDS = pds.Pds('migration')
i18n = PDS.session.i18n
IconLoader = pds.QIconLoader(PDS)
KIcon = IconLoader.icon

OK, WARNING, ERROR = range(3)

user = None
sources = None
destinations = None
options = None
filesOptions = None
