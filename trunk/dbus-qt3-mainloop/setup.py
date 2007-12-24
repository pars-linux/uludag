#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import shutil
import subprocess
from distutils.core import setup, Extension
from distutils.command.install import install

distfiles = """
    setup.py
    mainloop.cpp
"""

class Install(install):
    def finalize_options(self):
        if os.path.exists("/usr/lib/python2.4/site-packages/dbus/mainloop"):
            self.install_platlib = '$base/lib/python2.4/site-packages/dbus/mainloop'
            self.install_purelib = '$base/lib/python2.4/site-packages/dbus/mainloop'
        install.finalize_options(self)

    def run(self):
        install.run(self)

setup(
    name='pyqt3-dbus-mainloop',
    version='0.1',
    ext_modules=[Extension('qt3', ['src/mainloop.cpp'], include_dirs=['/usr/include/dbus-1.0',
                                                                          '/usr/lib/dbus-1.0/include',
                                                                          '/usr/qt/3/include'],
                                                                  define_macros=[('QT_SHARED', None),
                                                                                 ('QT_NO_DEBUG', None),
                                                                                 ('QT_THREAD_SUPPORT', None),
                                                                                 ('_REENTRANT', None)],
                                                                  library_dirs=['/usr/qt/3/lib', '/usr/X11R6/lib'],
                                                                  libraries=['dbus-1',
                                                                             'z', 'm', 'rt', 'dl',
                                                                             'pthread',
                                                                             'qt-mt'],
                                                                  extra_link_args=['-Wl,--version-script=qt.exp'])],
    cmdclass = {'install' : Install
    }
)
