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
                         --disable-java-bindings \
                         --disable-lisp-bindings \
                         --disable-tcl-bindings \
                         --without-curses \
                         --with-espeak \
                         --with-speechd")

def build():
    autotools.make("-j1")

def install():
    #autotools.install()
    autotools.rawInstall("DESTDIR=%s" % get.installDIR()) 
    #autotools.rawInstall("DESTDIR=\"%s\" BINDIR=%s" % (get.installDIR(), get.sbinDIR())) 

    #pisitools.dodir("/etc")
    #pisitools.dodir("/etc/brltty")
    
    pisitools.dodoc("README")

