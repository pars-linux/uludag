# -*- coding: utf-8 -*-
# PyKDE4 Stuff
from PyKDE4.kdecore import *

# Application Data
appName     = "konfigtracker"
programName = ki18n("KonfigTracker")
version     = "1.0"
description = ki18n("Snapshot and monitoring tool for KDE4 Settings")
license     = KAboutData.License_GPL
copyright   = ki18n("(c) 2010 TUBITAK/UEKAE")
text        = ki18n(None)
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
catalog     = appName
aboutData   = KAboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Authors
aboutData.addAuthor (ki18n("Jain Basil Aliyas"), ki18n("Developer"))
