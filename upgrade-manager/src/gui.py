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

# System
import os
import re
import sys
import time
import urlgrabber

# PyQt
from PyQt4.QtGui import QDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMessageBox
from PyQt4.QtCore import SIGNAL, QTimer

# UI Files
from ui import ui_screen_1
from ui import ui_screen_2
from ui import ui_screen_3
from ui import ui_screen_4
from ui import ui_screen_5
from ui import ui_mainscreen

# PDS Imports
from pds import Pds
from pds.gui import *
from pds.thread import PThread
from pds.qpagewidget import QPageWidget
from pds.qprogressindicator import QProgressIndicator

# Pisi
import pisi
from pisi.ui import *
from backend import Iface
from backend import SimpleLogger
from backend import cleanup_pisi

# Helper & Migrate Methods
from migratekde import migrateKDE
from repohelper import DistupdatePlanner
from migrategrubconf import migrateGrubconf

# Translations
_pds = Pds('upgrade-manager', debug = False)
_ = _pds.i18n

# Constants
ARA_FORM = "http://cekirdek.pardus.org.tr/~onur/2009to2011/packages/%s"
REQUIRED_PACKAGES = ("libuser-0.57.1-1-1.pisi",
                     "python-pyliblzma-0.5.3-1-1.pisi",
                     "pisi-2.4_alpha3-1-1.pisi",
                     "xz-4.999.9_beta143-1-1.pisi")
REPO_TEMPLATE = "http://packages.pardus.org.tr/pardus/2011/%s/i686/pisi-index.xml.xz"
FORCE_INSTALL = "http://svn.pardus.org.tr/uludag/trunk/pardus-upgrade/2009_to_2011.list"

def salt_text(data):
    data = unicode(data)
    p = re.compile(r'<.*?>')
    return p.sub('', data)

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

        self.logger = SimpleLogger()
        self.log = self.logger.log

        self.target_repo = REPO_TEMPLATE % 'stable'
        self.iface = Iface(self)

        self.connect(self.iface, SIGNAL("notify(PyQt_PyObject)"), self.showMessage)

        self.msgbox = PMessageBox(self)
        self.msgbox.setStyleSheet("color:white;")
        self.msgbox.enableOverlay()
                                                          # Just for Fun :)
        self.pageWidget = QPageWidget(self.widget_screens)# , direction = 'ttb')
        self.layout.addWidget(self.pageWidget)

        self.button_next.clicked.connect(self.pageWidget.next)
        self.button_previous.clicked.connect(self.pageWidget.prev)
        self.button_cancel.clicked.connect(self.reject)

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
                    getWidget(ui_screen_1, _("Welcome to Upgrade Manager...")))

            # Repo Selection
            self.pageWidget.createPage(
                    getWidget(ui_screen_2, _("Select Upgrade Repository...")))

            # Check Results Page
            self.pageWidget.createPage(
                    getWidget(ui_screen_3, _("Checking your system...")),
                    inMethod = self.checkSystem, outMethod = self.hideMessage)

            resultWidget = self.pageWidget.getWidget(2).ui
            resultWidget.widget.hide()

            def updateButtons():
                if self.button_next.text() == _("Next"):
                    self.button_next.setText(_("Yes, Upgrade"))
                    self.button_previous.setText(_("Cancel"))
                    self.button_cancel.hide()
                else:
                    self.button_next.setText(_("Next"))
                    self.button_previous.setText(_("Previous"))
                    self.button_cancel.show()

            # Last Question
            self.pageWidget.createPage(
                    getWidget(ui_screen_4, ""), inMethod = updateButtons,
                                                outMethod= updateButtons)
        self._step_counter = 0

        # Progress Screen
        self.pageWidget.createPage(
                getWidget(ui_screen_5, _("Upgrading the system...")), inMethod = self.upgradeStep_1)

        # Shortcut for Progress Screen UI
        # Get the last added page as progress page
        # After the first step completed, um will use just this page !
        self.ps = self.pageWidget.getWidget(self.pageWidget.count() - 1).ui

        # Busy indicator to Progress Screen
        self.ps.busy = QProgressIndicator(self)
        self.ps.busy.hide()
        self.ps.layout.addWidget(self.ps.busy)

        if step == 2:
            self.upgradeStep_2()
        elif step == 3:
            self.upgradeStep_3()

    # Step 1 Method
    def checkSystem(self):
        self.showMessage(_("Checking your system..."))
        self.log("CHECKING CURRENT PACKAGES", "GUI")
        repoWidget = self.pageWidget.getWidget(1).ui

        for repo in ('stable', 'devel', 'testing'):
            if getattr(repoWidget, repo).isChecked():
                self.target_repo = REPO_TEMPLATE % repo

        if repoWidget.manual.isChecked():
            self.target_repo = str(repoWidget.manualRepo.text())

        self.thread_check.start()

    # Step 1 Method
    def findMissingPackages(self):
        updatePlan = DistupdatePlanner(nextRepoUri = self.target_repo, Debug = True, forceInstallUri = FORCE_INSTALL)
        updatePlan.plan()
        self.missing_packages = updatePlan.missingPackages
        try:
            self.missing_packages.remove("upgrade-manager")
        except ValueError:
            pass
        self.required_diskspace = updatePlan.sizeOfNeededTotalSpace
        self.planner_successful = updatePlan.successful

    # Step 1 Method
    def showResults(self):
        resultWidget = self.pageWidget.getWidget(2).ui
        free_size = os.statvfs('/').f_bavail * os.statvfs('/').f_bsize
        if not self.planner_successful:
            self.hideMessage()
            QMessageBox.critical(self, _("Critical Error"),
                                       _("An error ocurred while planning the upgrade procedure, "\
                                         "this is usually caused by faulty Network Connection or "\
                                         "wrong repo address."))
            self.pageWidget.prev()
            return
        if self.required_diskspace + 200000000 > free_size:
            self.hideMessage()
            QMessageBox.critical(self, _("Not enough free space"),
                                       _("This upgrade requires at least <b>%s MB</b> free space, "\
                                         "please use another repository or remove some files "\
                                         "to make a space for upgrade operation.") % \
                                       str(self.required_diskspace / (1024 ** 2)))
            self.pageWidget.prev()
            return
        else:
            resultWidget.widget.show()
            if self.missing_packages:
                resultWidget.package_list.clear()
                resultWidget.package_list.addItems(self.missing_packages)
            self.log("MISSING PACKAGES FOUND: %s" % ','.join(self.missing_packages), "GUI")
        self.label_header.setText(_("Check results..."))
        self.hideMessage()

    # Step 1 Method
    def upgradeStep_1(self):
        self.log("STARTING TO STEP 1", "GUI")
        self.log('PISI VERSION in STEP 1 is %s' % str(pisi.__version__),"GUI")
        self.disableButtons()

        # To Animate it
        self.ps.steps.hide()
        self.ps.busy.busy()

        # Install New Pisi and its dependencies
        # To keep install in given order we need to pass ignore_dep as True
        self.thread_step_1.start()

    # Step 1 Threaded Method
    def step_1_start(self):
        resultWidget = self.pageWidget.getWidget(2).ui
        if resultWidget.remove_packages.isChecked():
            self.ps.progress.setFormat(_("Removing unsupported packages..."))
            self.iface.removePackages(self.missing_packages)

        self.ps.progress.setFormat(_("Installing new package management system..."))
        self.iface.removeRepos()
        self.iface.installPackages(map(lambda x: ARA_FORM % x, REQUIRED_PACKAGES), ignore_dep = True)

    # Step 1 Threaded Method Finalize
    def step_1_end(self):
        # END OF Step 1 in Upgrade
        self.log("STEP 1 COMPLETED", "GUI")
        self.ps.progress.setFormat(_("Step 1 Completed"))

        # STEP 1 Finishes at 10 percent
        self.ps.progress.setValue(10)

        # Write selected upgrade repository to a temporary file
        try:
            file('/tmp/target_repo','w').write(self.target_repo)
        except:
            self.log("TARGET REPO STORE FAILED, USING stable AS DEFAULT", "GUI")

        # Mark the step
        self.logger.markStep(2)

        # Cleanup Pisi DB
        cleanup_pisi()

        # Just wait a little bit.
        time.sleep(2)

        # Re-launch the um for 2. step
        os.execv('/usr/bin/upgrade-manager', ['/usr/bin/upgrade-manager', '--start-from-step2'])

    # Step 2 Method
    def upgradeStep_2(self):
        self.log("STARTING TO STEP 2", "GUI")
        self.disableButtons()
        self.ps.steps.hide()
        self.ps.busy.busy()
        self.ps.progress.setValue(10)
        self.ps.progress.setFormat(_("Upgrading to Pardus 2011..."))

        self.thread_step_2.start()

    # Step 2 Threaded Method
    def step_2_start(self):
        # Lets Update !
        self._step2_success = self.iface.upgradeSystem()

    # Step 2 Threaded Method Finalize
    def step_2_end(self):
        if not self._step2_success:
            QMessageBox.critical(self, _("Critical Error"),
                                       _("An error ocurred while upgrading the system, "\
                                         "this is usually caused by a repository problem.\n"\
                                         "Please try again later."))
            sys.exit(1)

        self.log("STEP 2 COMPLETED", "GUI")
        # Mark the step
        self.logger.markStep(3)

        # Just wait a little bit.
        time.sleep(2)

        # Re-launch the um for 3. step
        os.execv('/usr/bin/upgrade-manager', ['/usr/bin/upgrade-manager', '--start-from-step3'])

    # Step 3 Method
    def upgradeStep_3(self):
        self.log("STARTING TO STEP 3", "GUI")
        self.disableButtons()
        self.ps.steps.hide()
        self.ps.busy.busy()
        self.ps.progress.setValue(70)
        self.ps.progress.setFormat(_("Configuring for Pardus 2011..."))

        self.thread_step_3.start()

    # Step 3 Threaded Method
    def step_3_start(self):
        # Lets Configure !
        self.iface.configureSystem()

    # Step 3 Threaded Method Finalize
    def step_3_end(self):
        self.log("STEP 3 COMPLETED", "GUI")
        # Step 4
        self.ps.progress.setFormat(_("Running Post Upgrade Operations..."))

        # Migrate KDE Configs
        self.log("RUNNING migrateKDE SCRIPT...", "GUI")
        migrateKDE()
        self.log("migrateKDE SCRIPT COMPLETED.", "GUI")

        # Migrate NetworkManager Configurations
        self.log("MIGRATING NETWORK PROFILES...", "GUI")
        os.system("/usr/sbin/migrate-comar-network-profiles")
        self.log("NETWORK PROFILES MIGRATED.", "GUI")

        # Migrate BootLoader conf
        self.log("MIGRATING grub.conf...", "GUI")
        migrateGrubconf('/boot/grub/grub.conf')
        self.log("grub.conf MIGRATED", "GUI")

        # Time to reboot
        self.ps.progress.setFormat(_("Rebooting to the Pardus 2011..."))

        # Finalize log.
        self.log("STEP 4 COMPLETED", "GUI")

        # Mark the step
        self.logger.markStep(4)

        # Just wait a little bit.
        time.sleep(3)

        # Time to reboot to Pardus 2011
        self.log("REBOOTING TO Pardus 2011...", "GUI")
        self.logger.close()
        os.system("reboot")

    # Shared Method
    def processNotify(self, event, notify):

        # print "PN:", event, "%%", notify

        self.hideMessage()

        if 'package' in notify:
            package = str(notify['package'].name)

            if event == installing:
                self.ps.status.setText(_("Installing: <b>%s</b>") % package)
            elif event == installed:
                self.ps.status.setText(_("Installed: <b>%s</b>") % package)
            elif event == upgraded:
                self.ps.status.setText(_("Upgraded: <b>%s</b>") % package)
            elif event == configuring:
                self.ps.status.setText(_("Configuring: <b>%s</b>") % package)
            elif event == configured:
                self.ps.status.setText(_("Configured: <b>%s</b>") % package)
            elif event == removing:
                self.ps.status.setText(_("Removing: <b>%s</b>") % package)
            elif event == removed:
                self.ps.status.setText(_("Removed: <b>%s</b>") % package)

            self.log(salt_text(self.ps.status.text()), "PISI")

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
        self.ps.status.setText(_("Downloading: <b>%s</b>") % raw['filename'])
        percent = raw['percent']

        if percent==100:
            self.ps.steps.hide()
            self.ps.busy.busy()
        else:
            self.ps.steps.setValue(percent)
            self.ps.steps.show()
            self.ps.busy.hide()

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

    # Shared Method
    def reject(self):
        self.log("USER REJECTED", "GUI")
        for thread in (self.thread_step_1, self.thread_step_2, self.thread_step_3):
            if thread.isRunning():
                self.log("REQUEST IGNORED PISI IS STILL RUNNING !", "GUI")
                return
        self.log("REQUEST ACCEPTED, EXITING", "GUI")
        QDialog.reject(self)

