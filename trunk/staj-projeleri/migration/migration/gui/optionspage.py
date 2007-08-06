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

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *

class OptionsPage(QWidget):
    "Dynamically creates a widget of options using sources"
    def __init__(self, sources, destinations={}):
        QWidget.__init__(self)
        self.sources = sources
        self.lay = QVBoxLayout(self, 0, 10, "lay")
        # Wallpaper:
        if sources.has_key("Wallpaper Path"):
            self.wpGroup = QButtonGroup(self, "wpGroup")
            self.wpGroup.setTitle(i18n("Wallpaper"))
            self.wpGroup.setColumnLayout(0, Qt.Horizontal)
            self.wpLayout = QHBoxLayout(self.wpGroup.layout())
            self.lay.addWidget(self.wpGroup)
            # New (current) Wallpaper:
            self.newLayout = QVBoxLayout(None)
            self.newLayout.setAlignment(Qt.AlignCenter)
            self.wpLayout.addLayout(self.newLayout)
            # Thumbnail:
            self.newThumb = QLabel(self.wpGroup, "newThumb")
            if destinations.has_key("Wallpaper Path"):
                newwp = QImage(destinations["Wallpaper Path"])
                newwp = newwp.smoothScale(100, 100, QImage.ScaleMax)
                pixmap = QPixmap(newwp)
                self.newThumb.setPixmap(pixmap)
                self.newLayout.addWidget(self.newThumb)
            else:
                self.newLayout.addSpacing(100)
            # Radio Button:
            self.newRadio = QRadioButton(self.wpGroup, "newRadio")
            if destinations.has_key("Wallpaper Path"):
                self.newRadio.setText(i18n("Keep current wallpaper"))
            else:
                self.newRadio.setText(i18n("Don't use wallpaper"))
            self.newRadio.setChecked(True)
            self.newLayout.addWidget(self.newRadio)
            # Old Wallpaper:
            self.oldLayout = QVBoxLayout(None)
            self.oldLayout.setAlignment(Qt.AlignCenter)
            self.wpLayout.addLayout(self.oldLayout)
            # Thumbnail:
            self.oldThumb = QLabel(self.wpGroup, "oldThumb")
            oldwp = QImage(sources["Wallpaper Path"])
            oldwp = oldwp.smoothScale(100, 100, QImage.ScaleMax)
            pixmap = QPixmap(oldwp)
            self.oldThumb.setPixmap(pixmap)
            self.oldLayout.addWidget(self.oldThumb)
            # Radio Button:
            self.oldRadio = QRadioButton(self.wpGroup, "oldRadio")
            self.oldRadio.setText(i18n("Use my old wallpaper"))
            self.oldLayout.addWidget(self.oldRadio)
        # Bookmarks:
        if sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            self.Bookmarks = QGroupBox(self, "Bookmarks")
            self.Bookmarks.setTitle(i18n("Bookmarks"))
            self.Bookmarks.setColumnLayout(0, Qt.Vertical)
            self.BookmarksLayout = QVBoxLayout(self.Bookmarks.layout())
            self.lay.addWidget(self.Bookmarks)
            # FF Bookmarks:
            if sources.has_key("Firefox Profile Path"):
                self.FFBookmarks = QCheckBox(self.Bookmarks, "FFBookmarks")
                self.FFBookmarks.setText(i18n("Firefox bookmarks"))
                self.FFBookmarks.setChecked(True)
                self.BookmarksLayout.addWidget(self.FFBookmarks)
            # IE Bookmarks:
            if sources.has_key("Favorites Path"):
                self.IEBookmarks = QCheckBox(self.Bookmarks, "IEBookmarks")
                self.IEBookmarks.setText(i18n("Internet Explorer favorites"))
                self.IEBookmarks.setChecked(True)
                self.BookmarksLayout.addWidget(self.IEBookmarks)
        # Accounts:
        if sources.has_key("GTalk Key"):
            self.Accounts = QGroupBox(self, "Accounts")
            self.Accounts.setTitle(i18n("Accounts"))
            self.Accounts.setColumnLayout(0, Qt.Vertical)
            self.AccountsLayout = QVBoxLayout(self.Accounts.layout())
            self.lay.addWidget(self.Accounts)
            # GTalk Accounts:
            if sources.has_key("GTalk Key"):
                self.GTalk = QCheckBox(self.Accounts, "GTalk")
                self.GTalk.setText(i18n("GTalk Accounts"))
                self.GTalk.setChecked(True)
                self.AccountsLayout.addWidget(self.GTalk)
            # MSN Accounts:
            if sources.has_key("Contacts Path"):
                self.MSN = QCheckBox(self.Accounts, "MSN")
                self.MSN.setText(i18n("MSN Accounts"))
                self.MSN.setChecked(True)
                self.AccountsLayout.addWidget(self.MSN)
        # Spacer:
        spacer = QSpacerItem(1,1,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.lay.addItem(spacer)
    
    def getOptions(self):
        "Returns a dictionary consists of selected options"
        options = {}
        # Add fundamental items:
        for item in ["Partition", "OS Type", "User Name", "Home Path"]:
            options[item] = self.sources[item]
        # Add selected optional items:
        items = [("IEBookmarks", "Favorites Path"),
                 ("FFBookmarks", "Firefox Profile Path"),
                 ("oldRadio", "Wallpaper Path"),
                 ("GTalk", "GTalk Key"),
                 ("MSN", "Contacts Path")]
        for widgetname, dictname in items:
            item = self.child(widgetname)
            if item and item.isChecked():
                options[dictname] = self.sources[dictname]
        return options
