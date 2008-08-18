# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from app import App

class Wget(App):
    
    def __init__(self):
        self.path = os.path.expanduser("~/.wgetrc")
        # keys of the config file
        self.http = "http_proxy"
        self.ftp = "ftp_proxy"
        self.user = "proxy_user"
        self.passwd = "proxy_passwd"
        self.active = "use_proxy" # value will be 1 or 0
        
        if os.path.exists(self.path):
            confRead = open(self.path, "r")
            self.conf_lines = confRead.readlines()
            confRead.close()
        else:
            self.conf_lines = []
        
        self.clean()
        self.lines = []
    
    def clean(self):
        i = 0
        hi = fi = ui = pi = ai = -1
        while len(self.conf_lines) != i:
            if len(self.conf_lines[i]) == 0 or self.conf_lines[i][0] == ("#" or "\n"): pass
            elif hi == -1 and self.conf_lines[i].find(self.http) != -1: hi = i
            elif fi == -1 and self.conf_lines[i].find(self.ftp) != -1: fi = i
            elif ui == -1 and self.conf_lines[i].find(self.user) != -1: ui = i
            elif pi == -1 and self.conf_lines[i].find(self.passwd) != -1: pi = i
            elif ai == -1 and self.conf_lines[i].find(self.active) != -1: ai = i
            i = i + 1
        indexes = [hi, fi, ui, pi,ai]
        indexes.sort()
        indexes.reverse()
        for i in indexes:
            if i != -1: del self.conf_lines[i]
        
        if hi == -1:
            self.conf_lines.append(self.http + "=")
            hi = len(self.conf_lines) - 1
        if fi == -1:
            self.conf_lines.append(self.ftp + "=")
            fi = len(self.conf_lines) - 1
        if ui == -1:
            self.conf_lines.append(self.user + "=")
            ui = len(self.conf_lines) - 1
        if pi == -1:
            self.conf_lines.append(self.passwd + "=")
            pi = len(self.conf_lines) - 1
        if ai == -1:
            self.conf_lines.append(self.active + "=")
            ai = len(self.conf_lines) - 1        

    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        del self.lines[:]
        if not port:
            self.lines.append(self.http + " = " + ip + "\n")
            self.lines.append(self.ftp + " = " + ip + "\n")
        else:
            self.lines.append(self.http + " = " + ip + ":" + port + "\n")
            self.lines.append(self.ftp + " = " + ip + ":" + port + "\n")
        self.lines.append(self.active + " = 1" + "\n")
        
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        del self.lines[:]
        if not port: self.lines.append(self.http + " = " + ip + "\n")
        else: self.lines.append(self.http + " = " + ip + ":" + port + "\n")
        self.lines.append(self.active + " = 1" + "\n")

    def setFTPProxy(self, ip, port=None, user=None, pasw=None):
        del self.lines[:]
        if not port: self.lines.append(self.ftp + " = " + ip + "\n")
        else: self.lines.append(self.ftp + " = " + ip + ":" + port + "\n")
        self.lines.append(self.active + " = 1" + "\n")

    def noProxy(self):
        del self.lines[:]
        self.lines.append(self.active + " = 0" + "\n")
    
    def close(self):
        self.clean()
        self.conf_lines[len(self.conf_lines):] = self.lines
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()
