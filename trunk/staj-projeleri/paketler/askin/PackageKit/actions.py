#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--with-dbus-sys=/etc/dbus-1 \
                         --with-dbus-services=/usr/share/dbus-1/system-services \
                         --with-default-backend=pisi \
                         --enable-pisi \
                         --with-security-framework=polkit \
                         --localstatedir=/var \
                         --disable-static")

def build():
    autotools.make()

def install():
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.dodoc("README", "TODO", "MAINTAINERS", "HACKING", "AUTHORS", "NEWS")
    pisitools.doman("man/*.1")
    pisitools.dohtml("docs/html/")
