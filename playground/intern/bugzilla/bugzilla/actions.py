#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get
from pisi.actionsapi import shelltools

def fixperms(d):
    for root, dirs, files in os.walk(d):
        for name in dirs:
            shelltools.chmod(os.path.join(root, name), 0755)
        for name in files:
            shelltools.chmod(os.path.join(root, name), 0644)

def install():
    #shelltools.copytree("/var/pisi/bugzilla-3.6.2-1/work/bugzilla-3.6.2", \
    #        "%s/var/www/localhost/htdocs/bugzilla" % get.installDIR())

    #pisitools.dodir
    pisitools.insinto("/var/www/localhost/htdocs/bugzilla", "*" )
