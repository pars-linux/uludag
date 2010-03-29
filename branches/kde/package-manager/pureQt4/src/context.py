#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import pds

Pds = pds.Pds('package-manager', debug = False)
# Force to use Default Session for testing
# Pds.session = pds.DefaultDe
print 'Current session is : %s %s' % (Pds.session.Name, Pds.session.Version)
i18n = Pds.session.i18n
KIconLoader = pds.QIconLoader(Pds)
KIcon = KIconLoader.icon
