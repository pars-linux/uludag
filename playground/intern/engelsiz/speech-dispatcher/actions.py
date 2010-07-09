#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/copyleft/gpl.txt.


from pisi.actionsapi import autotools
from pisi.actionsapi import pisitools


def setup():
    #autotools.autoreconf("-fi")
    autotools.configure("--disable-static \
                         --without-ibmtts \
                         --without-ivona \
                         --without-nas \
                         --with-alsa \
                         --with-flite \
                         --with-espeak \
                         --with-libao \
                         --with-pulse")

    #pisitools.dosed('libtool', '^hardcode_libdir_flag_spec=.*', 'hardcode_libdir_flag_spec=""')
    #pisitools.dosed('libtool', '^runpath_var=LD_RUN_PATH', 'runpath_var=DIE_RPATH_DIE')


def build():
    autotools.make()

def install():
    autotools.install()

    pisitools.remove("/usr/share/info/ssip.info")

    # Rename generically named binaries
    pisitools.rename("/usr/bin/long_message", "spd_long_message")
    pisitools.rename("/usr/bin/run_test", "spd_run_test")

    pisitools.dodoc("AUTHORS", "COPYING", "README")

