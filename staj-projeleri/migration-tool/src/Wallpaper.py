#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import shutil
import tempfile
import ConfigParser

from dcopext import DCOPClient, DCOPObj

import registry

class WallpaperError(Exception):
    pass

def winPath(currentdir, path):
    pathlist = path.split("/",1)
    files = os.listdir(currentdir)
    for thefile in files:
        if thefile.lower() == pathlist[0].lower():
            if len(pathlist) > 1:
                if pathlist[1] == "":
                    return os.path.join(currentdir, thefile)
                else:
                    return winPath(os.path.join(currentdir, thefile), pathlist[1])
            else:
                return os.path.join(currentdir, thefile)
    return None

def getKDEWallpaperPath():
    parser = ConfigParser.ConfigParser()
    parser.readfp(open(os.path.expanduser("~/.kde/share/config/kdesktoprc")))
    wallpaper = parser.get("Desktop0", "Wallpaper")
    wallpaper = wallpaper.replace("$HOME", os.path.expanduser("~"))
    if os.path.isfile(wallpaper):
        return wallpaper
    else:
        raise WallpaperError, "KDE wallpaper cannot be found"

def getWindowsWallpaperPath(partition, hive):
    key = hive.getKey("Control Panel\\Desktop")
    values = key.valueDict()
    if values.has_key("Wallpaper"):     # Windows XP
        value = values["Wallpaper"]
    elif values.has_key("WallPaper"):   # Windows Vista
        value = values["WallPaper"]
    else:
        raise WallpaperError, "Windows wallpaper cannot be found"
    if value.find("C:\\") != -1:
        value = value.replace("C:\\", "")
        value = value.replace("\\", "/")
        value = winPath(partition, value)
        if value:
            return value
    raise WallpaperError, "Windows wallpaper cannot be found"

def getThumbnail(oldfile, width=100, height=100):
    newfile = tempfile.mktemp(".jpg")
    command = "convert '" + oldfile + "' -resize 100x100 '" + newfile + "'"
    os.system(command)
    return newfile

def changeWallpaper(path):
    # Copy file to wallpapers dir:
    newpath = os.path.join(os.path.expanduser("~/.kde/share/wallpapers"), os.path.basename(path))
    shutil.copyfile(path, newpath)
    # Create a dcop object:
    client = DCOPClient()
    if not client.attach():
        raise WallpaperError, "Wallpaper cannot be changed"
    # Set Wallpaper:
    background = DCOPObj("kdesktop", client, "KBackgroundIface")
    ok, wallpaper = background.setWallpaper(newpath, 6)     # 6: Scaled
    if ok:
        return True
    else:
        raise WallpaperError, "Wallpaper cannot be changed"
