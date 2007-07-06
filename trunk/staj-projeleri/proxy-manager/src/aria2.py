# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from module import Module

class Aria2(Module):
    
    def __init__(self):
        # FIXME: find paths automatically
        self.path = "config_files/aria2.conf"
        confRead = open(self.path, "r")
        self.lines = confRead.readlines()
        confRead.close()
        
        i = 0
        self.hi = -1
        while len(self.lines) != i and self.hi == -1:
            if self.lines[i].find("http-proxy") != -1:
                self.hi = i
            i += 1
        if self.hi == -1:
            self.lines.append("")
            self.hi = len(self.lines) - 1
    
    def setGlobalProxy(self, ip, port=None):
        self.setHTTPProxy(ip, port)

    def setHTTPProxy(self, ip, port=None):
        proxy = "http-proxy = " + ip
        if port: proxy += ":" + port
        proxy += "\n"
        self.lines[self.hi] = proxy
    
    def noProxy(self):
        self.lines[self.hi] = ""
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()
    

# FIXME: test kodunu sil
##a = Aria2()
##a.setGlobalProxy("192.223.211.123")
##a.noProxy()
##a.close()
 
