# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import re

from app import App

class KDE(App):
    def __init__(self):
        # self.path = os.path.expanduser("~/.kde/share/config/kioslaverc")
        self.path = os.path.expanduser("~/svn/pardus/proxy-manager/src/config_files/kioslaverc")
        
        # keys of the config file
        self.https = "httpsProxy"
        self.httpsRE = re.compile(self.https + "=.*?\n")
        self.http = "httpProxy"
        self.httpRE = re.compile(self.http + "=.*?\n")
        self.ftp = "ftpProxy"
        self.ftpRE = re.compile(self.ftp + "=.*?\n")
        self.autoconfig_url = "Proxy Config Script"
        self.autoconfig_urlRE = re.compile(self.autoconfig_url + "=.*?\n")
        self.type = "ProxyType"
        self.typeRE = re.compile(self.type + "=.*?\n")
        
        self.globl = False
        
        if os.path.exists(self.path):
            confRead = open(self.path, "r")
            self.text = confRead.read()
            confRead.close()
        else:
            self.text = ""
            
        if re.search("\[Proxy Settings\]", self.text) == None:
            self.text = self.text + "[Proxy Settings]\nAuthMode=0\nNoProxyFor=\nProxy Config Script=\nProxyType=\nReversedException=\nftpProxy=\nhttpProxy=\nhttpsProxy=\n"
        

    def clean(self):
        if not self.globl:
            self.text = self.autoconfig_urlRE .sub(self.autoconfig_url + "=0",self.text)
            self.text = self.httpRE.sub(self.http + "=\n", self.text)
            self.text = self.httpsRE.sub(self.https + "=\n", self.text)
            self.text = self.ftpRE.sub(self.ftp + "=\n", self.text)
    
    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        self.globl = True
        self.setHTTPProxy(ip, port, user, pasw)
        self.setHTTPSProxy(ip, port, user, pasw)
        self.setFTPProxy(ip, port, user, pasw)
        self.globl = False

    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        self.clean()
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.text = self.httpRE.sub(self.http + value, self.text)
        self.text = self.typeRE.sub(self.type + value, self.text)

    def setHTTPSProxy(self, ip, port=None, user=None, pasw=None):
        self.clean()
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.text = self.httpsRE.sub(self.https + value, self.text)
        self.text = self.typeRE.sub(self.type + "=1\n", self.text)

    def setFTPProxy(self, ip, port=None, user=None, pasw=None):
        self.clean()
        if not port: value = "=" + ip + "\n"
        else: value = "=" + ip + ":" + port + "\n"
        self.text = self.ftpRE.sub(self.ftp + value,  self.text)
        self.text = self.typeRE.sub(self.type + "=1\n", self.text)

    def setPAC_URL(self, url):
        self.text = self.autoconfig_urlRE .sub(self.autoconfig_url + "=" + url + "\n",  self.text)
        self.text = self.typeRE.sub(self.type + "=3\n", self.text)
        
    def noProxy(self):
        self.text = self.typeRE.sub(self.type + "=0\n", self.text)
    
    def close(self):
        confWrite = open(self.path, "w")
        confWrite.write(self.text)
        confWrite.close()
