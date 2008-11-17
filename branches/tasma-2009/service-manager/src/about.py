#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyKDE4 Stuff
from PyKDE4.kdecore import *

# Application Data
appName     = "service-manager"
catalog     = ""
programName = ki18n("Service Manager")
version     = "0.1"
description = ki18n("Service Manager")
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2008 TUBITAK/UEKAE")
text        = ki18n(None)
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Authors
aboutData.addAuthor (ki18n("Gökmen GÖKSEL"),    ki18n("Current Maintainer"))
aboutData.addAuthor (ki18n("Bahadır Kandemir"), ki18n("COMAR Author"))

