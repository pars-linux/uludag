#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
from qt import *

import browser

# no i18n yet
def _(x):
    return x


class HLine(QHBox):
    def __init__(self, title, parent):
        QHBox.__init__(self, parent)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        
        line = QFrame(self)
        line.setFrameStyle(line.HLine | line.Sunken)
        self.setStretchFactor(line, 1)
        
        text = QLabel(" %s " % unicode(title), self)
        
        line = QFrame(self)
        line.setFrameStyle(line.HLine | line.Sunken)
        self.setStretchFactor(line, 8)


class Project(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(3)
        self.setCentralWidget(vb)
        
        HLine(_("CD Contents:"), vb)
        
        hb = QHBox(vb)
        hb.setSpacing(3)
        QLabel(_("Release files:"), hb)
        self.contentdir = QLineEdit(hb)
        
        hb = QHBox(vb)
        hb.setSpacing(3)
        QLabel(_("Boot image:"), hb)
        self.cdroot = QLineEdit(hb)
        
        HLine(_("Package selection:"), vb)
        
        hb = QHBox(vb)
        hb.setSpacing(3)
        QLabel(_("Binary package folder:"), hb)
        self.packagedir = QLineEdit(hb)
        but = QPushButton(_("Select"), hb)
        self.connect(but, SIGNAL("clicked()"), self.selectPackages)
        self.show()
    
    def selectPackages(self):
        browser.PackageSelector(self, str(self.packagedir.text()))
