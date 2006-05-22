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


class PathEntry(QHBox):
    def __init__(self, question, parent, is_dir=True):
        QHBox.__init__(self, parent)
        self.is_dir = is_dir
        self.question = question
        self.setSpacing(3)
        self.path = QLineEdit(self)
        self.path.setMinimumWidth(120)
        but = QPushButton("...", self)
        self.connect(but, SIGNAL("clicked()"), self.browse)
    
    def browse(self):
        if self.is_dir:
            s = QFileDialog.getExistingDirectory(self.path.text(), self, "lala", self.question, False)
        else:
            s = QFileDialog.getOpenFileName(self.path.text(), "All (*.*)", self, "lala", self.question)
        self.path.setText(s)
    
    def text(self):
        return str(self.path.text())


def makePathEntry(label, question, grid, row, parent, is_dir=True):
    lab = QLabel(label, parent)
    grid.addWidget(lab, row, 0, Qt.AlignRight)
    edit = PathEntry(question, parent, is_dir)
    grid.addWidget(edit, row, 1)
    return edit


class Project(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        w = QWidget(self)
        self.setCentralWidget(w)
        
        grid = QGridLayout(w, 9, 2, 12, 6)
        
        lab = QLabel(_("Project name:"), w)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.name = QLineEdit(w)
        grid.addWidget(self.name, 0, 1)
        
        line = HLine(_("CD Contents:"), w)
        grid.addMultiCellWidget(line, 1, 1, 0, 1)
        self.contentdir = makePathEntry(
            _("Release files:"),
            _("Select release files..."),
            grid, 2, w
        )
        self.cdroot = makePathEntry(
            _("Boot image:"),
            _("Select boot image..."),
            grid, 3, w, is_dir=False
        )
        
        line = HLine(_("Package selection:"), w)
        grid.addMultiCellWidget(line, 4, 4, 0, 1)
        self.packagedir = makePathEntry(
            _("Binary packages:"),
            _("Select binary package folder..."),
            grid, 5, w
        )
        
        but = QPushButton(_("Select packages"), w)
        self.connect(but, SIGNAL("clicked()"), self.selectPackages)
        grid.addMultiCellWidget(but, 6, 6, 0, 1)
        
        line = QFrame(w)
        line.setFrameStyle(line.HLine | line.Sunken)
        grid.addMultiCellWidget(line, 7, 7, 0, 1, Qt.AlignBottom)
        
        hb = QHBox(w)
        hb.setSpacing(12)
        grid.addMultiCellWidget(hb, 8, 8, 0, 1, Qt.AlignBottom)
        
        QPushButton(_("Save"), hb)
        QPushButton(_("Save as..."), hb)
        QPushButton(_("Make ISO"), hb)
        
        self.show()
    
    def selectPackages(self):
        browser.PackageSelector(self, self.packagedir.text()).exec_loop()
