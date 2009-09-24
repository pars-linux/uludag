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

from puding.constants import NAME
from puding.constants import VERSION
from puding.constants import DESCRIPTION
from puding.constants import CORE_DEVELOPER
from puding.constants import CORE_EMAIL
from puding.constants import URL
from puding.constants import LICENSE_NAME

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

def convertToPy(file_list):
    for i in file_list:
        file_name = os.path.split(i)[1]
        if os.path.splitext(i)[1] == ".qrc":
            os.system("/usr/bin/pyrcc4 %s -o puding/%s" % (i, file_name.replace(".qrc", "_rc.py")))

        if os.path.splitext(i)[1] == ".ui":
            # FIX ME: It should go to true directory.
            os.system("/usr/bin/pyuic4 %s -o puding/%s" % (i, file_name.replace(".ui", ".py")))

# Edit script
script = "%s/%s" % (NAME, NAME)
shutil.copyfile("%s.py" % script, script)
os.chmod(script, 0755)
os.remove("%s.py" % script)

# Convert Qt files
qt_files = ["data/icons.qrc"]
qt_files.extend(glob.glob("data/ui/qt*.ui"))
convertToPy(qt_files)

#LANGS = ["tr"]

# General installation functions
# def locale(lang):
#    return("share/locale/%s/LC_MESSAGES" % lang,
#            ["data/po/locale/%s/%s.mo" % (lang, NAME)])

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
    ("share/pixmaps", ["data/images/puding.png"]),
    ("share/%s/gfxtheme" % NAME, glob.glob("data/gfxtheme/*"))]
#    ("share/%s/ui" % NAME, glob.glob("data/ui/*"))]
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
