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
import ConfigParser

from dcopext import DCOPClient, DCOPObj

import registry

class WallpaperError(Exception):
    pass

def winPath(currentdir, path):
    "Returns the case sensitive correspondent of a case insensitive path"
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

def getKDEWallpaper():
    "Returns KDE Wallpaper using kdesktoprc file"
    parser = ConfigParser.ConfigParser()
    parser.readfp(open(os.path.expanduser("~/.kde/share/config/kdesktoprc")))
    if not parser.has_option("Desktop0", "Wallpaper"):
        return None
    wallpaper = parser.get("Desktop0", "Wallpaper")
    wallpaper = wallpaper.replace("$HOME", os.path.expanduser("~"))
    if os.path.isfile(wallpaper):
        return wallpaper
    else:
        return None

def getWindowsWallpaper(partition, hive):
    "Returns windows wallpaper path using user registry hive"
    try:
        key = hive.getKey("Control Panel\\Desktop")
        values = key.valueDict()
    except:
        return None
    if values.has_key("Wallpaper"):     # Windows XP
        value = values["Wallpaper"]
    elif values.has_key("WallPaper"):   # Windows Vista
        value = values["WallPaper"]
    else:
        return None
    if value.find("C:\\") != -1:
        value = value.replace("C:\\", "")
        value = value.replace("\\", "/")
        value = winPath(partition, value)
        if value:
            return value
    return None

def setWallpaper(path):
    "Changes current wallpaper with the new one"
    # Copy file to wallpapers dir:
    wallpapersdir = os.path.expanduser("~/.kde/share/wallpapers")
    if not (os.path.isdir(wallpapersdir)):
        os.makedirs(wallpapersdir)
    newpath = os.path.join(wallpapersdir, os.path.basename(path))
    shutil.copyfile(path, newpath)
    # Create a dcop object:
    client = DCOPClient()
    if not client.attach():
        raise WallpaperError, "Wallpaper cannot be changed"
    # Set Wallpaper:
    background = DCOPObj("kdesktop", client, "KBackgroundIface")
    ok, wallpaper = background.setWallpaper(newpath, 6)     # 6: Scaled
    if not ok:
        raise WallpaperError, "Wallpaper cannot be changed"
