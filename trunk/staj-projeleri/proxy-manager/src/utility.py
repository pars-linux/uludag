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

import ConfigParser

import pisi

configDir = os.path.expanduser("~/.proxy/")
configPath = configDir +"proxy"
config = ConfigParser.SafeConfigParser()
modules = []

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def parseConfig():
    if not os.path.exists(configDir):
        os.mkdir(configDir)
    config.read(configPath)
    noProxy = "noproxy"
    if not config.has_section(noProxy):
        config.add_section(noProxy)
    if not config.has_option(noProxy,"isActive"):
        config.set(noProxy,"isActive","1")
    config.set(noProxy, "type", "0")

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
        

def changeProxy(section):
    type = config.getint(section,"type")
    if type == 0:
        for m in modules:
            m.noProxy()
    elif type == 1:
        for m in modules:
            if config.has_option(section,"http_port"):
                m.setGlobalProxy(config.get(section,"http_host"), config.get(section,"http_port"))
            else:
                m.setGlobalProxy(config.get(section,"http_host"))
    elif type == 2:
        for m in modules:
            if config.has_option(section,"http_host"):
                if config.has_option(section,"http_port"):
                    m.setHTTPProxy(config.get(section,"http_host"), config.get(section,"http_port"))
                else:
                    m.setHTTPProxy(config.get(section,"http_host"))
            if config.has_option(section,"ftp_host"):
                if config.has_option(section,"ftp_port"):
                    m.setFTPProxy(config.get(section,"ftp_host"), config.get(section,"ftp_port"))
                else:
                    m.setFTPProxy(config.get(section,"ftp_host"))
            if config.has_option(section,"gopher_host"):
                if config.has_option(section,"gopher_port"):
                    m.setGopherProxy(config.get(section,"gopher_host"), config.get(section,"gopher_port"))
                else:
                    m.setGopherProxy(config.get(section,"gopher_host"))
            if config.has_option(section,"ssl_host"):
                if config.has_option(section,"ssl_port"):
                    m.setSSLProxy(config.get(section,"ssl_host"), config.get(section,"ssl_port"))
                else:
                    m.setSSLProxy(config.get(section,"ssl_host"))
            if config.has_option(section,"socks_host"):
                if config.has_option(section,"socks_port"):
                    m.setSOCKSProxy(config.get(section,"socks_host"), config.get(section,"socks_port"))
                else:
                    m.setSOCKSProxy(config.get(section,"socks_host"))
    elif type == 3:
        for m in modules:
            m.setPAC_URL(config.get(section,"auto_url"))
        
    for m in modules:
        m.close()
    for s in config.sections():
        config.set(s,"isActive","0")
    config.set(section,"isActive","1")
    f = open(configPath,"w")
    config.write(f)
    f.close()
