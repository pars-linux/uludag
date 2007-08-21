#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from qt import *
from kdecore import *

import os

import pisi
import profile

profiles = []
modules = []

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def initProfiles():
    profiles[0:] = profile.parseConfig()

def createModules():
    home_dir = os.path.expanduser("~/")
    if "firefox" in installed or "thunderbird" in installed:
        from apps.mozilla import Mozilla
        if os.exists(home_dir + ".mozilla/firefox"):
            modules.append(Mozilla(home_dir + ".mozilla/firefox/"))
        if os.exists(home_dir + ".thunderbird"):
            modules.append(Mozilla(home_dir + ".thunderbird/"))
    if "amsn" in installed and os.exists(home_dir + ".amsn/config.xml"):
        from apps.amsn import AMSN
        modules.append(AMSN())
    if "aria2" in installed:
        from apps.aria2 import Aria2
        modules.append(Aria2())
    if "kdebase" in installed:
        from apps.kde import KDE
        modules.append(KDE())
    if "gftp" in installed:
        from apps.gftp import Gftp
        modules.append(Gftp())
    if "pidgin" in installed and os.exists(home_dir + ".purple/prefs.xml"):
        from apps.pidgin import Pidgin
        modules.append(Pidgin())
        

def changeProxy(prfl):
    if prfl.type == profile.direct:
        for m in modules:
            m.noProxy()
    elif prfl.type == profile.globl:
        for m in modules:
            m.setGlobalProxy(prfl.globl_host, prfl.globl_port)
    elif prfl.type == profile.indiv:
        for m in modules:
            if prfl.has_http:
                m.setHTTPProxy(prfl.http_host, prfl.http_port)
            if prfl.has_ftp:
                m.setFTPProxy(prfl.ftp_host, prfl.ftp_port)
            if prfl.has_ssl:
                m.setSSLProxy(prfl.ssl_host, prfl.ssl_port)
            if prfl.has_socks:
                m.setSOCKSProxy(prfl.socks_host, prfl.socks_port)
    elif prfl.type == profile.auto:
        for m in modules:
            m.setPAC_URL(prfl.auto_url)
        
    for m in modules:
        m.close()
        
    for p in profiles:
        p.isActive = False
    prfl.isActive = True
    
    profile.save()
