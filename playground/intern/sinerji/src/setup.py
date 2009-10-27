#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob 
import shutil
from distutils.core import setup
from distutils.command.install import install

version = "0.1"

distfiles = """
    README
    AUTHORS
    COPYING
    setup.py
    po/*.po
    sinerji/*.py
    sinerji/sinerji
    sinerji/*.ui
    sinerji/*.qrc
    sinerji/images/*.png
    sinerji/images/sinerji.desktop
"""

def image_files():
    p = "sinerji/images/*"
    return glob.glob(p)

def resource_files():
    p = "sinerji/*.qrc"
    return glob.glob(p)	

def make_dist():
    distdir = "sinerji-%s" % version
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
    os.popen("tar -czf %s %s" % ("sinerji-" + version + ".tar.gz", distdir))
    shutil.rmtree(distdir)

if "dist" in sys.argv:
    make_dist()
    sys.exit(0)


class I18nInstall(install):
    def run(self):
        install.run(self)
        shutil.copy("sinerji/images/sinerji.desktop", "/usr/share/applications/sinerji.desktop")
        shutil.copy("sinerji/images/sinerji.png", "/usr/share/pixmaps/sinerji.png")
        i18n_domain = "sinerji"
        i18n_languages = ["tr", "es"]  ### List of languases, if other languages is added, add it to this list, like ["tr","en" ]
        for lang in i18n_languages:
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



setup (name='Sinerji',
      version=version,
      description='Sinerji is a fronted for Synergy',
      author='Fatih Arslan',
      author_email='fatih@arsln.org',
      url='http://blog.arsln.org',
      license='GNU GPL2',
      packages = ['sinerji'],
      package_dir = {'': ''},
      data_files = [('/usr/share/sinerji', resource_files()), 
          ('/usr/share/sinerji/images', image_files())],
      scripts = ['sinerji/sinerji'],
      cmdclass = {
        'install': I18nInstall,
        }
)





