#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2005 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.
#
# A. Murat Eren <meren at uludag.org.tr>

from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi import get

WorkDir = "merhaba-pisi-1.0"

def install():
    pisitools.dobin("merhaba-pisi.py")
    pisitools.rename("/usr/bin/merhaba-pisi.py", "merhaba-pisi")
    pisitools.dodir("/usr/lib")
    shelltools.copy(get.installDIR() + "/usr/bin/merhaba-pisi", get.installDIR() + "/usr/lib/merhaba-osman")
