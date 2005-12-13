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

class Window(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.my_parent = parent
        vb = QVBox(self)
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
        
        self.links = QListBox(vb)
        for item in links:
            self.links.insertItem(item)
        
        self.show()
