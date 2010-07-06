#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools

WorkDir = "flite-1.4-release"

def setup():
    #autotools.configure("--disable-static")  
    #autotools.configure("--prefix=/usr")
    autotools.configure("--enable-shared \
                         --with-audio=alsa" )

def build():
    autotools.make("-j1")

def install():
    #autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    autotools.install()
    
    pisitools.dodoc("COPYING", "README")

