#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2006-2008 TUBITAK/UEKAE
# Licensed under the GNU General Public License, version 2.
# See the file http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt

from pisi.actionsapi import pythonmodules
from pisi.actionsapi import get
from pisi.actionsapi import pisitools

WorkDir = "CherryPy-%s" % get.srcVERSION()

def install():
    pisitools.dosed("cherrypy/test/test.py", "raw_input", "")
    pisitools.dosed("cherrypy/test/test.py", "'test_cache_filter',", "")
    pisitools.dosed("setup.py", "distutils.core", "setuptools")
    pisitools.dosed("setup.py", "\"cherrypy.tutorial\",", "")
    pisitools.dosed("setup.py", "('cherrypy\/tutorial',/, /),", "/d")
    pythonmodules.install()

    pisitools.dodoc("README.txt")
