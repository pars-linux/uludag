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

import os
from qt import *
from qtext import *

import templates
import config
import utils

class SpecEd(utils.TextEd):
    def __init__(self, path, name):
        utils.TextEd.__init__(self, path, "pspec.xml", utils.HTMLLexer())
        if not self.loaded:
            data = { "PACKAGE":  name, "NAME": config.name, "EMAIL": config.email, "DATE": "2005-08-06" }
            self.setText(templates.pspec_xml % (data))


class ActionEd(utils.TextEd):
    def __init__(self, path, name):
        utils.TextEd.__init__(self, path, "actions.py", utils.PythonLexer())
        if not self.loaded:
            data = { "PACKAGE":  name, "NAME": config.name, "EMAIL": config.email }
            self.setText(templates.actions_py % (data))


class PisiOut(utils.TextEd):
    def __init__(self, path):
        utils.TextEd.__init__(self, path, "debug.txt")


class Editor(QMainWindow):
    def __init__(self, path, name):
        QMainWindow.__init__(self)
        self.setMinimumSize(540, 320)
        self.setCaption(name + " - pisimat")
        self.pak_path = path
        self.pak_name = name
        # menu
        bar = self.menuBar()
        file_ = QPopupMenu(self)
        bar.insertItem("&File", file_)
        file_.insertItem("Save", self.save, self.CTRL + self.Key_S)
        file_.insertSeparator()
        file_.insertItem("Close", self.close, self.CTRL + self.Key_Q)
        pisi = QPopupMenu(self)
        bar.insertItem("&Pisi", pisi)
        pisi.insertItem("Fetch", self.close, self.CTRL + self.Key_F)
        pisi.insertItem("Unpack", self.close, self.CTRL + self.Key_U)
        pisi.insertItem("Compile", self.close, self.CTRL + self.Key_C)
        pisi.insertItem("Build", self.close, self.CTRL + self.Key_B)
        # editing area
        tab = QTabWidget(self)
        tab.setTabPosition(tab.Bottom)
        self.setCentralWidget(tab)
        self.spec_ed = SpecEd(path, name)
        tab.addTab(self.spec_ed, "pspec.xml")
        self.action_ed = ActionEd(path, name)
        tab.addTab(self.action_ed, "actions.py")
        self.pisi_out = PisiOut(path)
        tab.addTab(self.pisi_out, "Pisi Output")
        # show window
        self.show()
    
    def save(self):
        self.spec_ed.save_changes()
        self.action_ed.save_changes()
