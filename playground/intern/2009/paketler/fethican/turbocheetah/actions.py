#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2005-2007 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import pisitools
from pisi.actionsapi import get

WorkDir = "TurboCheetah-%s" % get.srcVERSION()

def install():
    pythonmodules.install()

    #pisitools.removeDir("/usr/lib/python2.5/site-packages/TurboCheetah-1.0-py2.5.egg-info")
    pisitools.dosed("%s/usr/bin/TurboCheetah" % get.installDIR(),
                    get.installDIR(),
                    "/")
    pisitools.dodoc("README.txt")
