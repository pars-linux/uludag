# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from xml.dom.minidom import *

from module import Module

class AMSN(Module):
    
    def __init__(self):
        # FIXME: find paths automatically
        self.path = "/home/bertan/.amsn/rmznbrtn_hotmail_com/config.xml"
        self.doc = xml.dom.minidom.parse(self.path)
        self.conf = open(self.path, "w")
        entries = self.doc.getElementsByTagName("entry")
        for entry in entries:
            # value of the 'attribute' element
            attribute = entry.firstChild.nextSibling
            # value of the 'value' element
            value = attribute.nextSibling.nextSibling
            if attribute.firstChild.nodeValue == "connectiontype":
                self.connectiontype = value
            elif attribute.firstChild.nodeValue == "proxy":
                self.proxy = value

    def setGlobalProxy(self, ip, port=None):
        self.connectiontype.firstChild.nodeValue = "proxy"
        textValue = ip
        if not port: textValue + " " + port
        if self.proxy.firstChild == None: self.proxy.appendChild( self.doc.createTextNode(textValue) )
        else: self.proxy.firstChild.nodeValue = textValue
    
    def noProxy(self):
        self.connectiontype.firstChild.nodeValue = "direct"
    
    def close(self):
        self.conf.write(self.doc.toxml("utf-8"))

