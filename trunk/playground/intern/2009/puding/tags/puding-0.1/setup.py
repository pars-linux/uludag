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
    for file in glob.glob("qt4/src/*"):
        shutil.copy(file, "puding/")

from puding.constants import NAME
from puding.constants import VERSION
from puding.constants import DESCRIPTION
from puding.constants import CORE_DEVELOPER
from puding.constants import CORE_EMAIL
from puding.constants import URL
from puding.constants import LICENSE_NAME

# General installation functions
def removeBuildFiles():
    rmDir = ["build", "locale", "puding"]

    # remove build directories
    for dir in rmDir:
        try:
            print("removing directory, %s.." % dir)
            shutil.rmtree(dir)

        except:
            pass

    # remove compiled Python files.
    for file in os.listdir("./"):
        if file.endswith(".pyc"):
            os.remove(file)

    # and remove desktop file.
    os.remove("datas/puding.desktop")

def convertQtFiles(file_list):
    qm_dir = "locale/qm"
    if not os.path.exists(qm_dir):
        os.makedirs(qm_dir)

    for i in file_list:
        file_name = os.path.split(i)[1]
        print("converting %s..." % i)
        if os.path.splitext(i)[1] == ".qrc":
            os.system("/usr/bin/pyrcc4 %s -o puding/%s" % (i, file_name.replace(".qrc", "_rc.py")))

        if os.path.splitext(i)[1] == ".ui":
            os.system("/usr/bin/pyuic4 %s -o puding/%s" % (i, file_name.replace(".ui", ".py")))

        if os.path.splitext(i)[1] == ".ts":
            os.system("/usr/bin/lrelease-qt4 %s -qm locale/qm/%s" % (i, file_name.replace(".ts", ".qm")))

def createMoFiles():
    mo_dir = "locale/mo/"
    if not os.path.exists(mo_dir):
        os.makedirs(mo_dir)

    po_list = glob.glob("po/*.po")
    data_list = []
    for path in po_list:
        po_file = os.path.split(path)[-1]
        lang = po_file.split(".")[0]
        mo_file = mo_dir + lang + "/%s.mo" % NAME

        os.mkdir(mo_dir + lang + "/")
        print("generating %s" % mo_file)
        os.system("msgfmt %s -o %s" % (path, mo_file))

        data_list.append(("share/locale/%s/LC_MESSAGES" % lang, ["locale/mo/%s/%s.mo" % (lang, NAME)]))

    return data_list

# Edit script
script = "%s/%s" % (NAME, NAME)
shutil.copyfile("%s.py" % script, script)
os.chmod(script, 0755)
os.remove("%s.py" % script)

# Convert desktop.in
os.system("intltool-merge -d po datas/puding.desktop.in datas/puding.desktop")

# Convert Qt files
qt_files = ["qt4/icons.qrc"]
qt_files.extend(glob.glob("qt4/ui/qt*.ui"))
qt_files.extend(glob.glob("qt4/ts/puding*.ts"))
convertQtFiles(qt_files)

data = [
    ("share/doc/puding", ["AUTHORS", "ChangeLog", "COPYING", "NOTES", "README", "TODO"]),
    ("share/puding", glob.glob("datas/syslinux.cfg.*")),
    ("share/puding/qm", glob.glob("locale/qm/puding*.qm")),
    ("share/applications", ["datas/puding.desktop"]),
    ("share/puding/gfxtheme", glob.glob("datas/gfxtheme/*")),
    ("share/pixmaps", ["images/puding.png"])]

data.extend(createMoFiles())

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
