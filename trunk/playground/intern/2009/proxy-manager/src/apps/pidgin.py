# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
from xml.dom.minidom import *
from app import App

class Pidgin(App):
    def __init__(self):
        self.path = os.path.expanduser("~/.purple/prefs.xml")
        self.doc = xml.dom.minidom.parse(self.path)
        for pref1 in self.doc.documentElement.getElementsByTagName("pref"):
            if pref1.getAttribute("name") == "purple":
                for pref2 in pref1.getElementsByTagName("pref"):
                    if pref2.getAttribute("name") == "proxy":
                        for pref3 in pref2.getElementsByTagName("pref"):
                            if pref3.getAttribute("name") == "type":
                                self.type = pref3
                            if pref3.getAttribute("name") == "host":
                                self.host = pref3
                            if pref3.getAttribute("name") == "port":
                                self.port = pref3
                            if pref3.getAttribute("name") == "username":
                                self.user = pref3
                            if pref3.getAttribute("name") == "password":
                                self.pasw = pref3

    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        self.setHTTPProxy(ip, port, user, pasw)
    
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        self.type.setAttribute("value", "http")
        self.host.setAttribute("value", ip)
        if port: self.port.setAttribute("value", "" + port)
        else: self.port.setAttribute("value", "0")
        if user: self.user.setAttribute("value", user)
        if pasw: self.pasw.setAttribute("value", pasw)
    
    def noProxy(self):
        self.type.setAttribute("value", "none")
        self.host.setAttribute("value", "")
        self.port.setAttribute("value", "0")
        self.user.setAttribute("value", "")
        self.pasw.setAttribute("value", "")
    
    def close(self):
        conf = open(self.path, "w")
        conf.write(self.doc.toxml("utf-8"))
        conf.close()
