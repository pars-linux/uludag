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

from PyQt4.QtCore import SIGNAL, QTimer
from PyQt4.QtGui import QWidget
from ui import ui_main
from ui import ui_mainscreen
from ui import ui_screen_1
from ui import ui_screen_2
from ui import ui_screen_3

from pds.thread import PThread
from pds.gui import PMessageBox
from pds.gui import TOPCENTER, MIDCENTER, BOTCENTER, CURRENT, OUT
from pds.qpagewidget import QPageWidget

from backend import Iface
from backend import threaded
from repo_helper import findMissingPackagesForDistupdate

ARA_FORM      = "http://cekirdek.pardus.org.tr/~onur/2009to2011/packages/pisi-index.xml.bz2"
REPO_TEMPLATE = "http://packages.pardus.org.tr/pardus/2011/%s/i686/pisi-index.xml.xz"
FORCE_INSTALL = "http://svn.pardus.org.tr/uludag/trunk/pardus-upgrade/2009_to_2011.list"

def getWidget(page = None, title = ""):
    widget = QWidget()
    widget.title = title
    if page:
        page = page.Ui_Screen()
        page.setupUi(widget)
        widget.ui = page
    return widget

class UmMainScreen(QWidget, ui_mainscreen.Ui_UpgradeManager):

    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        self.target_repo = REPO_TEMPLATE % 'stable'
        self.iface = Iface(self)

        self.msgbox = PMessageBox(self)
        self.msgbox.setStyleSheet(PMessageBox.Style)
        self.msgbox.enableOverlay()

        self.thread = PThread(self, self.findMissingPackages, self.showResults)

        self.pageWidget = QPageWidget(self.widget_screens)
        self.layout.addWidget(self.pageWidget)

        self.button_next.clicked.connect(self.pageWidget.next)
        self.button_previous.clicked.connect(self.pageWidget.prev)

        # Update Page Title
        self.connect(self.pageWidget, SIGNAL("currentChanged()"), lambda:\
                    self.label_header.setText(self.pageWidget.getCurrentWidget().title))

        # Welcome
        self.pageWidget.createPage(
                getWidget(ui_screen_1, "Welcome to Upgrade Manager..."))

        # Repo Selection
        self.pageWidget.createPage(
                getWidget(ui_screen_2, "Select Upgrade Repository..."))

        # Dummy Page
        self.pageWidget.createPage(
                getWidget(ui_screen_3, "Checking your system..."),
                inMethod = self.checkSystem, outMethod = self.hideMessage)

        resultWidget = self.pageWidget.getWidget(2).ui
        resultWidget.c_package.hide()
        resultWidget.c_disk.hide()
        resultWidget.success.hide()

    def checkSystem(self):
        # self.button_next.setEnabled(False)
        # self.button_previous.setEnabled(False)
        self.showMessage("Checking your system...")
        repoWidget = self.pageWidget.getWidget(1).ui
        for repo in ('stable', 'devel', 'testing'):
            if getattr(repoWidget, repo).isChecked():
                self.target_repo = REPO_TEMPLATE % repo

        self.thread.start()

    def findMissingPackages(self):
        self.missing_packages = findMissingPackagesForDistupdate(self.target_repo)

    def showResults(self):
        resultWidget = self.pageWidget.getWidget(2).ui
        if self.missing_packages:
            resultWidget.package_list.clear()
            resultWidget.c_package.show()
            resultWidget.package_list.addItems(self.missing_packages)
        else:
            resultWidget.success.show()
        self.label_header.setText("Check results...")
        self.hideMessage()

    def showMessage(self, message):
        self.msgbox.busy.busy()
        self.msgbox.setMessage(message)
        if not self.msgbox.isVisible():
            self.msgbox.animate(start = MIDCENTER, stop = MIDCENTER)

    def hideMessage(self):
        if self.msgbox.isVisible():
            self.msgbox.animate(start = CURRENT, stop = CURRENT, direction = OUT)

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

