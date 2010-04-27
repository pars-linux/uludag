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

import context as ctx

if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdecore import ki18n, KAboutData

    # Application Data
    appName     = "package-manager"
    catalog     = appName
    version     = "2.2.0"
    programName = ki18n("Package Manager")
    description = ki18n("Package Manager")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009-2010 TUBITAK/UEKAE")
    text        = ki18n(None)
    homePage    = "http://www.pardus.org.tr/eng/projects"
    bugEmail    = "bugs@pardus.org.tr"
    aboutData   = KAboutData(appName, catalog, programName, version, \
                    description, license, copyright, text, homePage, bugEmail)

    # Authors
    aboutData.addAuthor (ki18n("Gökmen Göksel"), ki18n("Maintainer"))
    aboutData.addAuthor (ki18n("Faik Uygur"), ki18n("Old Developer"))
    aboutData.setProgramIconName(":/data/package-manager.png")
