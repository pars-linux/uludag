#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import pt

# Application Data
appName     = "package-manager"
catalog     = appName
version     = "2.0.4"
programName = pt.ki18n("Package Manager")
description = pt.ki18n("Package Manager")
license     = pt.AboutData.License_GPL
copyright   = pt.ki18n("(c) 2009-2010 TUBITAK/UEKAE")
text        = pt.ki18n(None)
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
aboutData   = pt.AboutData(appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)

# Authors
aboutData.addAuthor (pt.ki18n("Faik Uygur"), pt.ki18n("Maintainer"))
aboutData.setProgramIconName(":/data/package-manager.png")
