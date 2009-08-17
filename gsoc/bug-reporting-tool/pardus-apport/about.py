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

# PyKDE
from PyKDE4.kdecore import KAboutData, ki18n

# Application Data
appName     = "paapport"
programName = ki18n("Pardus' Apport KDE GUI")
modName     = "papport"
version     = "4.0"
description = ki18n("Pardus' Apport KDE GUI")
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2005-2009 TUBITAK/UEKAE")
text        = ki18n(" ")
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Author(s)
aboutData.addAuthor(ki18n("GSoC"), ki18n("Current Maintainer"))
