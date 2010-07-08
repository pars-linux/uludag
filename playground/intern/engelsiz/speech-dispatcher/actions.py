#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools


def setup():
    autotools.configure("--disable-static \
                         --without-ibmtts \
                         --without-ivona \
                         --without-nas \
                         --without-flite \
                         --with-alsa \
                         --with-espeak \
                         --with-libao \
                         --with-pulse")

def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.remove("/usr/share/info/ssip.info")

    pisitools.dodoc("AUTHORS", "COPYING", "README")

