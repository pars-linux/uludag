#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TUBITAK/BILGEM
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import pythonmodules

def setup():
    autotools.configure("--disable-dmtxread \
                         --disable-dmtxwrite \
                         --disable-dmtxquery")

def build():
    autotools.make()

def install():
    autotools.install()
    pisitools.removeDir("/usr/share/man/man1")
    pisitools.removeDir("/usr/lib/pkgconfig")
    pisitools.dodoc("AUTHORS", "COPYING", "README")
