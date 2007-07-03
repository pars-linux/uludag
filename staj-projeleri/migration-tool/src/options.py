#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *

class Options(QWidget):
    def __init__(self, sources):
        QWidget.__init__(self)
        self.sources = sources
        self.layout = QVBoxLayout(self)
        
        # Bookmarks:
        if sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            self.Bookmarks = QGroupBox(self)
            self.Bookmarks.setTitle(u"Yer İmleri")
            self.Bookmarks.setColumnLayout(0,Qt.Vertical)
            self.BookmarksLayout = QVBoxLayout(self.Bookmarks.layout())
            self.layout.addWidget(self.Bookmarks)
            
            if sources.has_key("Firefox Profile Path"):
                self.FFBookmarks = QCheckBox(self.Bookmarks)
                self.FFBookmarks.setText(u"Firefox yer imlerini alayım mı?")
                self.BookmarksLayout.addWidget(self.FFBookmarks)
            
            if sources.has_key("Favorites Path"):
                self.IEBookmarks = QCheckBox(self.Bookmarks)
                self.IEBookmarks.setText(u"Internet Explorer yer imlerini alayım mı?")
                self.BookmarksLayout.addWidget(self.IEBookmarks)
        
        spacer = QSpacerItem(1,1,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout.addItem(spacer)
    
    def getOptionsSteps(self):
        options = {"Bookmarks":0, "FFBookmarks":0, "IEBookmarks":0}
        if self.sources.has_key("Firefox Profile Path") and self.FFBookmarks.isOn():
            options["FFBookmarks"] = 1
            options["Bookmarks"] = 1
        if self.sources.has_key("Favorites Path") and self.IEBookmarks.isOn():
            options["IEBookmarks"] = 1
            options["Bookmarks"] = 1
        steps = options["Bookmarks"] + options["FFBookmarks"] + options["IEBookmarks"]
        return options, steps
