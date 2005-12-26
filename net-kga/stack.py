#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
import widgets


class Window(QMainWindow):
    def __init__(self, parent, comar):
        QMainWindow.__init__(self, parent)
        self.comar = comar
        
        self.setCaption(i18n("Network Settings"))
        self.setMinimumSize(280, 320)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(6)
        self.setCentralWidget(vb)
        
        widgets.HLine(i18n("Computer"), vb)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        QLabel(i18n("Host name:"), hb)
        self.host = widgets.Edit(hb)
        
        widgets.HLine(i18n("Name servers"), vb)
        
        self.dns = QListBox(vb)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        but = QPushButton(i18n("Add"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAdd)
        but = QPushButton(i18n("Remove"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotRemove)
        
        self.comar.call("Net.Stack.getHostNames", id=50)
        self.comar.call("Net.Stack.getNameServers", id=51)
    
    def slotAdd(self):
        pass
    
    def slotRemove(self):
        pass
    
    def slotComar(self, reply):
        if reply[0] == self.comar.RESULT:
            if reply[1] == 51:
                self.dns.clear()
                for item in reply[2].split("\n"):
                    self.dns.insertItem(item)
            elif reply[1] == 50:
                self.host.edit.setText(reply[2])
