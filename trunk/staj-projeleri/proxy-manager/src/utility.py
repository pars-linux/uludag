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

import ConfigParser

import pisi

programs = None
config = ConfigParser.SafeConfigParser()
configPath = "config_files/config"
modules = []

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

def parseConfig():
    # FIXME: use a variable for "home" path
    config.read(configPath)

def createModules():
    pisi.api.init(write=False)
    installed = pisi.api.list_installed()
    if "firefox" in installed:
        from firefox import Firefox
        modules.append(Firefox())
    if "amsn" in installed:
        from amsn import AMSN
        modules.append(AMSN())
        # FIXME: uncomment
##    if "aria2" in installed:
    if True:
        from aria2 import Aria2
        modules.append(Aria2())
    if "kdebase" in installed:
        from kde import KDE
        modules.append(KDE())
    if "gftp" in installed:
        global Gftp
        from gftp import Gftp
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
    # FIXME: "or type == 3" maybe added later
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
        
    for m in modules:
        m.close()
    for s in config.sections():
        config.set(s,"isActive","0")
    config.set(section,"isActive","1")
    f = open(configPath,"w")
    config.write(f)
    f.close()
