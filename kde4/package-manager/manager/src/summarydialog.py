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

from ui_summarydialog import Ui_SummaryDialog
from ui_appitem import Ui_ApplicationItem

from pmutils import *

import backend
import localedata
import desktopparser

class ApplicationItem(QtGui.QListWidgetItem):
    def __init__(self, genericName, name, icon, command, parent=None):
        QtGui.QListWidgetItem.__init__(self, parent)

        self.genericName = genericName
        self.name = name
        self.icon = icon
        self.command = command

class ApplicationItemWidget(QtGui.QWidget, Ui_ApplicationItem):
    def __init__(self, item, parent=None):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.setupUi(self)
        self.item = item
        self.initialize()

    def initialize(self):
        self.appName.setText(self.item.genericName)
        self.appSummary.setText(self.item.genericName)
        self.appIcon.setPixmap(KIcon(self.item.icon).pixmap(32))

class SummaryDialog(QtGui.QDialog, Ui_SummaryDialog):
    def __init__(self, operation, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.iface = backend.pm.Iface()
        self.parser = desktopparser.DesktopParser()
        self.lang = localedata.getKDELocale()
        self.operation = operation

    def setDesktopFiles(self, desktopFiles):
        for desktopFile in desktopFiles:
            self.addApplication(desktopFile)

    def __getValue(self, name):
        try:
            value = self.parser.get_locale('Desktop Entry', '%s[%s]' % (name, self.lang), '')
        except:
            value = self.parser.get_locale('Desktop Entry', name, '')
        return value

    def addApplication(self, desktopFile):
        self.parser.read("/%s" % str(desktopFile))
        item = ApplicationItem(self.__getValue("Comment"),
                               self.__getValue("Name"),
                               self.__getValue("Icon"),
                               self.__getValue("Exec"),
                               self.appList)
        item.setFlags(Qt.NoItemFlags | Qt.ItemIsEnabled)
        item.setSizeHint(QSize(0,48))
        itemWidget = ApplicationItemWidget(item, self)
        self.appList.setItemWidget(item, itemWidget)

    def show(self):
        self.setDesktopFiles(self.operation.desktopFiles)
        QtGui.QDialog.show(self)
