#!/usr/bin/python
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
            --disable-dbus-python-check")

def build():
    autotools.make()

def install():
    autotools.install("libexecdir=%s/%s" % (get.installDIR(), get.libexecDIR()))
    #autotools.install()
    pisitools.dodoc("AUTHORS", "ChangeLog", "COPYING", "NEWS", "README")
