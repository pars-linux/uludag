#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import SIGNAL, SLOT, Qt

# KDE Stuff
from PyKDE4.kdeui import KMessageBox, KIcon
from PyKDE4.kio import KFileDialog, KFile
from PyKDE4.kdecore import *

from ui import Ui_mainForm
from uilanguage import Ui_languageForm
from uipackages import Ui_packagesForm

from project import Project
from packages import Repository

class LanguageForm(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_languageForm()
        self.ui.setupUi(self)

        # TODO: i18n stuff
        self.supported_languages = {"ca_ES": "Catalan",
                                    "de_DE": "Deutsch",
                                    "en_US": "English",
                                    "es_ES": "Spanish",
                                    "fr_FR": "French",
                                    "it_IT": "Italian",
                                    "nl_NL": "Dutch",
                                    "pl_PL": "Polish",
                                    "pt_BR": "Brazilian Portuguese",
                                    "sv_SE": "Svenska",
                                    "tr_TR": "Turkish"}

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)

    def setLanguages(self, languages=[]):
        selected = self.ui.kactionselectorLang.selectedListWidget()
        available = self.ui.kactionselectorLang.availableListWidget()
        selected.clear()
        for code in languages:
            label = self.supported_languages[code]
            item = QtGui.QListWidgetItem(label)
            item.code = code
            selected.addItem(item)
        for code, label in self.supported_languages.iteritems():
            if code not in languages:
                item = QtGui.QListWidgetItem(label)
                item.code = code
                available.addItem(item)

    def getLanguages(self):
        selected = self.ui.kactionselectorLang.selectedListWidget()
        languages = []
        for i in xrange(selected.count()):
            item = selected.item(i)
            languages.append(item.code)
        return languages


class PackagesForm(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_packagesForm()
        self.ui.setupUi(self)

        self.repo = None

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)

    def setRepo(self, repo):
        self.repo = repo
        self.repo.parse_index()
        # Packages
        self.ui.listPackages.clear()
        for package in self.repo.packages.keys():
            item = QtGui.QListWidgetItem(package)
            self.ui.listPackages.addItem(item)
        # Components
        self.ui.listComponents.clear()
        for component in self.repo.components.keys():
            item = QtGui.QListWidgetItem(component)
            self.ui.listComponents.addItem(item)

    def getRepo(self):
        return self.repo

    def setSelectedPackages(self, packages):
        pass

    def setAllPackages(self, packages):
        pass

    def getSelectedPackages(self):
        return []

    def getAllPackages(self):
        return []

    def setSelectedComponents(self, components):
        pass

    def getSelectedComponents(self):
        return []


class MainForm(QtGui.QWidget):
    def __init__(self, parent, app=None):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainForm()
        self.app = app

        # Create language selector
        self.languageSelectionDialog = LanguageForm(self)

        # Create package selector
        self.packagesSelectionDialog = PackagesForm(self)

        # Project
        self.project = Project()

        # Create attributes
        self.repo_uri = None
        self.work_dir = None
        self.plug_dir = None
        self.rl_files = None

        # Setup ui
        self.ui.setupUi(self)

        # Set icons
        self.setIcons()

        # Set connections
        self.connect(self.ui.pushButtonNew, SIGNAL("clicked()"), self.slotProjectNew)
        self.connect(self.ui.pushButtonLoad, SIGNAL("clicked()"), self.slotProjectLoad)
        self.connect(self.ui.pushButtonSave, SIGNAL("clicked()"), self.slotProjectSave)
        self.connect(self.ui.pushButtonSaveAs, SIGNAL("clicked()"), self.slotProjectSaveAs)

        self.connect(self.ui.pushButtonBrowseRepo, SIGNAL("clicked()"), self.slotBrowseRepo)
        self.connect(self.ui.pushButtonBrowseWork, SIGNAL("clicked()"), self.slotBrowseWork)
        self.connect(self.ui.pushButtonBrowsePlugin, SIGNAL("clicked()"), self.slotBrowsePlugin)
        self.connect(self.ui.pushButtonBrowseRelease, SIGNAL("clicked()"), self.slotBrowseRelease)

        self.connect(self.ui.pushButtonLanguages, SIGNAL("clicked()"), self.slotLanguages)
        self.connect(self.ui.pushButtonPackages, SIGNAL("clicked()"), self.slotPackages)

    def slotProjectNew(self):
        self.project.reset()

    def slotProjectLoad(self):
        project_file = KFileDialog.getOpenFileName(KUrl('.'), "*.xml", self, i18n("Select project file"))
        if project_file:
            ret = self.project.open(unicode(project_file))
            if ret:
                # FIXME: Show error dialog
                pass
            else:
                # Title, repo, etc.
                self.ui.lineEditTitle.setText(self.project.title)
                self.ui.lineEditParams.setText(self.project.extra_params)
                self.ui.lineEditRepo.setText(self.project.repo_uri)
                self.ui.lineEditRelease.setText(self.project.release_files)
                self.ui.lineEditPlugin.setText(self.project.plugin_package)
                self.ui.lineEditWorkdir.setText(self.project.work_dir)
                # Type
                if self.project.type == "install":
                    self.ui.comboBoxType.setCurrentIndex(0)
                elif self.project.type == "live":
                    self.ui.comboBoxType.setCurrentIndex(1)
                elif self.project.type == "package":
                    self.ui.comboBoxType.setCurrentIndex(2)
                # Media
                if self.project.media == "cd":
                    self.ui.comboBoxSize.setCurrentIndex(0)
                elif self.project.media == "dvd":
                    self.ui.comboBoxSize.setCurrentIndex(1)
                elif self.project.media == "usb":
                    self.ui.comboBoxSize.setCurrentIndex(2)
                elif self.project.media == "custom":
                    self.ui.comboBoxSize.setCurrentIndex(3)
                # Languages
                self.languageSelectionDialog.setLanguages(self.project.selected_languages)
                # Selected Packages
                self.packagesSelectionDialog.setSelectedPackages(self.project.selected_packages)
                # All Packages
                self.packagesSelectionDialog.setAllPackages(self.project.all_packages)
                # Selected Components
                self.packagesSelectionDialog.setSelectedComponents(self.project.selected_components)

    def slotProjectSave(self):
        if self.project.filename:
            # Title, repo, etc.
            self.project.title = unicode(self.ui.lineEditTitle.text())
            self.project.extra_params = unicode(self.ui.lineEditParams.text())
            self.project.repo_uri = unicode(self.ui.lineEditRepo.text())
            self.project.release_files = unicode(self.ui.lineEditRelease.text())
            self.project.plugin_package = unicode(self.ui.lineEditPlugin.text())
            self.project.work_dir = unicode(self.ui.lineEditWorkdir.text())
            # Type
            if self.ui.comboBoxType.currentIndex() == 0:
                self.project.type = "install"
            elif self.ui.comboBoxType.currentIndex() == 1:
                self.project.type = "live"
            elif self.ui.comboBoxType.currentIndex() == 2:
                self.project.type = "package"
            # Media
            if self.ui.comboBoxSize.currentIndex() == 0:
                self.project.media = "cd"
            elif self.ui.comboBoxSize.currentIndex() == 1:
                self.project.media = "dvd"
            elif self.ui.comboBoxSize.currentIndex() == 2:
                self.project.media = "usb"
            elif self.ui.comboBoxSize.currentIndex() == 3:
                self.project.media = "custom"
            # Save file
            self.project.save()
        else:
            self.slotProjectSaveAs()

    def slotProjectSaveAs(self):
        project_file = KFileDialog.getSaveFileName(KUrl('.'), "*.xml", self, i18n("Select project file"))
        if project_file:
            self.project.filename = project_file
            self.slotProjectSave()

    def slotLanguages(self):
        if self.languageSelectionDialog.exec_():
            self.project.selected_languages = self.languageSelectionDialog.getLanguages()

    def slotPackages(self):
        # FIXME: Check URI/WorkDir
        if not self.packagesSelectionDialog.getRepo():
            repo = Repository(self.project.repo_uri, self.project.work_dir)
            self.packagesSelectionDialog.setRepo(repo)
        if self.packagesSelectionDialog.exec_():
            self.project.selected_packages = self.packagesSelectionDialog.getSelectedPackages()
            self.project.all_packages = self.packagesSelectionDialog.getAllPackages()
            self.project.selected_components = self.packagesSelectionDialog.getSelectedComponents()

    def slotBrowseRepo(self):
        self.repo_uri = KFileDialog.getOpenFileName(KUrl('.'), "pisi-index.xml*", self, i18n("Select repository index"))
        if self.repo_uri:
            self.ui.lineEditRepo.setText(self.repo_uri)

    def slotBrowsePlugin(self):
        self.plug_dir = KFileDialog.getOpenFileName(KUrl('.'), "*.pisi", self, i18n("Select plugin package"))
        if self.plug_dir:
            self.ui.lineEditPlugin.setText(self.plug_dir)

    def slotBrowseRelease(self):
        file_dialog = KFileDialog(KUrl(), "", self)

        file_dialog.setMode(KFile.Directory)

        self.rl_files = file_dialog.getOpenFileName(KUrl(), "", self, i18n("Select the directory for the release files"))
        if self.rl_files:
            self.ui.lineEditRelease.setText(self.rl_files)

    def slotBrowseWork(self):
        self.work_dir = KFileDialog.getOpenFileName()
        if self.work_dir:
            self.ui.lineEditWorkdir.setText(self.work_dir)

    def setIcons(self):
        # Set pushbutton icons
        self.ui.pushButtonNew.setIcon(KIcon('document-new'))
        self.ui.pushButtonLoad.setIcon(KIcon('document-open'))
        self.ui.pushButtonSave.setIcon(KIcon('document-save'))
        self.ui.pushButtonAbout.setIcon(KIcon('help-about'))
        self.ui.pushButtonUpdate.setIcon(KIcon('view-refresh'))
        self.ui.pushButtonPackages.setIcon(KIcon('games-solve'))
        self.ui.pushButtonSaveAs.setIcon(KIcon('document-save-as'))
        self.ui.pushButtonCreate.setIcon(KIcon('media-playback-start'))
        self.ui.pushButtonLanguages.setIcon(KIcon('applications-education-language'))
