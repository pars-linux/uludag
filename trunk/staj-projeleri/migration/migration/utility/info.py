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
import ConfigParser

import registry
import wall

def userInfo(sources):
    "Collects information from given user"
    if sources.has_key("OS Type"):
        if sources["OS Type"] in ["Windows XP", "Windows Vista"]:
            return windowsInfo(sources)

def localInfo():
    "Collects information from Pardus"
    home = os.path.expanduser("~")
    destinations = {"Home Path":home}
    # Find user wallpaper:
    wallpaper = wall.getKDEWallpaper()
    if wallpaper:
        destinations["Wallpaper Path"] = wallpaper
    # Firefox:
    profilepath = getMozillaProfile(os.path.expanduser("~/.mozilla/firefox/"))
    if profilepath:
        destinations["Firefox Profile Path"] = profilepath
    # Return Info:
    return destinations

def windowsInfo(sources):
    "Collects information from a windows user"
    # Find user directories using registry:
    try:
        hive = registry.Hive(os.path.join(sources["Home Path"], "NTUSER.DAT"))
        key = hive.getKey("Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders")
    except:
        return sources
    valuedict = key.valueDict()
    for field, value in valuedict.iteritems():
        if field in ["AppData", "Cache", "Cookies", "Desktop", "Favorites", "Fonts",
                        "History", "My Music", "My Pictures", "My Video", "Personal"]:
            if value.find("C:\\") != -1:
                value = value.replace("C:\\", "")
                value = value.replace("\\", "/")
                value = os.path.join(sources["Partition"], value)
                if os.path.isdir(value):
                    sources["%s Path" % field] = value
    # Find user wallpaper:
    wallpaper = wall.getWindowsWallpaper(sources["Partition"], hive)
    if wallpaper:
        sources["Wallpaper Path"] = wallpaper
    # Firefox:
    possiblepath = os.path.join(sources["AppData Path"], "Mozilla/Firefox")
    profilepath = getMozillaProfile(possiblepath)
    if profilepath:
        sources["Firefox Profile Path"] = profilepath
    # Thunderbird:
    possiblepath = os.path.join(sources["AppData Path"], "Thunderbird")
    profilepath = getMozillaProfile(possiblepath)
    if profilepath:
        sources["Thunderbird Profile Path"] = profilepath
    # Messenger Contacts:
    possiblepath = os.path.join(sources["Home Path"], "Contacts")
    if os.path.isdir(possiblepath):
        sources["Contacts Path"] = possiblepath
    # Google Talk:
    try:
        key = hive.getKey("Software\\Google\\Google Talk")
        sources["GTalk Key"] = key
    except:
        pass
    # Return Info:
    return sources

def getMozillaProfile(path):
    "Returns default mozilla profile path using a mozilla installation path"
    parser = ConfigParser.ConfigParser()
    inifile = os.path.join(path, "profiles.ini")
    try:
        parser.readfp(open(inifile))
    except:
        return None
    # Find Default Profile:
    profilename = ""
    if parser.has_section("Profile1"):
        sections = parser.sections()
        for section in sections:
            if parser.has_option(section, "Default") and parser.get(section, "Default"):
                profilename = section
                break
    else:
        if parser.has_section("Profile0"):
            profilename = "Profile0"
    if not profilename:
        return None
    # Get Profile Path:
    if parser.has_option(profilename, "Path"):
        if parser.has_option(profilename, "IsRelative") and parser.get(profilename, "IsRelative"):
            possibledir = os.path.join(path, parser.get(profilename, "Path"))
            if os.path.isdir(possibledir):
                return possibledir      # Relative Path
        else:
            return parser.get(profilename, "Path")      # Absolute Path
    return None
