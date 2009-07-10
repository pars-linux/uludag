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

from PyKDE4.kdecore import KAboutData, ki18n

# Application Data
appName     = "migration"
modName     = "migration"
programName = ki18n("Migration Tool")
version     = "0.0.1"
description = ki18n("Migration Tool")
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2006-2009 TUBITAK/UEKAE")
text        = ki18n(" ")
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Author(s)
aboutData.addAuthor(ki18n("Mete Alpaslan"), ki18n("Current Maintainer"))
