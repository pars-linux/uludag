#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyKDE
from PyKDE4.kdecore import KAboutData, ki18n, ki18nc

PACKAGE = "Firewall Manager"

# Application Data
appName     = "firewall-manager"
modName     = "firewallmanager"
programName = ki18n(PACKAGE)
version     = "3.0.0_alpha1"
description = ki18n(PACKAGE)
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2006-2010 TUBITAK/UEKAE")
text        = ki18n(None)
homePage    = "http://developer.pardus.org.tr/projects/firewall-manager"
bugEmail    = "bugs@pardus.org.tr"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Author(s)
aboutData.addAuthor(ki18n("Gökmen Göksel"), ki18n("Current Maintainer"))
aboutData.addAuthor(ki18n("Bahadır Kandemir"), ki18n("First Developer"))
aboutData.setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"), ki18nc("EMAIL OF TRANSLATORS", "Your emails"))

# Use this if icon name is different than appName
aboutData.setProgramIconName("security-high")
