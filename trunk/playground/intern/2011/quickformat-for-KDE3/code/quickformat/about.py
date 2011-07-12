#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 TUBITAK/BILGEM
# Renan Çakırerk <renan at pardus.org.tr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# (See COPYING)

from kdecore import KAboutData
from I18N import i18n

# Application Data
appName     = "quickformat"
programName = i18n("Quick Format")
version     = "1.0.0"
description = i18n("Removable Device Formatting Tool")
license     = KAboutData.License_GPL
copyright   = i18n("(c) 2011 TUBITAK/BILGEM")
text        = i18n(None)
homePage    = "http://www.pardus.org.tr/eng/projects"
bugEmail    = "bugs@pardus.org.tr"
catalog     = appName
