#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

# FIXME: clean print statements in all files

from qt import *
from kdecore import *
from khtml import *

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
    pisi.api.init(write=False)
    installed = pisi.api.list_installed()
    pisi_packages = []
    pisi_packages.append("firefox")
    pisi_packages.append("thunderbird")
    pisi_packages.append("amsn")
    pisi_packages.append("aria2")
    pisi_packages.append("kdebase")
    pisi_packages.append("gftp")
    if pisi_packages[0] in installed:
        from apps.mozilla import Mozilla, isUsed
        if isUsed(pisi_packages[0]):
            modules.append(Mozilla(pisi_packages[0]))
    if pisi_packages[1] in installed:
        from apps.mozilla import Mozilla
        if isUsed(pisi_packages[1]):
            modules.append(Mozilla(pisi_packages[1]))
    if "amsn" in installed:
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
        
    for p in profiles:
        p.isActive = False
    prfl.isActive = True
    
    for m in modules:
        m.close()
    profile.save()
