# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
from app import App

class Aria2(App):
    def __init__(self):
        self.dir = os.path.expanduser("~/.aria2/")
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.path = self.dir + "aria2.conf"
        # open for writing, so the file will be created if it doesn't exist already
        confRead = open(self.path, "w+")
        self.lines = confRead.readlines()
        confRead.close()
        
        i = 0
        self.hi = -1
        while len(self.lines) != i and self.hi == -1:
            if self.lines[i].find("http-proxy") != -1:
                self.hi = i
            i += 1
        if self.hi == -1:
            self.lines.append("\n")
            self.hi = len(self.lines) - 1
    
    def setGlobalProxy(self, ip, port=None):
        self.setHTTPProxy(ip, port)

    def setHTTPProxy(self, ip, port=None):
        proxy = "http-proxy = " + ip
        if port: proxy += ":" + port
        else: proxy += ":3128"
        proxy += "\n"
        self.lines[self.hi] = proxy
    
    def noProxy(self):
        self.lines[self.hi] = ""
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()
    

### FIXME: test kodunu sil
##from time import *
##print time()
##a = Aria2()
##a.setGlobalProxy("192.223.211.123")
##a.close()
##print time() 
