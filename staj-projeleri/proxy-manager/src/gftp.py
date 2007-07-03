# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from module import Module

class Gftp(Module):
    
    def __init__(self):
        # FIXME: find paths automatically
        self.path = "config_files/gftprc"
        # keys of the config file
        self.http = "http_proxy_host"
        self.httpPort = "http_proxy_port"
        self.ftp = "ftp_proxy_host"
        self.ftpPort = "ftp_proxy_port"
        
        if os.path.exists(self.path):
            confRead = open(self.path, "r")
            self.lines = confRead.readlines()
            confRead.close()
        else:
            self.lines = []
        
        i = self.hi = self.hpi = self.fi = self.fpi = 0
        while len(self.lines) != i:
            if not self.fi and self.lines[i].find(self.ftp) != -1: self.fi = i
            elif not self.fpi and self.lines[i].find(self.ftpPort) != -1: self.fpi = i
            elif not self.hi and self.lines[i].find(self.http) != -1: self.hi = i
            elif not self.hpi and self.lines[i].find(self.httpPort) != -1: self.hpi = i
            i = i + 1
        if not self.fi:
            self.lines.append(self.ftp + "=")
            self.fi = len(self.lines) - 1
        if not self.fpi:
            self.lines.append(self.ftpPort + "=")
            self.fpi = len(self.lines) - 1
        if not self.hi:
            self.lines.append(self.http + "=")
            self.hi = len(self.lines) - 1
        if not self.hpi:
            self.lines.append(self.httpPort + "=")
            self.hpi = len(self.lines) - 1
        
    def setGlobalProxy(self, ip, port=None):
        if not port: value = "=\n"
        else: value = "=" + port + "\n"
        self.lines[self.fi] = self.ftp + "=" + ip + "\n"
        self.lines[self.fpi] = self.ftpPort + value
        self.lines[self.hi] = self.http + "=" + ip + "\n"
        self.lines[self.hpi] = self.httpPort + value
        
    def setHTTPProxy(self, ip, port=None):
        if not port: self.lines[self.hpi] = self.httpPort + "=\n"
        else: self.lines[self.hpi] = self.httpPort + "=" + port + "\n"
        self.lines[self.hi] = self.http + "=" + ip + "\n"

    def setFTPProxy(self, ip, port=None):
        if not port: self.lines[self.fpi] = self.ftpPort + "=\n"
        else: self.lines[self.fpi] = self.ftpPort + "=" + port + "\n"
        self.lines[self.fi] = self.ftp + "=" + ip + "\n"

    def noProxy(self):
        self.setGlobalProxy("", "")
    
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
a = Gftp()
a.setGlobalProxy("123.321.123.312", "1122")
a.setFTPProxy("123.321.123.333", "ftp")
a.setHTTPProxy("123.321.123.444", "http")
a.close()
print time()
