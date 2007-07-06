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

import Wallpaper

class Options(QWidget):
    def __init__(self, sources, destinations={}):
        QWidget.__init__(self)
        self.sources = sources
        self.layout = QVBoxLayout(self)
        
        # Bookmarks:
        if sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            self.Bookmarks = QGroupBox(self)
            self.Bookmarks.setTitle(u"Bookmarks")
            self.Bookmarks.setColumnLayout(0,Qt.Vertical)
            self.BookmarksLayout = QVBoxLayout(self.Bookmarks.layout())
            self.layout.addWidget(self.Bookmarks)
            
            if sources.has_key("Firefox Profile Path"):
                self.FFBookmarks = QCheckBox(self.Bookmarks)
                self.FFBookmarks.setText(u"Firefox bookmarks")
                self.BookmarksLayout.addWidget(self.FFBookmarks)
            
            if sources.has_key("Favorites Path"):
                self.IEBookmarks = QCheckBox(self.Bookmarks)
                self.IEBookmarks.setText(u"Internet Explorer favorites")
                self.BookmarksLayout.addWidget(self.IEBookmarks)
        
        # Wallpaper:
        if sources.has_key("Wallpaper Path") and destinations.has_key("Wallpaper Path"):
            self.wpGroup = QButtonGroup(self)
            self.wpGroup.setTitle("Wallpaper")
            self.wpGroup.setColumnLayout(0,Qt.Horizontal)
            self.wpLayout = QHBoxLayout(self.wpGroup.layout())
            self.layout.addWidget(self.wpGroup)
            
            # New (current) Wallpaper:
            self.newLayout = QVBoxLayout(None)
            self.newLayout.setAlignment(Qt.AlignCenter)
            self.wpLayout.addLayout(self.newLayout)
            
            self.newThumb = QLabel(self.wpGroup)
            newwp = Wallpaper.getThumbnail(destinations["Wallpaper Path"])
            pixmap = QPixmap(newwp)
            self.newThumb.setPixmap(pixmap)
            self.newLayout.addWidget(self.newThumb)
            
            self.newRadio = QRadioButton(self.wpGroup)
            self.newRadio.setText(u"Keep current wallpaper")
            self.newRadio.setChecked(True)
            self.newLayout.addWidget(self.newRadio)
            
            # Old Wallpaper:
            self.oldLayout = QVBoxLayout(None)
            self.oldLayout.setAlignment(Qt.AlignCenter)
            self.wpLayout.addLayout(self.oldLayout)
            
            self.oldThumb = QLabel(self.wpGroup)
            oldwp = Wallpaper.getThumbnail(sources["Wallpaper Path"])
            pixmap = QPixmap(oldwp)
            self.oldThumb.setPixmap(pixmap)
            self.oldLayout.addWidget(self.oldThumb)
            
            self.oldRadio = QRadioButton(self.wpGroup)
            self.oldRadio.setText(u"Use old wallpaper")
            self.oldLayout.addWidget(self.oldRadio)
        
        spacer = QSpacerItem(1,1,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.layout.addItem(spacer)
    
    def getOptionsSteps(self):
        options = {"Bookmarks":0, "FFBookmarks":0, "IEBookmarks":0, "Change Wallpaper":0}
        if self.sources.has_key("Firefox Profile Path") and self.FFBookmarks.isOn():
            options["FFBookmarks"] = 1
            options["Bookmarks"] = 1
        if self.sources.has_key("Favorites Path") and self.IEBookmarks.isOn():
            options["IEBookmarks"] = 1
            options["Bookmarks"] = 1
        if self.oldRadio.isChecked():
            options["Change Wallpaper"] = 1
        steps = options["Bookmarks"] + options["FFBookmarks"] + options["IEBookmarks"] + options["Change Wallpaper"]
        return options, steps
