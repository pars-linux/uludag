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

WorkDir = "smolt-%s" % get.srcVERSION()

def build():
    shelltools.cd("client")
    autotools.make()

def install():
    shelltools.cd("client")
    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    pisitools.domove("/etc/smolt/config.py",
                     "/etc",
                     "smolt.cfg")
    pisitools.dosym("/etc/smolt.cfg",
                    "/usr/share/smolt/client/config.py")
    pisitools.dosym("%s/usr/share/smolt/client/sendProfile.py" % get.installDIR(),
                    "%s/usr/bin/smoltSendProfile" % get.installDIR())
    shelltools.copy("%s/smolt-%s/client/fs_util.py" % ( get.workDIR(), get.srcVERSION()),
                    "%s/usr/share/smolt/client" % get.installDIR())
    shelltools.touch("%s/etc/smolt/hw-uuid" % get.installDIR())
