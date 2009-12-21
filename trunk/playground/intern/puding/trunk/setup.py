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

from puding.constants import VERSION
from puding.constants import DESCRIPTION
from puding.constants import CORE_DEVELOPER
from puding.constants import CORE_EMAIL
from puding.constants import URL
from puding.constants import LICENSE_NAME

def convertQtFiles(file_list):
    qm_dir = os.path.join("build", "qm")
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
            os.system("/usr/bin/lrelease %s -qm build/qm/%s" % (i, file_name.replace(".ts", ".qm")))

def createMoFiles():
    mo_dir = os.path.join("build", "mo")
    if not os.path.exists(mo_dir):
        os.makedirs(mo_dir)

    po_list = glob.glob("translations/po/*.po")
    data_list = []
    for path in po_list:
        po_file = os.path.split(path)[-1]
        lang = po_file.split(".")[0]
        mo_file = mo_dir + "/" + lang + "/puding.mo"

        os.mkdir(mo_dir + "/" + lang + "/")
        print("generating %s" % mo_file)
        os.system("msgfmt %s -o %s" % (path, mo_file))

        data_list.append(("share/locale/%s/LC_MESSAGES" % lang, ["build/mo/%s/puding.mo" % lang]))

    return data_list

# Edit script
script = os.path.join("build", "puding")
# TODO: It will be in build process..
if not os.path.exists("build"):
    os.mkdir("build")
shutil.copyfile(os.path.join("puding", "main.py"), script)

# Convert desktop.in
os.system("intltool-merge -d po datas/puding.desktop.in datas/puding.desktop")

# Convert Qt files
qt_files = ["puding/ui/qt/icons.qrc"]
qt_files.extend(glob.glob("puding/ui/qt/ui/*.ui"))
qt_files.extend(glob.glob("translations/ts/*.ts"))
convertQtFiles(qt_files)

data = [
    ("share/doc/puding", ["AUTHORS", "ChangeLog", "COPYING", "NOTES", "README", "TODO"]),
    ("share/puding", glob.glob("datas/syslinux.cfg.*")),
    ("share/puding/qm", glob.glob("build/qm/puding*.qm")),
    ("share/applications", ["datas/puding.desktop"]),
    ("share/puding/gfxtheme", glob.glob("datas/gfxtheme/*")),
    ("share/pixmaps", ["images/puding.png"])]

data.extend(createMoFiles())

setup(
    name = "puding",
    version = VERSION,
    description = DESCRIPTION,
    author = CORE_DEVELOPER,
    author_email = CORE_EMAIL,
    url = URL,
    license = LICENSE_NAME,
    packages = ["puding", "puding.ui", "puding.ui.cmd", "puding.ui.qt"],
    scripts = [script],
    data_files = data,
    )

