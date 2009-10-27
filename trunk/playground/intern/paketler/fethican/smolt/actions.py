#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2006-2008 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools
from pisi.actionsapi import pisitools

def build():
    shelltools.cd("client")
    autotools.make()

def install():
    shelltools.cd("client")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())

    pisitools.rename("/etc/smolt/config.py",
                     "smolt.cfg")
    pisitools.dosym("/etc/smolt/smolt.cfg",
                    "/usr/share/smolt/client/config.py")

    # Stupid makefile links executables to wrong place.Remove and link them again.
    pisitools.remove("/usr/bin/smoltSendProfile")
    pisitools.remove("/usr/bin/smoltDeleteProfile")
    pisitools.remove("/usr/bin/smoltGui")
    pisitools.dosym("/usr/share/smolt/client/sendProfile.py",
                    "/usr/bin/smoltSendProfile")
    pisitools.dosym("/usr/share/smolt/client/deleteProfile.py",
                    "/usr/bin/smoltDeleteProfile")
    pisitools.dosym("/usr/share/smolt/client/smoltGui.py",
                    "/usr/bin/smoltGui")

    pisitools.insinto("/usr/share/smolt/client",
                      "fs_util.py")
