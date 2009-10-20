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

from kdecore import *

# Workaround the fact that PyKDE provides no I18N_NOOP as KDE
def I18N_NOOP(str):
    return str

# Application Data
appName     = "upgrade-manager"
catalog     = appName
programName = i18n("Distribution Upgrade Manager")
version     = "0.1"
description = i18n("Distribution Update Manager")
license     = KAboutData.License_GPL
copyright   = i18n("(c) 2009 TUBITAK/UEKAE")
text        = i18n(None)
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
aboutData   = KAboutData(appName, programName, version, description, license, copyright, text, homePage, bugEmail)

# Authors
aboutData.addAuthor (I18N_NOOP("Faik Uygur"), i18n("Maintainer"))
