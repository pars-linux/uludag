#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
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
import subprocess
import tempfile

# Qt
import QTermWidget

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QIcon, QMessageBox, QMainWindow,QFileDialog
from PyQt4.QtCore import QFile


# UI
from gui.ui.main import Ui_MainWindow

# Dialogs
from gui.languages import LanguagesDialog
from gui.packages import PackagesDialog

# Progress Dialog
from gui.progress import Progress

# Repository tools
from repotools.packages import Repository, ExIndexBogus, ExPackageCycle, ExPackageMissing
from repotools.project import Project, ExProjectMissing, ExProjectBogus

import gettext
_ = lambda x:gettext.ldgettext("pardusman", x)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Terminal

        self.terminal = QTermWidget.QTermWidget()
        self.terminal.setHistorySize(-1)
        self.terminal.setScrollBarPosition(2)
        self.terminal.setColorScheme(2)
        self.terminalLayout.addWidget(self.terminal)
        self.terminal.show()

        # Arguments
        self.args = args

        # Project
        self.project = Project()

        # Package repository
        self.repo = None

        # Set icons
        self.setIcons()

        # Top toolbar
        self.connect(self.pushNew, SIGNAL("clicked()"), self.slotNew)
        self.connect(self.pushOpen, SIGNAL("clicked()"), self.slotOpen)
        self.connect(self.pushSave, SIGNAL("clicked()"), self.slotSave)
        self.connect(self.pushSaveAs, SIGNAL("clicked()"), self.slotSaveAs)
        self.connect(self.pushExit, SIGNAL("clicked()"), self.close)

        # Browse buttons
        self.connect(self.pushBrowseRepository, SIGNAL("clicked()"), self.slotBrowseRepository)
        self.connect(self.pushBrowseWorkFolder, SIGNAL("clicked()"), self.slotBrowseWorkFolder)
        self.connect(self.pushBrowsePluginPackage, SIGNAL("clicked()"), self.slotBrowsePluginPackage)
        self.connect(self.pushBrowseReleaseFiles, SIGNAL("clicked()"), self.slotBrowseReleaseFiles)

        # Bottom toolbar
        self.connect(self.pushUpdateRepo, SIGNAL("clicked()"), self.slotUpdateRepo)
        self.connect(self.pushSelectLanguages, SIGNAL("clicked()"), self.slotSelectLanguages)
        self.connect(self.pushSelectPackages, SIGNAL("clicked()"), self.slotSelectPackages)
        self.connect(self.pushMakeImage, SIGNAL("clicked()"), self.slotMakeImage)

        # Initialize
        self.initialize()

    def initialize(self):
        if len(self.args) == 2:
            self.slotOpen(self.args[1])

    def setIcons(self):
        # Top toolbar
        self.pushNew.setIcon(QIcon("document-new"))
        self.pushOpen.setIcon(QIcon("document-open"))
        self.pushSave.setIcon(QIcon("document-save"))
        self.pushSaveAs.setIcon(QIcon("document-save-as"))
        self.pushExit.setIcon(QIcon("dialog-close"))

        # Bottom toolbar
        self.pushUpdateRepo.setIcon(QIcon("view-refresh"))
        self.pushSelectPackages.setIcon(QIcon("games-solve"))
        self.pushSelectLanguages.setIcon(QIcon("applications-education-language"))
        self.pushMakeImage.setIcon(QIcon("media-playback-start"))

    def slotNew(self):
        """
            New button fires this function.
        """
        self.project = Project()
        self.loadProject()

    def slotOpen(self, filename=None):
        """
            Open button fires this function.
        """
        if not filename:
            filename = QFileDialog.getOpenFileName(self, _("Select project file"), ".", "*.xml")
        if filename:
            self.project = Project()
            try:
                self.project.open(unicode(filename))
            except ExProjectMissing:
                QMessageBox.error(self, _("Project file is missing."))
                return
            except ExProjectBogus:
                QMessageBox.error(self, _("Project file is corrupt."))
                return
            self.loadProject()

    def slotSave(self):
        """
            Save button fires this function.
        """
        if self.project.filename:
            self.updateProject()
            self.project.save()
        else:
            self.slotSaveAs()

    def slotSaveAs(self):
        """
            Save as button fires this function.
        """
        filename = QFileDialog.getSaveFileName(self, _("Save project"), "", "*.xml")
        if filename:
            self.project.filename = unicode(filename)
            self.slotSave()

    def slotBrowseRepository(self):
        """
            Browse repository button fires this function.
        """
        filename = QFileDialog.getOpenFileName(self, _("Select repository index"), ".", "pisi-index.xml*")
        if filename:
            filename = unicode(filename)
            if filename.startswith("/"):
                filename = "file://%s" % filename
            self.lineRepository.setText(filename)

    def slotBrowsePluginPackage(self):
        """
            Browse plugin package button fires this function.
        """
        filename = QFileDialog.getOpenFileName(self, _("Select plugin package"), ".", "*.pisi")
        if filename:
            self.linePluginPackage.setText(filename)

    def slotBrowseReleaseFiles(self):
        """
            Browse release files button fires this function.
        """
        directory = QFileDialog.getExistingDirectory(self, "")
        if directory:
            self.lineReleaseFiles.setText(directory)

    def slotBrowseWorkFolder(self):
        """
            Browse work folder button fires this function.
        """
        directory = QFileDialog.getExistingDirectory(self, "")
        if directory:
            self.lineWorkFolder.setText(directory)

    def slotSelectLanguages(self):
        """
            Select language button fires this function.
        """
        dialog = LanguagesDialog(self, self.project.selected_languages)
        if dialog.exec_():
            self.project.default_language = dialog.languages[0]
            self.project.selected_languages = dialog.languages

    def slotSelectPackages(self):
        """
            Select package button fires this function.
        """
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        dialog = PackagesDialog(self, self.repo, self.project.selected_packages, self.project.selected_components)
        if dialog.exec_():
            self.project.selected_packages = dialog.packages
            self.project.selected_components = dialog.components
            self.project.all_packages = dialog.all_packages

    def slotUpdateRepo(self):
        """
            Update repository button fires this function.
        """
        if not self.checkProject():
            return
        self.updateRepo()

    def slotMakeImage(self):
        """
            Make image button fires this function.
        """
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return
        temp_project = tempfile.NamedTemporaryFile(delete=False)
        self.project.save(temp_project.name)
        app_path = self.args[0]
        if app_path[0] != "/":
            app_path = os.path.join(os.getcwd(), app_path)

        # Konsole Mode
        # cmd = 'konsole --noclose --workdir "%s" -e "%s" make "%s"' % (os.getcwd(), app_path, temp_project.name)
        # subprocess.Popen(["xdg-su", "-u", "root", "-c", cmd])

        cmd = '%s make %s' % (app_path, temp_project.name)
        self.terminal.sendText("sudo %s\n" % cmd)
        self.terminal.setFocus()

    def checkProject(self):
        """
            Checks required fields for the project.
        """
        if not len(self.lineTitle.text()):
            QMessageBox.error(self, _("Image title is missing."))
            return False
        if not len(self.lineRepository.text()):
            QMessageBox.error(self, _("Repository URL is missing."))
            return False
        if not len(self.lineWorkFolder.text()):
            QMessageBox.error(self, _("Work folder is missing."))
            return False
        return True

    def updateProject(self):
        """
            Updates project information.
        """
        self.project.title = unicode(self.lineTitle.text())
        self.project.repo_uri = unicode(self.lineRepository.text())
        self.project.work_dir = unicode(self.lineWorkFolder.text())
        self.project.release_files = unicode(self.lineReleaseFiles.text())
        self.project.plugin_package = unicode(self.linePluginPackage.text())
        self.project.extra_params = unicode(self.lineParameters.text())
        self.project.type = ["install", "live"][self.comboType.currentIndex()]
        self.project.squashfs_comp_type = ["GZIP", "LZMA"][self.comboCompression.currentIndex()]
        self.project.media = ["cd", "dvd", "usb", "custom"][self.comboSize.currentIndex()]

    def loadProject(self):
        """
            Loads project information.
        """
        self.lineTitle.setText(unicode(self.project.title))
        self.lineRepository.setText(unicode(self.project.repo_uri))
        self.lineWorkFolder.setText(unicode(self.project.work_dir))
        self.lineReleaseFiles.setText(unicode(self.project.release_files))
        self.linePluginPackage.setText(unicode(self.project.plugin_package))
        self.lineParameters.setText(unicode(self.project.extra_params))
        self.comboType.setCurrentIndex(["install", "live"].index(self.project.type))
        self.comboCompression.setCurrentIndex(["GZIP", "LZMA"].index(self.project.squashfs_comp_type))
        self.comboSize.setCurrentIndex(["cd", "dvd", "usb", "custom"].index(self.project.media))

    def updateRepo(self, update_repo=True):
        """
            Fetches package index and retrieves list of package and components.
        """
        # Progress dialog
        self.progress = Progress(self)
        # Update project
        self.updateProject()
        # Get repository
        try:
            self.repo = self.project.get_repo(self.progress, update_repo=update_repo)
        except ExIndexBogus, e:
            self.progress.finished()
            QMessageBox.error(self, _("Unable to load package index. URL is wrong, or file is corrupt."))
            return False
        except ExPackageCycle, e:
            self.progress.finished()
            cycle = " > ".join(e.args[0])
            QMessageBox.error(self, _("Package index has errors. Cyclic dependency found:\n  %s.") % cycle)
            return False
        except ExPackageMissing, e:
            self.progress.finished()
            QMessageBox.error(self, _("Package index has errors. '%s' depends on non-existing '%s'.") % e.args)
            return False
        missing_components, missing_packages = self.project.get_missing()
        if len(missing_components):
            QMessageBox.information(self, _("There are missing components. Removing."))
            for component in missing_components:
                if component in self.project.selected_components:
                    self.project.selected_components.remove(component)
            return self.updateRepo(update_repo=False)
        if len(missing_packages):
            QMessageBox.information(self, _("There are missing packages. Removing."))
            for package in missing_packages:
                if package in self.project.selected_packages:
                    self.project.selected_packages.remove(package)
            return self.updateRepo(update_repo=False)
        return True
