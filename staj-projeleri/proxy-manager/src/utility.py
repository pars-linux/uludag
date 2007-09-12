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
    """Import modules if they are necessary. For some modules the file that it
    modifies must exist, but for some the file must be created by the module itself.
    So, below there are some checks to determine whether the module must be imported,
    or not."""
    
    pisi.api.init(write=False)
    installed = pisi.api.list_installed()
    home_dir = os.path.expanduser("~/")
    
    # kdebase must be installed, hopefully, no need to check.
    from apps.kde import KDE
    modules.append(KDE())
    if os.path.exists(home_dir + ".mozilla/firefox") or os.path.exists(home_dir + ".thunderbird"):
        from apps.mozilla import Mozilla
        if os.path.exists(home_dir + ".mozilla/firefox"):
            modules.append(Mozilla(home_dir + ".mozilla/firefox/"))
        if os.path.exists(home_dir + ".thunderbird"):
            modules.append(Mozilla(home_dir + ".thunderbird/"))
    if os.path.exists(home_dir + ".amsn/config.xml"):
        from apps.amsn import AMSN
        modules.append(AMSN())
    if "aria2" in installed:
        from apps.aria2 import Aria2
        modules.append(Aria2())
    if "gftp" in installed:
        from apps.gftp import Gftp
        modules.append(Gftp())
    if "pidgin" in installed and os.path.exists(home_dir + ".purple/prefs.xml"):
        from apps.pidgin import Pidgin
        modules.append(Pidgin())
    if "subversion" in installed and os.path.exists(home_dir + ".subversion/servers"):
        from apps.svn import Svn
        modules.append(Svn())
    if "wget" in installed:
        from apps.wget import Wget
        modules.append(Wget())


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
