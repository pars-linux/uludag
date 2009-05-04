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

class LanguageForm(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_languageForm()
        self.ui.setupUi(self)

        # TODO: i18n stuff
        self.supported_languages = {"Catalan" : "ca_ES",
                                    "Deutsch" : "de_DE",
                                    "English" : "en_US",
                                    "Spanish" : "es_ES",
                                    "French" : "fr_FR",
                                    "Italian" : "it_IT",
                                    "Dutch" : "nl_NL",
                                    "Polish" : "pl_PL",
                                    "Brazilian Portuguese" : "pt_BR",
                                    "Svenska" : "sv_SE",
                                    "Turkish" : "tr_TR"}

        available = self.ui.kactionselectorLang.availableListWidget()
        available.addItems(self.supported_languages.keys())

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)


class PackagesForm(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_packagesForm()
        self.ui.setupUi(self)

        self.connect(self.ui.buttonBox, SIGNAL("accepted()"), self.accept)
        self.connect(self.ui.buttonBox, SIGNAL("rejected()"), self.reject)


class MainForm(QtGui.QWidget):
    def __init__(self, parent, app=None):
        QtGui.QWidget.__init__(self, parent)

        # Create the ui
        self.ui = Ui_mainForm()
        self.app = app

        # Create language selector
        self.languageSelectionDialog = LanguageForm(self)

        # Create package selector
        self.packageSelectionDialog = PackagesForm(self)

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
        self.connect(self.ui.pushButtonBrowseRepo, SIGNAL("clicked()"), self.slotBrowseRepo)
        self.connect(self.ui.pushButtonBrowseWork, SIGNAL("clicked()"), self.slotBrowseWork)
        self.connect(self.ui.pushButtonBrowsePlugin, SIGNAL("clicked()"), self.slotBrowsePlugin)
        self.connect(self.ui.pushButtonBrowseRelease, SIGNAL("clicked()"), self.slotBrowseRelease)
        self.connect(self.ui.pushButtonLanguages, SIGNAL("clicked()"), self.slotLanguages)
        self.connect(self.ui.pushButtonLanguages, SIGNAL("clicked()"), self.slotLanguages)
        self.connect(self.ui.pushButtonPackages, SIGNAL("clicked()"), self.slotPackages)

    def slotLanguages(self):
        if self.languageSelectionDialog.exec_():
            print "ok"
        else:
            print "cancel"

    def slotPackages(self):
        if self.packageSelectionDialog.exec_():
            print "ok"
        else:
            print "cancel"

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
        self.ui.pushButtonLoad.setIcon(KIcon('document-open'))
        self.ui.pushButtonSave.setIcon(KIcon('document-save'))
        self.ui.pushButtonAbout.setIcon(KIcon('help-about'))
        self.ui.pushButtonUpdate.setIcon(KIcon('view-refresh'))
        self.ui.pushButtonPackages.setIcon(KIcon('games-solve'))
        self.ui.pushButtonSaveAs.setIcon(KIcon('document-save-as'))
        self.ui.pushButtonCreate.setIcon(KIcon('media-playback-start'))
        self.ui.pushButtonLanguages.setIcon(KIcon('applications-education-language'))
