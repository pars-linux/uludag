#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n

from migration.gui.ScreenWidget import ScreenWidget
import migration.gui.context as ctx

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Welcome")
    desc = ki18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)



    def creator(self):
         # Bookmarks:
        if ctx.sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            self.bookmarks = QtGui.QGroupBox(self, "Bookmarks")
            self.bookmarks.setTitle(i18n("Bookmarks"))
            self.bookmarks.setColumnLayout(0, Qt.Vertical)
            self.bookmarksLayout = QtGui.QVBoxLayout(self.bookmarks.layout())
            self.lay.addWidget(self.bookmarks)
            # FF Bookmarks:
            if sources.has_key("Firefox Profile Path"):
                self.FFBookmarks = QCheckBox(self.Bookmarks, "FFBookmarks")
                self.FFBookmarks.setText(i18n("Firefox bookmarks"))
                self.FFBookmarks.setChecked(True)
                QToolTip.add(self.FFBookmarks, i18n("Copies your old Firefox bookmarks to Firefox under Pardus."))
                self.BookmarksLayout.addWidget(self.FFBookmarks)
            # Opera Bookmarks:
            if sources.has_key("Opera Profile Path"):
                self.OperaBookmarks = QCheckBox(self.Bookmarks, "OperaBookmarks")
                self.OperaBookmarks.setText(i18n("Opera bookmarks"))
                self.OperaBookmarks.setChecked(True)
                QToolTip.add(self.OperaBookmarks, i18n("Copies your old Opera bookmarks to Firefox under Pardus."))
                self.BookmarksLayout.addWidget(self.OperaBookmarks)
            # IE Bookmarks:
            if sources.has_key("Favorites Path"):
                self.IEBookmarks = QCheckBox(self.Bookmarks, "IEBookmarks")
                self.IEBookmarks.setText(i18n("Internet Explorer favorites"))
                self.IEBookmarks.setChecked(True)
                QToolTip.add(self.IEBookmarks, i18n("Copies your old Internet Explorer favorites to Firefox under Pardus."))
                self.BookmarksLayout.addWidget(self.IEBookmarks)
    def shown(self):
        pass

    def execute(self):
        return True