#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2011 TUBITAK/UEKAE
# Upgrade Manager
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import sys

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QWidget
from ui import ui_main
from ui import ui_mainscreen
from ui import ui_screen_1
from ui import ui_screen_2
from ui import ui_screen_3

from pds.gui import PMessageBox
from pds.gui import TOPCENTER, MIDCENTER, BOTCENTER
from pds.qpagewidget import QPageWidget
from backend import Iface

def getWidget(page = None, title = ""):
    widget = QWidget()
    widget.title = title
    if page:
        page = page()
        page.setupUi(widget)
    return widget

class UmMainScreen(QWidget, ui_mainscreen.Ui_UpgradeManager):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.iface = Iface(self)

        self.msgbox = PMessageBox(self)
        self.msgbox.busy.setColor("black")

        pageWidget = QPageWidget(self.widget_screens)
        self.layout.addWidget(pageWidget)

        self.button_next.clicked.connect(pageWidget.next)
        self.button_previous.clicked.connect(pageWidget.prev)

        # Update Page Title
        self.connect(pageWidget, SIGNAL("currentChanged()"), lambda:\
                    self.label_header.setText(pageWidget.getCurrentWidget().title))

        # Welcome
        pageWidget.createPage(
                getWidget(ui_screen_1.Ui_Screen, "Welcome to Upgrade Manager..."))

        # Repo Selection
        pageWidget.createPage(
                getWidget(ui_screen_2.Ui_Screen, "Select Upgrade Repository..."))

        # Dummy Page
        pageWidget.createPage(
                getWidget(), inMethod = self.checkSystem)

    def checkSystem(self):
        self.button_next.setEnabled(False)
        self.button_previous.setEnabled(False)
        self.showMessage("Checking your system...")

    def showMessage(self, message):
        self.msgbox.busy.busy()
        self.msgbox.setMessage(message)
        self.msgbox.animate(start = TOPCENTER, stop = MIDCENTER)

    def hideMessage(self):
        if self.msgbox.isVisible():
            self.msgbox.animate(start = CURRENT, stop = BOTCENTER, direction = OUT)

    def updateProgress(self, package, downloaded, total, symbol, percent):
        print package, downloaded, total, symbol, percent
        self.progress.setValue(percent)
        if percent == 100:
            self.label.setText("Download Complete, please press Exit.")
            self.exitButton.show()
            self.progress.hide()

class UmGui(QWidget, ui_main.Ui_UpgradeManager):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.progress.hide()
        self.exitButton.hide()

        self.iface = Iface(self)

        self.upgradeButton.clicked.connect(self.upgrade)
        self.exitButton.clicked.connect(sys.exit)

    def upgrade(self):
        self.upgradeButton.hide()
        self.progress.show()

        self.iface.downloadPackages(['urbanterror'])

    def updateProgress(self, package, downloaded, total, symbol, percent):
        print package, downloaded, total, symbol, percent
        self.progress.setValue(percent)
        if percent == 100:
            self.label.setText("Download Complete, please press Exit.")
            self.exitButton.show()
            self.progress.hide()

