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

import sys
from qt import *

# default settings
name = u"Pars Paketçioğlu"
email = "pardus@uludag.org.tr"
pspec_folder = "."

class ConfigWindow(QDialog):
    def __init__(self, *args):
        QDialog.__init__(self, *args)
        self.setCaption("Pisimat Settings")
        vb = QVBoxLayout(self, 6)
        g = QGridLayout(vb, 3, 2, 6)
        lab = QLabel("Name", self)
        g.addWidget(lab, 0, 0)
        lab = QLabel("Email", self)
        g.addWidget(lab, 1, 0)
        lab = QLabel("PSpec folder", self)
        g.addWidget(lab, 2, 0)
        self.name = QLineEdit(self)
        g.addWidget(self.name, 0, 1)
        self.email = QLineEdit(self)
        g.addWidget(self.email, 1, 1)
        hb = QHBoxLayout(self, 1)
        self.dir = QLineEdit(self)
        hb.addWidget(self.dir)
        b = QPushButton("...", self)
        self.connect(b, SIGNAL("clicked()"), self.ask_file)
        hb.addWidget(b)
        g.addLayout(hb, 2, 1)
        b = QPushButton("OK", self)
        b.setDefault(True)
        self.connect(b, SIGNAL("clicked()"), self.accept)
        vb.addWidget(b)
    
    def ask_file(self):
        s = QFileDialog.getExistingDirectory(self.dir.text(), self, "lala", "Choose PSpec folder", False)
        self.dir.setText(s)
    
    def accept(self):
        if self.name.text() == "" or self.email.text() == "" or self.dir.text() == "":
            return
        QDialog.accept(self)
    
    def reject(self):
        sys.exit(0)
