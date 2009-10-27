# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from app import App

class Gftp(App):
    
    def __init__(self):
        self.path = os.path.expanduser("~/.gftp/gftprc")
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
        
        i = 0
        self.hi = self.hpi = self.fi = self.fpi = -1
        while len(self.lines) != i:
            if len(self.lines[i]) == 0 or self.lines[i][0] == ("#" or "\n"): pass
            elif self.fi == -1 and self.lines[i].find(self.ftp) != -1: self.fi = i
            elif self.fpi == -1 and self.lines[i].find(self.ftpPort) != -1: self.fpi = i
            elif self.hi == -1 and self.lines[i].find(self.http) != -1: self.hi = i
            elif self.hpi == -1 and self.lines[i].find(self.httpPort) != -1: self.hpi = i
            i = i + 1
        if self.fi == -1:
            self.lines.append(self.ftp + "=")
            self.fi = len(self.lines) - 1
        if self.fpi == -1:
            self.lines.append(self.ftpPort + "=")
            self.fpi = len(self.lines) - 1
        if self.hi == -1:
            self.lines.append(self.http + "=")
            self.hi = len(self.lines) - 1
        if self.hpi == -1:
            self.lines.append(self.httpPort + "=")
            self.hpi = len(self.lines) - 1
        
    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        self.setHTTPProxy(ip, port, user, pasw)
        self.setFTPProxy(ip, port, user, pasw)
        
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        if not port: self.lines[self.hpi] = self.httpPort + "=\n"
        else: self.lines[self.hpi] = self.httpPort + "=" + port + "\n"
        self.lines[self.hi] = self.http + "=" + ip + "\n"

    def setFTPProxy(self, ip, port=None, user=None, pasw=None):
        if not port: self.lines[self.fpi] = self.ftpPort + "=\n"
        else: self.lines[self.fpi] = self.ftpPort + "=" + port + "\n"
        self.lines[self.fi] = self.ftp + "=" + ip + "\n"

    def noProxy(self):
        self.setGlobalProxy("", "")
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()
