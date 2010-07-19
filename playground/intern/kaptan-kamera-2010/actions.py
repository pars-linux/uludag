# -*- coding: utf-8 -*-
 
#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import pythonmodules

WorkDir = "v4l2capture-%s" % get.srcVERSION()

def setup():
    pythonmodules.run()

def build():
    pythonmodules.compile()

def install():
    pythonmodules.install()
    pisitools.dodoc("README")


