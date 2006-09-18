#!/usr/bin/python

from distutils.core import setup
from distutils.command.install import install
from distutils.cmd import Command

import os
import shutil

i18n_domain = "plsa"
source_list = ["plsa/*.py", "plsa-cli"]

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
        os.system("xgettext -L Python -o po/plsa.pot %s" % " ".join(source_list))
        for item in os.listdir("po"):
            if item.endswith(".po"):
                os.system("msgmerge -q -o temp.po po/%s po/plsa.pot" % item)
                os.system("cp temp.po po/%s" % item)
        os.system("rm -f temp.po")
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass

setup(name='plsa',
      version='1.0',
      packages=['plsa'],
      scripts=["plsa-cli"],
      cmdclass={"update_messages": UpdateMessages,
                "install": Install})
