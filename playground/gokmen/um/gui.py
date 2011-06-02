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

import os
import sys
import time
import pisi
import urlgrabber

from PyQt4.QtCore import SIGNAL, QTimer
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget

from ui import ui_main
from ui import ui_mainscreen
from ui import ui_screen_1
from ui import ui_screen_2
from ui import ui_screen_3
from ui import ui_screen_4
from ui import ui_screen_5

from pds.thread import PThread
from pds.gui import PMessageBox
from pds.gui import TOPCENTER, MIDCENTER, BOTCENTER, CURRENT, OUT
from pds.qpagewidget import QPageWidget

from backend import Iface
from backend import cleanup_pisi
from repo_helper import findMissingPackagesForDistupdate

from migratekde import migrateKDE
from migrategrubconf import migrateGrubconf

ARA_FORM      = "http://cekirdek.pardus.org.tr/~onur/2009to2011/packages/%s"
REQUIRED_PACKAGES = ("libuser-0.57.1-1-1.pisi",
                     "python-pyliblzma-0.5.3-1-1.pisi",
                     "pisi-2.4_alpha3-1-1.pisi",
                     "xz-4.999.9_beta143-1-1.pisi")
REPO_TEMPLATE = "http://packages.pardus.org.tr/pardus/2011/%s/i686/pisi-index.xml.xz"
FORCE_INSTALL = "http://svn.pardus.org.tr/uludag/trunk/pardus-upgrade/2009_to_2011.list"

from pisi.ui import *

def getWidget(page = None, title = ""):
    widget = QWidget()
    widget.title = title
    if page:
        page = page.Ui_Screen()
        page.setupUi(widget)
        widget.ui = page
    return widget

class UmMainScreen(QDialog, ui_mainscreen.Ui_UpgradeManager):

    def __init__(self, parent = None, step = 1):
        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.target_repo = REPO_TEMPLATE % 'stable'
        self.iface = Iface(self)

        self.msgbox = PMessageBox(self)
        self.msgbox.setStyleSheet(PMessageBox.Style)
        self.msgbox.enableOverlay()

        self.pageWidget = QPageWidget(self.widget_screens)
        self.layout.addWidget(self.pageWidget)

        self.button_next.clicked.connect(self.pageWidget.next)
        self.button_previous.clicked.connect(self.pageWidget.prev)

        # Threads
        self.thread_step_1 = PThread(self, self.step_1_start, self.step_1_end)
        self.thread_step_2 = PThread(self, self.step_2_start, self.step_2_end)
        self.thread_step_3 = PThread(self, self.step_3_start, self.step_3_end)

        # Update Page Title
        self.connect(self.pageWidget, SIGNAL("currentChanged()"), lambda:\
                     self.label_header.setText(self.pageWidget.getCurrentWidget().title))

        self.current_step = step

        if step == 1:
            self.thread_check = PThread(self, self.findMissingPackages, self.showResults)

            # Welcome
            self.pageWidget.createPage(
                    getWidget(ui_screen_1, "Welcome to Upgrade Manager..."))

            # Repo Selection
            self.pageWidget.createPage(
                    getWidget(ui_screen_2, "Select Upgrade Repository..."))

            # Check Results Page
            self.pageWidget.createPage(
                    getWidget(ui_screen_3, "Checking your system..."),
                    inMethod = self.checkSystem, outMethod = self.hideMessage)

            resultWidget = self.pageWidget.getWidget(2).ui
            resultWidget.c_package.hide()

            def updateButtons():
                if self.button_next.text() == "Next":
                    self.button_next.setText("Yes, Upgrade")
                    self.button_previous.setText("Cancel")
                    self.button_cancel.hide()
                else:
                    self.button_next.setText("Next")
                    self.button_previous.setText("Previous")
                    self.button_cancel.show()

            # Last Question
            self.pageWidget.createPage(
                    getWidget(ui_screen_4, ""), inMethod = updateButtons,
                                                outMethod= updateButtons)
        self._step_counter = 0

        # Progress Screen
        self.pageWidget.createPage(
                getWidget(ui_screen_5, "Upgrading the system..."), inMethod = self.upgradeStep_1)

        # Shortcut for Progress Screen UI
        # Get the last added page as progress page
        # After the first step completed, um will use just this page !
        self.ps = self.pageWidget.getWidget(self.pageWidget.count() - 1).ui

        if step == 2:
            self.upgradeStep_2()
        elif step == 3:
            self.upgradeStep_3()

    # Step 1 Method
    def checkSystem(self):
        self.showMessage("Checking your system...")
        repoWidget = self.pageWidget.getWidget(1).ui

        for repo in ('stable', 'devel', 'testing'):
            if getattr(repoWidget, repo).isChecked():
                self.target_repo = REPO_TEMPLATE % repo

        self.thread_check.start()

    # Step 1 Method
    def findMissingPackages(self):
        self.missing_packages = findMissingPackagesForDistupdate(self.target_repo)

    # Step 1 Method
    def showResults(self):
        resultWidget = self.pageWidget.getWidget(2).ui
        if self.missing_packages:
            resultWidget.package_list.clear()
            resultWidget.c_package.show()
            resultWidget.package_list.addItems(self.missing_packages)
        self.label_header.setText("Check results...")
        self.hideMessage()

    # Step 1 Method
    def upgradeStep_1(self):
        print 'PISI VERSION in STEP 1 is', pisi.__version__
        self.disableButtons()

        # To Animate it
        self.ps.steps.setMaximum(0)

        # Remove Repositories
        self.ps.progress.setFormat("Removing current repositories...")
        self.iface.removeRepos()

        # Install New Pisi and its dependencies
        # To keep install in given order we need to pass ignore_dep as True
        self.ps.progress.setFormat("Installing new package management system...")
        self.thread_step_1.start()

    # Step 1 Threaded Method
    def step_1_start(self):
        self.iface.installPackages(map(lambda x: ARA_FORM % x, REQUIRED_PACKAGES), ignore_dep = True)

    # Step 1 Threaded Method Finalize
    def step_1_end(self):
        # END OF Step 1 in Upgrade
        self.ps.progress.setFormat("Step 1 Completed")
        # STEP 1 Finishes at 10 percent
        self.ps.progress.setValue(10)

        # Write selected upgrade repository to a temporary file
        file('/tmp/target_repo','w').write(self.target_repo)

        # Cleanup Pisi DB
        cleanup_pisi()

        # I know this is ugly but we need to use new Pisi :(
        time.sleep(2)
        os.execv('/usr/bin/upgrade-manager', ['/usr/bin/upgrade-manager', '--start-from-step2'])

    # Step 2 Method
    def upgradeStep_2(self):
        self.disableButtons()
        self.ps.steps.setMaximum(0)
        self.ps.progress.setValue(10)
        self.ps.progress.setFormat("Upgrading to Pardus 2011...")

        self.thread_step_2.start()

    # Step 2 Threaded Method
    def step_2_start(self):
        # Lets Update !
        self.iface.upgradeSystem()

    # Step 2 Threaded Method Finalize
    def step_2_end(self):
        time.sleep(2)
        os.execv('/usr/bin/upgrade-manager', ['/usr/bin/upgrade-manager', '--start-from-step3'])

    # Step 3 Method
    def upgradeStep_3(self):
        self.disableButtons()
        self.ps.steps.setMaximum(0)
        self.ps.progress.setValue(70)
        self.ps.progress.setFormat("Configuring for Pardus 2011...")

    # Step 3 Threaded Method
    def step_3_start(self):
        # Lets Configure !
        self.iface.configureSystem()

    # Step 3 Threaded Method Finalize
    def step_3_end(self):
        # Step 4
        self.ps.progress.setFormat("Running Post Upgrade Operations...")

        # Migrate KDE Configs
        migrateKDE()

        # Migrate NetworkManager Configurations
        os.system("/usr/sbin/migrate-comar-network-profiles")

        # Migrate BootLoader conf
        migrateGrubconf('/boot/grub/grub.conf')

        # Time to reboot
        self.ps.progress.setFormat("Rebooting to the Pardus 2011...")
        time.sleep(3)
        os.system("reboot")

    # Shared Method
    def processNotify(self, event, notify):

        # print "PN:", event, "%%", notify

        if 'package' in notify:
            package = str(notify['package'].name)

            if event == installing:
                self.ps.status.setText("Installing: <b>%s</b>" % package)
            elif event == installed:
                self.ps.status.setText("Installed: <b>%s</b>" % package)
            elif event == upgraded:
                self.ps.status.setText("Upgraded: <b>%s</b>" % package)
            elif event == configuring:
                self.ps.status.setText("Configuring: <b>%s</b>" % package)
            elif event == configured:
                self.ps.status.setText("Configured: <b>%s</b>" % package)
            elif event == removing:
                self.ps.status.setText("Removing: <b>%s</b>" % package)
            elif event == removed:
                self.ps.status.setText("Removed: <b>%s</b>" % package)

            print "DEBUG:", self.ps.status.text()

            if event in (installed, upgraded) and self.current_step == 1:
                self.ps.progress.setValue(self.ps.progress.value() + 2)

            if self.current_step == 2 and event in (installed, upgraded):
                self._step_counter += 1
                # STEP 2 Finishes at 70 percent
                if self.iface._nof_packgages > 0:
                    self.ps.progress.setValue(10 + self._step_counter / (self.iface._nof_packgages / 60))

            if self.current_step == 3 and event == configured:
                self._step_counter += 1
                # STEP 3 Finishes at 100 percent
                if self.iface._nof_packgages > 0:
                    self.ps.progress.setValue(70 + self._step_counter / (self.iface._nof_packgages / 100))

    # Shared Method
    def updateProgress(self, raw):
        self.ps.status.setText("Downloading: <b>%s</b>" % raw['filename'])
        percent = raw['percent']

        if percent==100:
            self.ps.steps.setMaximum(0)
        else:
            self.ps.steps.setMaximum(100)
            self.ps.steps.setValue(percent)

    # Shared Method
    def showMessage(self, message):
        self.msgbox.busy.busy()
        self.msgbox.setMessage(message)
        if not self.msgbox.isVisible():
            self.msgbox.animate(start = MIDCENTER, stop = MIDCENTER)

    # Shared Method
    def hideMessage(self):
        if self.msgbox.isVisible():
            self.msgbox.animate(start = CURRENT, stop = CURRENT, direction = OUT)

    # Shared Method
    def disableButtons(self):
        for button in (self.button_cancel, self.button_previous, self.button_next):
            button.setEnabled(False)

