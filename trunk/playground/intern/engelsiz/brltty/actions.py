#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools
from pisi.actionsapi import get


def setup():
    autotools.configure("--disable-stripping \
                         --without-curses \
                         --with-flite \
                         --with-espeak \
                         --with-speechd \
                         --with-speech-dispatcher")

def build():
    autotools.make("-j1")

def install():
    autotools.rawInstall("INSTALL_ROOT=%s" % get.installDIR()) 
    
    pisitools.remove("/usr/lib/libbrlapi.a") 
    pisitools.dodoc("README")

