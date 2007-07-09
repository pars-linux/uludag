# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os

from app import App
import ConfigParser

ffpath = os.path.expanduser("~/.mozilla/firefox/")
tbpath = os.path.expanduser("~/.thunderbird/")

# Determine if the app has a directory inside 'home' of the user
# FIXME: this can be a part of 'apps' class
def isUsed(app="firefox"):
    if (app == "firefox" and not os.path.exists(ffpath)) or (app == "thunderbird" and not os.path.exists(tbpath)):
        return False
    else:
        return True
    

class Mozilla(App):
    def __init__(self, app="firefox"):
        # Finds the path of the config file
        # NOTE: this is for default profile only.
        config = ConfigParser.SafeConfigParser()
        if app == "firefox":
            self.configdir = ffpath
        if app == "thunderbird":
            self.configdir = tbpath
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
            self.lines = confRead.readlines()
            confRead.close()
        else:
            self.lines = []
        
        i = 0
        # indexes to determine where the corresponding line is
        hi = hpi = fi = fpi = gi = gpi = self.ai = -1
        si = spi = soi = sopi = self.ti = self.shi = -1
        
        while len(self.lines) != i:
            if hi == -1 and self.lines[i].find(self.http) != -1: hi = i
            elif hpi == -1 and self.lines[i].find(self.http_port) != -1: hpi = i
            elif fi == -1 and self.lines[i].find(self.ftp) != -1: fi = i
            elif fpi == -1 and self.lines[i].find(self.ftp_port) != -1: fpi= i
            elif gi == -1 and self.lines[i].find(self.gopher) != -1: gi = i
            elif gpi == -1 and self.lines[i].find(self.gopher_port) != -1: gpi = i
            elif si == -1 and self.lines[i].find(self.ssl) != -1: si = i
            elif spi == -1 and self.lines[i].find(self.ssl_port) != -1: spi = i
            elif soi == -1 and self.lines[i].find(self.socks) != -1: soi = i
            elif sopi == -1 and self.lines[i].find(self.socks_port) != -1: sopi = i
            elif self.ai == -1 and self.lines[i].find(self.autoconfig_url) != -1: self.ai = i
            elif self.ti == -1 and self.lines[i].find(self.type) != -1: self.ti = i
            elif self.shi == -1 and self.lines[i].find(self.share) != -1: self.shi = i
            i = i + 1
        # if lines are not found, then add them
        if hi == -1: 
            self.lines.append(self.start + self.http + self.end)
            hi = len(self.lines) - 1
        if hpi == -1:
            self.lines.append(self.start + self.http_port + self.end)
            hpi = len(self.lines) - 1
        if fi == -1:
            self.lines.append(self.start + self.ftp + self.end)
            fi = len(self.lines) - 1
        if fpi == -1:
            self.lines.append(self.start + self.ftp_port + self.end)
            fpi = len(self.lines) - 1
        if gi == -1:
            self.lines.append(self.start + self.gopher + self.end)
            gi = len(self.lines) - 1
        if gpi == -1:
            self.lines.append(self.start + self.gopher_port + self.end)
            gpi = len(self.lines) - 1
        if si == -1:
            self.lines.append(self.start + self.ssl + self.end)
            si = len(self.lines) - 1
        if spi == -1:
            self.lines.append(self.start + self.ssl_port + self.end)
            spi = len(self.lines) - 1
        if soi == -1:
            self.lines.append(self.start + self.socks + self.end)
            soi = len(self.lines) - 1
        if sopi == -1:
            self.lines.append(self.start + self.socks_port + self.end)
            sopi = len(self.lines) - 1
        if self.ai == -1:
            self.lines.append(self.start + self.autoconfig_url + self.end)
            self.ai = len(self.lines) - 1
        if self.ti == -1:
            self.lines.append(self.start + self.type + "\", 0);\n")
            self.ti = len(self.lines) - 1
        if self.shi == -1:
            self.lines.append(self.start + self.share + "\", false);\n")
            self.shi = len(self.lines) - 1
        
        self.proxyIndexList = [hi, fi, gi, si, soi]
        self.portIndexList = [hpi, fpi, gpi, spi, sopi]
    
    ## a list-if system that eliminates conditions a they are met, so that performance improves?
    def setGlobalProxy(self, ip, port=None):
        if not port: port = "0"
        self.lines[self.proxyIndexList[0]]= self.start + self.http + "\", \"" + ip + "\");\n"
        self.lines[self.proxyIndexList[1]]= self.start + self.ftp + "\", \"" + ip + "\");\n"
        self.lines[self.proxyIndexList[2]]= self.start + self.gopher + "\", \"" + ip + "\");\n"
        self.lines[self.proxyIndexList[3]]= self.start + self.ssl + "\", \"" + ip + "\");\n"
        self.lines[self.proxyIndexList[4]]= self.start + self.socks + "\", \"" + ip + "\");\n"
        self.lines[self.portIndexList[0]]= self.start + self.http_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[1]]= self.start + self.ftp_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[2]]= self.start + self.gopher_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[3]]= self.start + self.ssl_port + "\", " + port + ");\n"
        self.lines[self.portIndexList[4]]= self.start + self.socks_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", true);\n"
        
    def setHTTPProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[0]]= self.start + self.http + "\", \"" + ip + "\");\n"
        self.lines[self.portIndexList[0]]= self.start + self.http_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setFTPProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[1]]= self.start + self.ftp + "\", \"" + ip + "\");\n"
        self.lines[self.portIndexList[1]]= self.start + self.ftp_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setGopherProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[2]]= self.start + self.gopher + "\", \"" + ip + "\");\n"
        self.lines[self.portIndexList[2]]= self.start + self.gopher_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setSSLProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[3]]= self.start + self.ssl + "\", \"" + ip + "\");\n"
        self.lines[self.portIndexList[3]]= self.start + self.ssl_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setSOCKSProxy(self, ip, port=None):
        self.lines[self.proxyIndexList[4]]= self.start + self.socks + "\", \"" + ip + "\");\n"
        self.lines[self.portIndexList[4]]= self.start + self.socks_port + "\", " + port + ");\n"
        self.lines[self.ti]= self.start + self.type + "\", 1);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def setPAC_URL(self, url):
        self.lines[self.ai] = self.start + self.autoconfig_url + "\", \"" + url + "\");\n"
        self.lines[self.ti]= self.start + self.type + "\", 2);\n"
        self.lines[self.shi]= self.start + self.share + "\", false);\n"
        
    def noProxy(self):
        for i in self.proxyIndexList:
            self.lines[i] = "//" + self.lines[i]
        for i in self.portIndexList:
            self.lines[i] = "//" + self.lines[i]
        self.lines[self.ti] = "user_pref(\"network.proxy.type\", 0);" + "\n"
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.writelines(self.lines)
        confWrite.close()


### FIXME: test kodunu sil
##from time import *
##print time()
##a = Firefox()
##a.setGlobalProxy("192.223.211.123")
##a.setHTTPProxy("122.311.11.11", "123")
##a.setFTPProxy("122.311.11.11", "123")
####a.setGopherProxy("122.311.11.11", "123")
####a.setSSLProxy("122.311.11.11", "123")
####a.setSOCKSProxy("122.311.11.11", "123")
##a.noProxy()
##a.close()
##print time()
