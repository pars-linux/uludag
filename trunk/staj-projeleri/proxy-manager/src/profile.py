# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

import os
import ConfigParser
from kdecore import *

# Constants
comment_direct = i18n("Direct connection")
comment_globl = i18n("Global proxy: ")
comment_http = i18n("HTTP")
comment_ftp = i18n("FTP")
comment_ssl = i18n("SSL")
comment_socks = i18n("SOCKS")
comment_auto = i18n("Auto configuration file.")
direct = "0"
globl = "1"
indiv = "2"
auto = "3"

noProxy = "noproxy"

config = ConfigParser.SafeConfigParser()
configDir = os.path.expanduser("~/.proxy/")
configPath = configDir +"proxy"
profiles = []

def parseConfig():
    if not os.path.exists(configDir):
        os.mkdir(configDir)
    config.read(configPath)
    if not config.has_section(noProxy):
        config.add_section(noProxy)
    if not config.has_option(noProxy,"isActive"):
        config.set(noProxy,"isActive","1")
    config.set(noProxy, "type", "0")
    # Create profiles
    for s in config.sections():
        profiles.append(Profile(s))
    
    return profiles

def save():
    for p in profiles:
        p.save()
    f = open(configPath,"w")
    config.write(f)
    f.close()

def deleteProfile(prfl):
    config.remove_section(prfl.name)
    del profiles[profiles.index(prfl)]

def exists(name):
    return config.has_section(name)
    
class Profile:
    def __init__(self, section):
        if section != noProxy: self.name = unicode(section)
        else: self.name = i18n("No Proxy")
        self.section = section
        self.comment = ""
        
        if config.has_section(self.section):
            # General properties
            self.type = config.get(self.section, "type")
            self.isActive = config.getboolean(self.section, "isActive")
            
            # Protocol dependent properties
            self.cleanProperties()
            
            if self.type == direct:
                self.comment = comment_direct
            elif self.type == globl:
                self.has_globl_port = config.has_option(self.section, "globl_port")
                self.globl_host = config.get(self.section, "globl_host")
                if self.has_globl_port: self.globl_port = config.get(self.section, "globl_port")
                self.comment = comment_globl + " " + self.globl_host
            elif self.type == indiv:
                self.comment = i18n("Protocols: ")
                self.has_http = config.has_option(self.section, "http_host")
                self.has_ftp = config.has_option(self.section, "ftp_host")
                self.has_ssl = config.has_option(self.section, "ssl_host")
                self.has_socks = config.has_option(self.section, "socks_host")
                if self.has_http:
                    self.http_host = config.get(self.section, "http_host")
                    self.http_port = config.get(self.section, "http_port")
                    self.comment += " " + comment_http + ":" + self.http_host
                if self.has_ftp:
                    self.ftp_host = config.get(self.section, "ftp_host")
                    self.ftp_port = config.get(self.section, "ftp_port")
                    self.comment += " " + comment_ftp + ":" + self.ftp_host
                if self.has_ssl:
                    self.ssl_host = config.get(self.section, "ssl_host")
                    self.ssl_port = config.get(self.section, "ssl_port")
                    self.comment += " " + comment_ssl + ":" + self.ssl_host
                if self.has_socks:
                    self.socks_host = config.get(self.section, "socks_host")
                    self.socks_port = config.get(self.section, "socks_port")
                    self.comment += " " + comment_socks + ":" + self.socks_host
            elif self.type == auto:
                self.auto_url = config.get(self.section, "auto_url")
                self.comment = comment_auto
        else:
            config.add_section(self.section)
            self.isActive = False
            self.cleanProperties()
    
    def cleanProperties(self):
        self.globl_host = self.globl_port = ""
        self.http_host = self.http_port = ""
        self.ftp_host = self.ftp_port = ""
        self.ssl_host = self.ssl_port = ""
        self.socks_host = self.socks_port = ""
        self.auto_url = ""
    
    def changeName(self, new):
        if config.has_section(self.section):
            config.remove_section(self.section)
        config.add_section(new)
        self.section = new
        self.name = self.section
        self.cleanProperties()
    
    def save(self):
        config.set(self.section, "type", self.type)
        config.set(self.section, "isActive", str(self.isActive))
        if self.type == direct:
            pass
        elif self.type == globl:
            config.set(self.section, "globl_host", self.globl_host)
            config.set(self.section, "globl_port", self.globl_port)
        elif self.type == indiv:
            if self.http_host:
                config.set(self.section, "http_host", self.http_host)
                config.set(self.section, "http_port", self.http_port)
            if self.ftp_host:
                config.set(self.section, "ftp_host", self.ftp_host)
                config.set(self.section, "ftp_port", self.ftp_port)
            if self.ssl_host:
                config.set(self.section, "ssl_host", self.ssl_host)
                config.set(self.section, "ssl_port", self.ssl_port)
            if self.socks_host:
                config.set(self.section, "socks_host", self.socks_host)
                config.set(self.section, "socks_port", self.socks_port)
        elif self.type == auto:
            config.set(self.section, "auto_url", self.auto_url)
