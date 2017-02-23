#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--disable-static \
                         --disable-schemas-install \
                         --enable-key-snooper")

def build():
    autotools.make()

def install():
    autotools.install("libexecdir=%s/%s" % (get.installDIR(), get.libexecDIR()))
    pisitools.removeDir("/usr/share/pixmaps")

    pisitools.dodoc("AUTHORS", "COPYING", "README")
