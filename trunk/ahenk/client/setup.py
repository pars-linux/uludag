#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.command.install import install
from distutils.cmd import Command

import glob
import os
import shutil
import sys

version = "1.90"

distfiles = """
    setup.py
    ahenk-ajan.py
    ahenk/*.py
    ahenk/ajan/*.py
    modules/*.py
    etc/ahenk-ajan.conf
"""

def make_dist():
    distdir = "ahenk-ajan-%s" % version
    files = []
    for t in distfiles.split():
        files.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in files:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -cjf %s %s" % ("ahenk-ajan-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

class Install(install):

    def finalize_options(self):
        # NOTE: for Pardus distribution
        if os.path.exists("/etc/pardus-release"):
            self.install_platlib = '$base/lib/pardus'
            self.install_purelib = '$base/lib/pardus'
        install.finalize_options(self)

    def run(self):
        install.run(self)

setup(
    name="ahenk-ajan",
    version=version,
    license = "GPL",
    packages = [
        # Main module
        "ahenk",
        # Agent module
        "ahenk.ajan"
    ],
    data_files = [
        # Main application
        ('/sbin', ['ahenk-ajan.py']),
        # Configuration file
        ('/etc', ['etc/ahenk-ajan.conf']),
        # Modules
        ('/var/lib/ahenk-ajan', ['modules/mod_test.py']),
    ],
    cmdclass = {
        'install' : Install
    }
)
