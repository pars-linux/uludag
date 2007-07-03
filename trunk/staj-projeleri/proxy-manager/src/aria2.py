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
    
    def setGlobalProxy(self, ip, port=None):
        proxy = "http-proxy = " + ip
        if port:
            proxy = proxy + ":" + port
        proxy = proxy + "\n"
        i = 0
        found = False
        while len(self.lines) != i:
            if self.lines[i].find("http-proxy") != -1:
                self.lines[i] = proxy
                found = True
            i = i + 1
        if not found:
            self.lines.append(proxy)
    
    def noProxy(self):
        i = 0
        while len(self.lines) != i:
            if self.lines[i].find("http-proxy") != -1:
                self.lines[i] = "# " + self.lines[i]
            i = i + 1
    
    def close(self):
        for a in self.lines:
            print a
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.flush()
        confWrite.close()
    

# FIXME: test kodunu sil
a = Aria2()
a.setGlobalProxy("192.223.211.123")
a.noProxy()
a.close()
 
