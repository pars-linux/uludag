#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen
# license: GPLv3 (Read COPYING file.)
#

from os import getenv

NAME = "puding"
LOCALE = "/usr/share/locale"
VERSION = "0.1"
HOME = "%s/.%s" % (getenv("HOME"), NAME)
SHARE = "/usr/share/%s" % NAME
SYSLINUX = "/usr/lib/syslinux"
URL = "http://www.gokmengorgen.net/puding"
CORE_DEVELOPER = u"Gökmen Görgen"
CORE_EMAIL = "gkmngrgn [at] gmail.com"
ART_CONTRIBUTOR = u"Yasin Özcan, hamfindik [at] gmail.com"
TRANSLATORS = u"""\
de: Stefan Wilhelm, sw1976de [at] googlemail.com<br />
es: Klemens Häckel click3d [at] linuxmail. org<br />
fr: Philippe Svetoslavsky, philsvet [at] gmail.com<br />
nl: Anton Tolboom, atolboo [at] gmail.com<br />
sv: Patrik Karlsson, patrik [at] pardus.nu<br />
tr: Necmettin Begiter, necmettin.begiter [at] gmail.com
"""
SUMMARY = "An USB Image Creator For Pardus Linux."
DESCRIPTION = "Puding is an USB image creator for Pardus Linux."
YEAR = "2009"
COPYRIGHT = u"Copyright (c) %s TUBITAK / UEKAE" % YEAR
LICENSE_NAME = "GPLv3"
LICENSE = """%s

Puding is a free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

Puding is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.\
""" % COPYRIGHT
