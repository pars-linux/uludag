#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

def setup():
    autotools.configure("--localstatedir=/var \
                         --disable-stripping \
                         --disable-caml-bindings \
                         --disable-java-bindings \
                         --without-curses \
                         --with-flite \
                         --with-espeak \
                         --with-speechd")

    # Fix overlinking
    pisitools.dosed("config.mk", "^HOSTMKMOD =.*", "HOSTMKMOD = $(CC) $(LDFLAGS) -shared -o")

def build():
    autotools.make()

def install():
    autotools.rawInstall("INSTALL_ROOT=%s" % get.installDIR())

    pisitools.remove("/usr/lib/libbrlapi.a")
    pisitools.dodoc("README")

