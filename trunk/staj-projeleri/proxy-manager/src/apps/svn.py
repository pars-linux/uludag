# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from app import App

class Svn(App):
    
    def __init__(self):
        self.path = os.path.expanduser("~/.subversion/servers")
        # keys of the config file
        self.http = ""
        self.httpPort = ""
        self.httpUser = ""
        self.httpPasw = ""
        self.HTTP = "http-proxy-host"
        self.HTTP_PORT = "http-proxy-port"
        self.HTTP_USER = "http-proxy-username"
        self.HTTP_PASW = "http-proxy-password"

    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        self.setHTTPProxy(ip, port, user, pasw)
        
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        self.http = self.HTTP + " = " + ip + "\n"
        if not port: self.httpPort = ""
        else: self.httpPort = self.HTTP_PORT + " = " + port + "\n"
        if not user: self.httpUser = ""
        else: self.httpUser = self.HTTP_USER + " = " + user + "\n"
        if not pasw: self.httpPasw = ""
        else: self.httpPasw = self.HTTP_PASW + " = " + pasw + "\n"

    def noProxy(self):
        self.http = ""
        self.httpPort = ""
        self.httpUser = ""
        self.httpPasw = ""
    
    def close(self):
        if os.path.exists(self.path):
            confRead = open(self.path, "r")
            self.lines = confRead.readlines()
            confRead.close()
        else:
            self.lines = []
        
        deleteList = []
        i = 0
        self.hi = self.hpi = self.ui = self.pi = -1
        inGlobalSection = False
        while len(self.lines) != i:
            if len(self.lines[i]) == 0 or self.lines[i][0] == "#": pass
            elif not inGlobalSection and self.lines[i].find("[global]") != -1: inGlobalSection = True
            elif inGlobalSection:
                if self.hi == -1 and self.lines[i].find(self.HTTP) != -1: self.hi = i
                elif self.hpi == -1 and self.lines[i].find(self.HTTP_PORT) != -1: self.hpi = i
                elif self.ui == -1 and self.lines[i].find(self.HTTP_USER) != -1: self.ui = i
                elif self.pi == -1 and self.lines[i].find(self.HTTP_PASW) != -1: self.pi = i
            i = i + 1
        if self.hi == -1 and len(self.http) != 0: self.lines.append(self.http)
        elif self.hi != -1:
            if len(self.http) != 0: self.lines[self.hi] = self.http
            else: deleteList.append(self.hi)
        
        if self.hpi == -1 and len(self.httpPort) != 0: self.lines.append(self.httpPort)
        elif self.hpi != -1:
            if len(self.httpPort) != 0: self.lines[self.hpi] = self.httpPort
            else: deleteList.append(self.hpi)
        
        if self.ui == -1 and len(self.httpUser) != 0: self.lines.append(self.httpUser)
        elif self.ui != -1:
            if len(self.httpUser) != 0: self.lines[self.ui] = self.httpUser
            else: deleteList.append(self.ui)
        
        if self.pi == -1 and len(self.httpPasw) != 0: self.lines.append(self.httpPasw)
        elif self.pi != -1:
            if len(self.httpUser) != 0: self.lines[self.pi] = self.httpPasw
            else: deleteList.append(self.pi)
        
        if len(deleteList) != 0:
            print deleteList
            deleteList.sort(reverse=True)
            for i in deleteList:
                del self.lines[i]
        
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()
