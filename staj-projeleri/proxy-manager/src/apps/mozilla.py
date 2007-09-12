# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from app import App
import ConfigParser    

class Mozilla(App):
    def __init__(self, configdir):
        # Finds the path of the config file
        # NOTE: this is for default profile only.
        self.configdir = configdir
        config = ConfigParser.SafeConfigParser()
        config.read(self.configdir + "profiles.ini")
        self.path = self.configdir + config.get("Profile0", "Path") + "/user.js"
        # keys of the config file
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
        self.autoconfig_url = "network.proxy.autoconfig_url"
        self.type = "network.proxy.type"
        self.share = "network.proxy.share_proxy_settings"
        self.start = "user_pref(\""
        self.end = "\", "");\n"
        
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
        # indexes to determine where the corresponding line is
        hi = hpi = fi = fpi = gi = gpi = ai = -1
        si = spi = soi = sopi = ti = shi = -1
        
        while len(self.conf_lines) != i:
            if len(self.conf_lines[i]) == 0 or self.conf_lines[i][0] == ("#" or "\n"): pass
            elif hi == -1 and self.conf_lines[i].find(self.http) != -1: hi = i
            elif hpi == -1 and self.conf_lines[i].find(self.http_port) != -1: hpi = i
            elif fi == -1 and self.conf_lines[i].find(self.ftp) != -1: fi = i
            elif fpi == -1 and self.conf_lines[i].find(self.ftp_port) != -1: fpi = i
            elif gi == -1 and self.conf_lines[i].find(self.gopher) != -1: gi = i
            elif gpi == -1 and self.conf_lines[i].find(self.gopher_port) != -1: gpi = i
            elif si == -1 and self.conf_lines[i].find(self.ssl) != -1: si = i
            elif spi == -1 and self.conf_lines[i].find(self.ssl_port) != -1: spi = i
            elif soi == -1 and self.conf_lines[i].find(self.socks) != -1: soi = i
            elif sopi == -1 and self.conf_lines[i].find(self.socks_port) != -1: sopi = i
            elif ai == -1 and self.conf_lines[i].find(self.autoconfig_url) != -1: ai = i
            elif ti == -1 and self.conf_lines[i].find(self.type) != -1: ti = i
            elif shi == -1 and self.conf_lines[i].find(self.share) != -1: shi = i
            i = i + 1
        indexes = [hi, hpi, fi, fpi, gi, gpi ,ai, si, spi, soi, sopi, ti, shi]
        indexes.sort()
        indexes.reverse()
        for i in indexes:
            if i != -1: del self.conf_lines[i]
        
    
    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        if not port: port = "0"
        del self.lines[:]
        self.lines.append(self.start + self.http + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.ftp + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.gopher + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.ssl + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.socks + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.http_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.ftp_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.gopher_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.ssl_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.socks_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.type + "\", 1);\n")
        self.lines.append(self.start + self.share + "\", true);\n")
        
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        if not port: port = "0"
        del self.lines[:]
        self.lines.append(self.start + self.http + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.http_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.type + "\", 1);\n")
        self.lines.append(self.start + self.share + "\", false);\n")
        
    def setFTPProxy(self, ip, port=None, user=None, pasw=None):
        if not port: port = "0"
        del self.lines[:]
        self.lines.append( self.start + self.ftp + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.ftp_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.type + "\", 1);\n")
        self.lines.append(self.start + self.share + "\", false);\n")
        
    def setGopherProxy(self, ip, port=None, user=None, pasw=None):
        if not port: port = "0"
        del self.lines[:]
        self.lines.append(self.start + self.gopher + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.gopher_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.type + "\", 1);\n")
        self.lines.append(self.start + self.share + "\", false);\n")
        
    def setSSLProxy(self, ip, port=None, user=None, pasw=None):
        if not port: port = "0"
        del self.lines[:]
        self.lines.append(self.start + self.ssl + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.ssl_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.type + "\", 1);\n")
        self.lines.append(self.start + self.share + "\", false);\n")
        
    def setSOCKSProxy(self, ip, port=None, user=None, pasw=None):
        if not port: port = "0"
        del self.lines[:]
        self.lines.append(self.start + self.socks + "\", \"" + ip + "\");\n")
        self.lines.append(self.start + self.socks_port + "\", " + port + ");\n")
        self.lines.append(self.start + self.type + "\", 1);\n")
        self.lines.append(self.start + self.share + "\", false);\n")
        
    def setPAC_URL(self, url):
        del self.lines[:]
        self.lines.append(self.start + self.autoconfig_url + "\", \"" + url + "\");\n")
        self.lines.append(self.start + self.type + "\", 2);\n")
        self.lines.append(self.start + self.share + "\", false);\n")
        
    def noProxy(self):
        del self.lines[:]
        self.lines.append("user_pref(\"network.proxy.type\", 0);" + "\n")
    
    def close(self):
        self.clean()
        self.conf_lines[len(self.conf_lines):] = self.lines
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()


### FIXME: test kodunu sil
##from time import *
##print time()
##a = Mozilla("/home/bertan/.mozilla/firefox/")
##a.setGlobalProxy("192.223.211.123")
##a.setHTTPProxy("122.311.11.11")
##a.setFTPProxy("122.311.11.11", "123")
##a.setGopherProxy("122.311.11.11", "123")
##a.setSSLProxy("122.311.11.11", "123")
##a.setSOCKSProxy("122.311.11.11", "123")
##a.noProxy()
##a.close()
##print time()
