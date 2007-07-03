# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from module import Module

class Firefox(Module):

    def __init__(self):
        # FIXME: find paths automatically
        self.path = "config_files/user.js"
        self.http = "network.proxy.http"
        self.ftp = "network.proxy.ftp"
        self.gopher = "network.proxy.gopher"
        self.ssl = "network.proxy.ssl"
        self.socks = "network.proxy.socks"
        self.http_port = "network.proxy.http_port"
        self.ftp_port = "network.proxy.ftp_port"
        self.gopher_port = "network.proxy.gopher_port"
        self.ssl_port = "network.proxy.ssl_port"
        self.socks_port = "network.proxy.socks_port"
        self.type = "network.proxy.type"
        self.share = "network.proxy.share_proxy_settings"
        self.start = "user_pref(\"network.proxy."
        self.defaultProxy = "\", "");\n"
        
        if os.path.exists(self.path):
            confRead = open(self.path, "r")
            self.lines = confRead.readlines()
            confRead.close()
        else:
            self.lines = []
        
        i = 0
        # indexes to determine where the corresponding line is
        hi = hpi = fi = fpi = gi = gpi = 0
        si = spi = soi = sopi = self.ti = self.shi = 0
        
        while len(self.lines) != i:
            if not hi and self.lines[i].find(self.http) != -1: hi = i
            elif not hpi and self.lines[i].find(self.http_port) != -1: hpi = i
            elif not fi and self.lines[i].find(self.ftp) != -1: fi = i
            elif not fpi and self.lines[i].find(self.ftp_port) != -1: fpi= i
            elif not gi and self.lines[i].find(self.gopher) != -1: gi = i
            elif not gpi and self.lines[i].find(self.gopher_port) != -1: gpi = i
            elif not si and self.lines[i].find(self.ssl) != -1: si = i
            elif not spi and self.lines[i].find(self.ssl_port) != -1: spi = i
            elif not soi and self.lines[i].find(self.socks) != -1: soi = i
            elif not sopi and self.lines[i].find(self.socks_port) != -1: sopi = i
            elif not self.ti and self.lines[i].find(self.type) != -1: ti = i
            elif not self.shi and self.lines[i].find(self.share) != -1: shi = i
            i = i + 1
        # if lines are not found, then add them
        if not hi: self.lines.append(self.start + self.http + self.defaultProxy)
        if not hpi: self.lines.append(self.start + self.http_port + self.defaultProxy)
        if not fi: self.lines.append(self.start + self.ftp + self.defaultProxy)
        if not fpi: self.lines.append(self.start + self.ftp_port + self.defaultProxy)
        if not gi: self.lines.append(self.start + self.gopher + self.defaultProxy)
        if not gpi: self.lines.append(self.start + self.gopher_port + self.defaultProxy)
        if not si: self.lines.append(self.start + self.ssl + self.defaultProxy)
        if not spi: self.lines.append(self.start + self.ssl_port + self.defaultProxy)
        if not soi: self.lines.append(self.start + self.socks + self.defaultProxy)
        if not sopi: self.lines.append(self.start + self.socks_port + self.defaultProxy)
        if not self.ti: self.lines.append(self.start + self.type + self.defaultProxy)
        if not self.shi: self.lines.append(self.start + self.share + self.defaultProxy)
        
        self.proxyIndexList = [hi, fi, gi, si, soi]
        self.portIndexList = [hpi, fpi, gpi, spi, sopi]
    
    ## a list-if system that eliminates conditions a they are met, so that performance improves?
    def setGlobalProxy(self, ip, port=None):
        if not port: port = "0"
        self.lines[self.proxyIndexList[0]]= self.start + self.http + "\", " + ip + ");\n"
        self.lines[self.proxyIndexList[1]]= self.start + self.ftp + "\", " + ip + ");\n"
        self.lines[self.proxyIndexList[2]]= self.start + self.gopher + "\", " + ip + ");\n"
        self.lines[self.proxyIndexList[3]]= self.start + self.ssl + "\", " + ip + ");\n"
        self.lines[self.proxyIndexList[4]]= self.start + self.socks + "\", " + ip + ");\n"
        self.lines[self.portIndexList[0]]= self.start + self.http_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[1]]= self.start + self.ftp_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[2]]= self.start + self.gopher_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[3]]= self.start + self.ssl_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[4]]= self.start + self.socks_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", true);\n"
        
    def setHTTPProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[0]]= self.start + self.http + "\", " + ip + ");\n"
        self.lines[self.portIndexList[0]]= self.start + self.http_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setFTPProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[1]]= self.start + self.ftp + "\", " + ip + ");\n"
        self.lines[self.portIndexList[1]]= self.start + self.ftp_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setGopherProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[2]]= self.start + self.gopher + "\", " + ip + ");\n"
        self.lines[self.portIndexList[2]]= self.start + self.gopher_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setSSLProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[3]]= self.start + self.ssl + "\", " + ip + ");\n"
        self.lines[self.portIndexList[3]]= self.start + self.ssl_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setSOCKSProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[4]]= self.start + self.socks + "\", " + ip + ");\n"
        self.lines[self.portIndexList[4]]= self.start + self.socks_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def noProxy(self):
        for i in self.proxyIndexList:
            self.lines[i] = "//" + self.lines[i]
        for i in self.portIndexList:
            self.lines[i] = "//" + self.lines[i]
        self.lines[ti] = "user_pref(\"network.proxy.type\", 0);" + "\n"
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.flush()
        confWrite.close()


# FIXME: test kodunu sil
from time import *
print time()
a = Firefox()
a.setGlobalProxy("192.223.211.123")
a.setHTTPProxy("122.311.11.11", "123")
a.setFTPProxy("122.311.11.11", "123")
a.setGopherProxy("122.311.11.11", "123")
a.setSSLProxy("122.311.11.11", "123")
a.setSOCKSProxy("122.311.11.11", "123")
##a.noProxy()
a.close()
print time()
