#!/usr/bin/python
# -*- coding: utf-8 -*-
#

from PyKDE4.kdecore import KAboutData, ki18n

appName = "pide"
modName = "pide"
programName = ki18n("Pide")
version = "0.0.1"
description = ki18n("PIDE")
license = KAboutData.License_GPL
copyright = ki18n("(c) 2009 TUBITAK/UEKAE")
text = ki18n(" ")
homePage = "http://www.pardus.org.tr/eng/projects"
bugEmail = "osman.mollahamid@gmail.com"
catalog = appName
aboutData = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Author(s)
aboutData.addAuthor(ki18n("Osman Mollahamut"), ki18n("Current Maintainer"))



