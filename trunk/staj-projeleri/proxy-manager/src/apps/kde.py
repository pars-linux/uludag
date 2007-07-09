# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from app import App

class KDE(App):
    def __init__(self):
        self.path = os.path.expanduser("~/.kde/share/config/kioslaverc")
        # keys of the config file
        self.https = "httpsProxy"
        self.http = "httpProxy"
        self.ftp = "ftpProxy"
        self.type = "ProxyType"
        
        if os.path.exists(self.path):
            confRead = open(self.path, "r")
            self.lines = confRead.readlines()
            confRead.close()
        else:
            self.lines = []
        
        i = 0
        self.hsi = self.hi = self.fi = self.ti = -1
        while len(self.lines) != i:
            if self.ti == -1 and self.lines[i].find(self.type) != -1: self.ti = i
            elif self.fi == -1 and self.lines[i].find(self.ftp) != -1: self.fi = i
            elif self.hi == -1 and self.lines[i].find(self.http) != -1: self.hi = i
            elif self.hsi == -1 and self.lines[i].find(self.https) != -1: self.hsi = i
            i = i + 1
        if self.hsi == -1:
            self.lines.append(self.https + "=")
            self.hsi = len(self.lines) - 1
        if self.hi == -1:
            self.lines.append(self.http + "=")
            self.hi = len(self.lines) - 1
        if self.fi == -1:
            self.lines.append(self.ftp + "=")
            self.fi = len(self.lines) - 1
        if self.ti == -1:
            self.lines.append(self.type + "=")
            self.ti = len(self.lines) - 1

    def setGlobalProxy(self, ip, port=None):
        self.setHTTPProxy(ip, port)
        self.setHTTPSProxy(ip, port)
        self.setFTPProxy(ip, port)

    def setHTTPProxy(self, ip, port=None):
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.lines[self.hi] = self.http + value
        self.lines[self.ti] = self.type + "=1" + "\n"

    def setHTTPSProxy(self, ip, port=None):
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.lines[self.hsi] = self.https + value
        self.lines[self.ti] = self.type + "=1" + "\n"

    def setFTPProxy(self, ip, port=None):
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.lines[self.fi] = self.ftp + value
        self.lines[self.ti] = self.type + "=1" + "\n"

    def noProxy(self):
        self.lines[self.ti] = self.type + "=0" + "\n"
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()

### FIXME: test kodunu sil
##from time import *
##print time()
##a = KDE()
##a.setGlobalProxy("192.168.3.248", "4444")
##a.close()
##print time()
