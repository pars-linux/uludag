#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import os.path
import sys
import glob
import shutil
from distutils.core import setup, Extension
from distutils.command.install import install

__version = "0.1"

distfiles = """
    setup.py
    src/pare/utils/*.py
    src/pare/*.py
    po/*.po
    po/*.pot
    COPYING
    AUTHORS
    README
"""

def make_dist():
    distdir = "pare-python-%s" % __version
    list = []
    for t in distfiles.split():
        list.extend(glob.glob(t))
    if os.path.exists(distdir):
        shutil.rmtree(distdir)
    os.mkdir(distdir)
    for file_ in list:
        cum = distdir[:]
        for d in os.path.dirname(file_).split('/'):
            dn = os.path.join(cum, d)
            cum = dn[:]
            if not os.path.exists(dn):
                os.mkdir(dn)
        shutil.copy(file_, os.path.join(distdir, file_))
    os.popen("tar -czf %s %s" % ("pare-python-" + __version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

class Install(install):
    def finalize_options(self):
        # NOTE: for Pardus distribution
        if os.path.exists("/etc/pare-release"):
            self.install_platlib = '$base/lib/pare'
            self.install_purelib = '$base/lib/pare'
        install.finalize_options(self)

    def run(self):
        install.run(self)
        self.installi18n()

    def installi18n(self):
        for name in os.listdir('po'):
            if not name.endswith('.po'):
                continue
            lang = name[:-3]
            print "Installing '%s' translations..." % lang
            os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            if not self.root:
                self.root = "/"
            destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
            if not os.path.exists(destpath):
                os.makedirs(destpath)
            shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "pare-python.mo"))

setup(name="pare",
      version="0.1",
      description="Python Modules for Partition Editor(PARE)",
      long_description="Partition Editor Python Modules for YALI.",
      license="GNU GPL2",
      author="Mete Alpaslan",
      author_email="mete@pardus.org.tr",
      url="http://www.pardus.org.tr/",
      packages = ['pare', 'pare.utils'],
      package_dir = {'pare':'src/pare','pare.utils':'src/pare/utils'},
      cmdclass = {'install' : Install})
