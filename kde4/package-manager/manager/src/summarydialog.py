#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *
from PyKDE4.kio import KRun

from ui_summarydialog import Ui_SummaryDialog
from ui_appitem import Ui_ApplicationItem

from pmutils import *

import backend
import localedata
import desktopparser

class ApplicationItem(QtGui.QListWidgetItem):
    def __init__(self, name, comment, icon, command, parent=None):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.name = name
        self.comment = comment
        self.icon = icon
        self.command = command

class ApplicationItemWidget(QtGui.QWidget, Ui_ApplicationItem):
    def __init__(self, item, parent=None):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.setupUi(self)
        self.item = item
        self.initialize()

    def initialize(self):
        self.appComment.setText(self.item.comment)
        self.appName.setText(self.item.name)
        self.appIcon.setPixmap(KIcon(self.item.icon).pixmap(32))
        self.appName.hide()

    def enterEvent(self, event):
        self.appName.show()

    def leaveEvent(self, event):
        self.appName.hide()

    def mouseDoubleClickEvent(self, event):
        KRun.runCommand(self.item.command, None)

class SummaryDialog(QtGui.QDialog, Ui_SummaryDialog):
    def __init__(self, operation, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = backend.pm.Iface()
        self.lang = localedata.getKDELocale()
        self.operation = operation

    def setDesktopFiles(self, desktopFiles):
        self.appList.clear()
        for desktopFile in desktopFiles:
            self.addApplication(desktopFile)

    def addApplication(self, desktopFile):
        parser = desktopparser.DesktopParser()
        parser.read("/%s" % str(desktopFile))

        icon = parser.safe_get_locale('Desktop Entry', 'Icon', None)
        command = parser.safe_get_locale('Desktop Entry', 'Exec', None)
        name = unicode(parser.safe_get_locale('Desktop Entry', 'Name', self.lang))
        comment = unicode(parser.safe_get_locale('Desktop Entry', 'Comment', self.lang))
        if not comment:
            comment = unicode(parser.safe_get_locale('Desktop Entry', 'GenericName', self.lang))

        item = ApplicationItem(name, comment, icon, command, self.appList)
        item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
        item.setSizeHint(QSize(0,48))
        itemWidget = ApplicationItemWidget(item, self)
        self.appList.setItemWidget(item, itemWidget)

    def show(self):
        self.setDesktopFiles(self.operation.desktopFiles)
        QtGui.QDialog.show(self)
