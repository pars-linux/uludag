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
import connection
import comar
import widgets


class Link(QListBoxItem):
    def __init__(self, box, comar, link_name):
        QListBoxItem.__init__(self, box)
        self.comar = comar
        self.link_name = link_name
        self.link_type = "net"
        self.remote_name = ""
        comar.call_package("Net.Link.linkInfo", link_name)
        tmp = comar.read_cmd()
        if tmp[0] != comar.RESULT:
            return
        self.link_type, self.name, self.remote_name = tmp[2].split("\n")
        
        self.f1 = QFont()
        self.f1.setBold(True)
        self.f1.setPointSize(self.f1.pointSize() + 4)
        self.pix = QPixmap("ether.png")
    
    def paint(self, painter):
        fm = QFontMetrics(self.f1)
        painter.setPen(Qt.black)
        painter.setFont(self.f1)
        painter.drawText(32 + 9, 3 + fm.ascent(), unicode(self.name))
        painter.drawPixmap(3, 3, self.pix)
    
    def height(self, box):
        fm = QFontMetrics(self.f1)
        ts = 3 + fm.height() + 3
        if ts < 32 + 3 + 3:
            ts = 32 + 3 + 3
        return ts
    
    def width(self, box):
        return 100


class Window(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.setMinimumSize(320, 240)
        self.setCaption("Connection types")
        self.my_parent = parent
        vb = QVBox(self)
        vb.setSpacing(6)
        vb.setMargin(12)
        self.setCentralWidget(vb)
        
        self.comar = comar.Link()
        self.comar.get_packages("Net.Link")
        tmp = self.comar.read_cmd()
        if tmp[0] != self.comar.RESULT:
            self.close(True)
            return
        
        if tmp[2] == "":
            QMessageBox.warning(self, "Install network packages!",
                "No package with COMAR network scripts are installed yet.",
                QMessageBox.Ok, QMessageBox.NoButton)
            self.close(True)
            return
        
        links = tmp[2].split("\n")
        if len(links) == 1:
            connection.Window(parent, "new connection", links[0], 1)
            self.close(True)
            return
        
        QLabel("Select a connection type:", vb)
        
        self.links = QListBox(vb)
        for item in links:
            Link(self.links, self.comar, item)
        
        but = QPushButton("Create connection", vb)
        self.connect(but, SIGNAL("clicked()"), self.slotCreate)
        
        self.show()
    
    def slotCreate(self):
        link = self.links.selectedItem()
        if link:
            connection.Window(self.my_parent, "new connection", link.link_name, 1)
            self.close(True)
