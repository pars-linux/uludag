# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from module import Module

class KDE(Module):
    
    def __init__(self):
        # FIXME: find paths automatically
        self.path = "/home/bertan/.kde3.5/share/config/kioslaverc"
        # keys of the config file
        self.https = "httpsProxy"
        self.http = "httpProxy"
        self.ftp = "ftpProxy"
        self.type = "ProxyType"
        
        if os.path.exists(self.path):
            self.confRead = open(self.path, "r")
            self.lines = self.confRead.readlines()
        else:
            self.lines = []
        for e in self.lines:
            print e,
        
        i = self.hsi = self.hi = self.fi = self.ti = 0
        while len(self.lines) != i:
            if not self.ti and self.lines[i].find(self.type) != -1: self.ti = i
            elif not self.fi and self.lines[i].find(self.ftp) != -1: self.fi = i
            elif not self.hi and self.lines[i].find(self.http) != -1: self.hi = i
            elif not self.hsi and self.lines[i].find(self.https) != -1: self.hsi = i
            i = i + 1
        if not self.hsi:
            self.lines.append(self.https + "=")
            self.hsi = len(self.lines) - 1
        if not self.hi:
            self.lines.append(self.http + "=")
            self.hi = len(self.lines) - 1
        if not self.fi:
            self.lines.append(self.ftp + "=")
            self.fi = len(self.lines) - 1
        if not self.ti:
            self.lines.append(self.type + "=")
            self.ti = len(self.lines) - 1
        
        self.confRead.close()

    def setGlobalProxy(self, ip, port=None):
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.lines[self.hsi] = self.https + value
        self.lines[self.hi] = self.http + value
        self.lines[self.fi] = self.ftp + value
        self.lines[self.ti] = self.type + "=1" + "\n"

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
        i = 0
        ## booleans to determine the values found in the file
        hFnd = hsFnd = False
        while len(self.lines) != i:
            if not hFnd and self.lines[i].find(self.type) != -1:
                self.lines[i] = self.http + value
                hFnd = True
            elif not hsFnd and self.lines[i].find(self.https) != -1:
                self.lines[i] = self.https + value
                hsFnd = True
            i = i + 1
        if not hFnd: self.lines.append(self.http + value)
    
    def close(self):
        for e in self.lines:
            print e,
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.flush()
        confWrite.close()

# FIXME: test kodunu sil
from time import *
print time()
a = KDE()
a.setGlobalProxy("192.168.3.248", "3128")
a.close()
print time()
