#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os
import shutil

# KDE Modules
from PyKDE4.kdecore import i18n
from migration.gui import context as ctx

ignoreList = ["desktop.ini", "thumbs.db", "$Recycled.Bin"]


def totalSize(fileList):
    "calculates total size of a list which includes files and dirs"
    size = 0
    for item in fileList:
        if os.path.basename(item) in ignoreList:
            continue
        if os.path.isfile(item):
            size += os.path.getsize(item)
        elif os.path.isdir(item):
            size += totalSize(map(lambda x: os.path.join(item, x), os.listdir(item)))
    return size


def base(path):
    "returns closest existent parent"
    if not os.path.exists(path):
        return base(os.path.dirname(path))
    return path


def freeSpace(path):
    "returns available disk space for a given path"
    stat = os.statvfs(base(path))
    return stat.f_bavail * stat.f_bsize

def findName(path):
    "Find a unique filename using path. If there are no file in path, don't change it."
    if not os.path.lexists(path):
        return (path)
    base, ext = os.path.splitext(path)
    middle = 1
    while os.path.lexists(base + "_" + str(middle) + ext):
        middle += 1
    return (base + "_" + str(middle) + ext)

desktopdata = """
[Desktop Entry]
Encoding=UTF-8
Name=%s
Icon=%s
Type=Link
URL=%s
"""

directorydata = """
[Desktop Entry]
Icon=%s
"""

icons = {"My Documents":"folder",
         "Desktop":"desktop",
         "My Music":"folder_sound",
         "My Pictures":"folder_image",
         "My Video":"folder_video"}

def createLink(link):
    "puts a link to the desktop"
    dest = os.path.join(os.path.expanduser("~/Desktop/%s.desktop" % link["localname"]))
    dest = findName(dest)
    desktopfile = open(dest, "w")
    desktopfile.write(desktopdata % (link["name"], icons[link["name"]], link["path"]))
    desktopfile.close()

def copyFolder(folder, destination, progress):
    "copies a root folder to destination and updates progress"
    # assume destination folder exists
    # Make directory:
    path = os.path.join(destination, folder["localname"])
    path = findName(path)
    os.mkdir(path)
    # Change icon:
    directoryfile = open(os.path.join(path, ".directory"), "w")
    directoryfile.write(directorydata % icons[folder["name"]])
    directoryfile.close()
    # Copy item:
    for item in folder["files"]:
        dst = item.replace(folder["source"], path)
        copyItem(item, dst, progress)

def copyItem(src, dst, progress):
    basename = os.path.basename(dst)
    dirname = os.path.dirname(dst)
    if basename in ignoreList:
        return
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if os.path.isfile(src):
        try:
            shutil.copy2(src, dst)
        except:
            progress.go(unicode(i18n("file '%s' cannot be copied")) % unicode(src), ctx.WARNING, os.path.getsize(src))
        else:
            progress.go(unicode(i18n("file '%s' copied")) % unicode(src), ctx.OK, os.path.getsize(src))
    elif os.path.isdir(src):
        if not os.path.exists(dst):
            os.makedirs(dst)
        files = os.listdir(src)
        for item in files:
            newdst = os.path.join(dst, item)
            newsrc = os.path.join(src, item)
            copyItem(newsrc, newdst, progress)
