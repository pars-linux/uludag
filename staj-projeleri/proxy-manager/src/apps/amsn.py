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

class AMSN(App):
    def __init__(self):
        self.path = os.path.expanduser("~/.amsn/config.xml")
        self.doc = xml.dom.minidom.parse(self.path)
        entries = self.doc.getElementsByTagName("entry")
        for entry in entries:
            # value of the 'attribute' element
            attribute = entry.firstChild.nextSibling
            # value of the 'value' element
            value = attribute.nextSibling.nextSibling
            #TODO: add auth. code
            if attribute.firstChild.nodeValue == "connectiontype":
                self.connectiontype = value
            elif attribute.firstChild.nodeValue == "proxy":
                self.proxy = value

    def setGlobalProxy(self, ip, port=None, user=None, pasw=None):
        self.setHTTPProxy(ip, port, user, pasw)
    
    def setHTTPProxy(self, ip, port=None, user=None, pasw=None):
        self.connectiontype.firstChild.nodeValue = "proxy"
        textValue = ip
        if port: textValue = textValue + " " + port
        if self.proxy.firstChild == None: self.proxy.appendChild( self.doc.createTextNode(textValue) )
        else: self.proxy.firstChild.nodeValue = textValue
    
    def noProxy(self):
        self.connectiontype.firstChild.nodeValue = "direct"
    
    def close(self):
        conf = open(self.path, "w")
        conf.write(self.doc.toxml("utf-8"))
        conf.close()
