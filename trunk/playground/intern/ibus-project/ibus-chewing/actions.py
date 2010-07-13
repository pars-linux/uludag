#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2010 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import cmaketools
from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "%s-%s-Source" % (get.srcNAME(), get.srcVERSION())

def setup():
    cmaketools.configure("-DCMAKE_BUILD_TYPE=RelWithDebInfo -DKDEDIR=%s" % get.kdeDIR())

def build():
    cmaketools.make()

def install():
    autotools.rawInstall("DESTDIR=%s libexecdir=/%s" %(get.installDIR(), get.libexecDIR()))

    pisitools.dodoc("AUTHORS", "README", "ChangeLog", "NEWS", "COPYING")

