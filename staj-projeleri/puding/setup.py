#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# author: Gökmen Görgen, <gkmngrgn_gmail.com>
# license: GPLv3
#

import glob
import os
import shutil

from distutils.core import setup

if not os.path.exists("puding/"):
    shutil.copytree("src/", "puding/")

from puding.constants import (NAME, VERSION, DESCRIPTION, CORE_DEVELOPER, \
                            CORE_EMAIL, URL, LICENSE_NAME)

script = "%s/%s" % (NAME, NAME)
shutil.copyfile("%s.py" % script, script)
os.chmod(script, 0755)

#LANGS = ["tr"]

# General installation functions
# def locale(lang):
#    return("share/locale/%s/LC_MESSAGES" % lang,
#            ["data/po/locale/%s/%s.mo" % (lang, NAME)])

def removeBuildFiles():
    rmDir = ["build", "data/po/locale", NAME]

    # remove build directories
    for dir in rmDir:
        try:
            print("Removing directory, %s.." % dir)
            shutil.rmtree(dir)
        except:
            pass

    # remove compiled Python files.
    for file in os.listdir("./"):
        if file.endswith(".pyc"):
            os.remove(file)

# Create .mo files
# if not os.path.exists("data/po/locale"):
#    os.mkdir("data/po/locale")
# 
#    for lang in LANGS:
#        pofile = "data/po/" + lang + ".po"
#        mofile = "data/po/locale/" + lang + "/%s.mo" % NAME
# 
#        os.mkdir("data/po/locale/" + lang + "/")
#        print("generating %s" % mofile)
#        os.system("msgfmt %s -o %s" % (pofile, mofile))

data = [
    ("share/doc/%s" % NAME, ["AUTHORS", "ChangeLog", "COPYING", "NOTES", "README"]),
    ("share/%s" % NAME, glob.glob("data/syslinux.cfg.*")),
    ("share/%s/gfxtheme" % NAME, glob.glob("data/gfxtheme/*")),
    ("share/%s/ui" % NAME, glob.glob("data/ui/*"))]
#    ("share/%s/ui" % NAME, glob.glob("data/ui/*")),
#    locale("tr")]

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    author = CORE_DEVELOPER,
    author_email = CORE_EMAIL,
    url = URL,
    license = LICENSE_NAME,
    packages = [NAME],
    scripts = [script],
    data_files = data,
    )

# Clean build files and directories
removeBuildFiles()
