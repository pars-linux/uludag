#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import shutil
import tempfile

from distutils.core import setup
from distutils.command.install import install

PROJECT = "lider"

os.chmod('data/firewall.fwb', 0666)

def makeDirs(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass

def update_messages():
    potfiles_in = tempfile.mkstemp()[1]

    filelist = os.popen("find lider -name '*.py'").read().strip().split("\n")
    filelist.sort()
    with open(potfiles_in, "w") as _potfiles_in:
        _potfiles_in.write("\n".join(filelist))

    # Generate POT file
    os.system("xgettext --default-domain=%s \
                        --keyword=i18n \
                        --files-from=%s \
                        --output=po/%s.pot" % (PROJECT, potfiles_in, PROJECT))

    # Update PO files based on new POT file
    for item in glob.glob1("po", "*.po"):
        print "Updating %s..." % item
        os.system("msgmerge --update --no-wrap --sort-by-file po/%s po/%s.pot" % (item, PROJECT))

    # Cleanup
    os.unlink(potfiles_in)

class Install(install):
    def run(self):
        install.run(self)

        if self.root:
            root_dir = "%s/usr/share" % self.root
        else:
            root_dir = "/usr/share"

        locale_dir = os.path.join(root_dir, "locale")

        # Install locales
        print "Installing locales..."
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt -o po/%s.mo po/%s.po" % (lang, lang))
            makeDirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % PROJECT))

if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(name='ahenk-lider',
      version='1.9.30',
      description='Agent for Ahenk Remote Management Framework',
      author='Bahadır Kandemir',
      author_email='bahadir@pardus.org.tr',
      url='http://www.pardus.org.tr/',
      packages=['lider', 'lider.helpers', 'lider.plugins',
                'lider.plugins.plugin_authentication',
                'lider.plugins.plugin_firewall',
                'lider.plugins.plugin_services',
                'lider.plugins.plugin_software',
                'lider.plugins.plugin_web',
                'lider.widgets',
                'lider.widgets.list_item'],
      scripts=['ahenk_lider'],
      data_files=[('/usr/share/ahenk-lider/', ['data/firewall.fwb', 'data/firewall-failsafe.fwb']),
                  ('/etc/ahenk/plugins', ['data/plugins.conf'])
                 ],
      cmdclass={
                    'install': Install
               }

     )
