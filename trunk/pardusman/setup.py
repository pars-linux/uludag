#!/usr/bin/python

from distutils.core import setup
from distutils.command.install import install
from distutils.cmd import Command

import glob
import os
import shutil
import sys

i18n_domain = "pardusman"
source_list = ["*.py"]

version = "1.0.0"

distfiles = """
    *.py
    *.png
    po/*.po
    po/*.pot
    *.xml
"""

def make_dist():
    distdir = "pardusman-%s" % version
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
    os.popen("tar -cjf %s %s" % ("pardusman-" + version + ".tar.bz2", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)

class Install(install):
    def run(self):
        install.run(self)
        self.installi18n()

    def installi18n(self):
        for item in os.listdir("po"):
            if item.endswith(".po"):
                lang = item.split(".")[0]
                print "Installing '%s' translations..." % lang
                os.popen("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
                if not self.root:
                    self.root = "/"
                destpath = os.path.join(self.root, "usr/share/locale/%s/LC_MESSAGES" % lang)
                try:
                    os.makedirs(destpath)
                except:
                    pass
                shutil.copy("po/%s.mo" % lang, os.path.join(destpath, "%s.mo" % i18n_domain))

class UpdateMessages(Command):
    user_options = []
    def run(self):
        os.system("xgettext -L Python -o po/pardusman.pot %s" % " ".join(source_list))
        for item in os.listdir("po"):
            if item.endswith(".po"):
                os.system("msgmerge -q -o temp.po po/%s po/pardusman.pot" % item)
                os.system("cp temp.po po/%s" % item)
        os.system("rm -f temp.po")
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

setup(name='pardusman',
      version='1.0',
      application_data = ['browser.py', 'gui.py', 'maker.py', 'packages.py',
                          'pardusman.py', 'project.py', 'utility.py', 'logo.png'],
      scripts=["pardusman.py"],
      cmdclass={"update_messages": UpdateMessages,
                "install": Install})
