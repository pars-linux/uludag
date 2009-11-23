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
import tempfile

# Qt
import QTermWidget

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QIcon, QMessageBox, QMainWindow, QFileDialog, QListWidgetItem
from PyQt4.QtCore import QFile


# UI
from gui.ui.main import Ui_MainWindow

# Dialogs
from gui.languages import LanguagesDialog
from gui.packages import PackagesDialog
from gui.packagecollection import PackageCollectionDialog

# Progress Dialog
from gui.progress import Progress

# Repository tools
from repotools.packages import Repository, ExIndexBogus, ExPackageCycle, ExPackageMissing
from repotools.project import Project, ExProjectMissing, ExProjectBogus

import gettext
_ = lambda x:gettext.ldgettext("pardusman", x)

class PackageCollectionListItem(QListWidgetItem):
    def __init__(self, parent, collection):
        QListWidgetItem.__init__(self, parent)
        self.collection = collection
        print "list item collection.title%s" % collection.title
        self.setText(collection.title)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, args):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.title = "Pardusman"
        # Terminal

        self.terminal = QTermWidget.QTermWidget()
        self.terminal.setHistorySize(-1)
        self.terminal.setScrollBarPosition(2)
        self.terminal.setColorScheme(2)
        self.terminalLayout.addWidget(self.terminal)
        self.terminal.show()

        self.collectionFrame.hide()

        # Arguments
        self.args = args

        # Project
        self.project = Project()

        # Package repository
        self.repo = None

        # Package Selection collections
        self.collections = None

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

        # Change Package Selection
        self.connect(self.pushAddCollection, SIGNAL("clicked()"),self.slotAddPackageCollection)
        self.connect(self.pushModifyCollection, SIGNAL("clicked()"),self.slotModifyPackageCollection)
        self.connect(self.pushRemoveCollection, SIGNAL("clicked()"),self.slotRemovePackageCollection)
        self.connect(self.pushSetDefaultCollection, SIGNAL("clicked()"),self.slotSetDefaultCollection)
        self.connect(self.comboSize, SIGNAL("currentIndexChanged(int)"), self.slotShowPackageCollection)
        self.connect(self.listPackageCollection, SIGNAL("itemClicked(QListWidgetItem *)"),self.slotClickedCollection)

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

    def initializeRepo(self):
        if not self.repo:
            if not self.checkProject():
                return
            if not self.updateRepo():
                return

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
                QMessageBox.warning(self, self.title, _("Project file is missing."))
                return
            except ExProjectBogus:
                QMessageBox.warning(self, self.title, _("Project file is corrupt."))
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

    def slotAddPackageCollection(self):
        if not self.repo:
            self.initializeRepo()

        dialog = PackageCollectionDialog(self, self.repo)
        if dialog.exec_():
            item = PackageCollectionListItem(self.listPackageCollection, dialog.collection)
            self.project.package_collections.append(item.collection)

            if self.listPackageCollection.count() == 1:
                item.collection.setDefault("True")


        self.updateCollection()

    def slotModifyPackageCollection(self):
        index = self.listPackageCollection.currentRow()
        item = self.listPackageCollection.item(index)
        #print "self.repo:%s" % self.repo.base_uri
        #print "item.collection"
        if not self.repo:
            self.initializeRepo()

        dialog = PackageCollectionDialog(self, self.repo, item.collection)
        if dialog.exec_():
            if not item.collection.uniqueTag.__eq__(dialog.collection.uniqueTag):
                print "item.setText"
                item.setText(dialog.collection.title)
            item.collection = dialog.collection

        self.updateCollection()

    def slotRemovePackageCollection(self):
        for item in self.listPackageCollection.selectedItems():
            self.listPackageCollection.takeItem(self.listPackageCollection.row(item))

        self.updateCollection()

    def slotClickedCollection(self, item):
#        if not self.listPackageCollection.count():
#            self.pushSetDefaultCollection.setEnabled(False)
#        elif self.listPackageCollection.count() == 1:
#            self.listPackageCollection.currentRow().collection.setDefault("True")
#            self.pushSetDefaultCollection.setChecked(False)
#        else:
        print "item.collection.name %s is default:%s" % (item.collection.title, item.collection.default)

        if item.collection.default == "True":
            if not self.pushSetDefaultCollection.isChecked():
                self.pushSetDefaultCollection.setChecked(True)
        else:
            if self.pushSetDefaultCollection.isChecked():
                self.pushSetDefaultCollection.setChecked(False)

    def slotSetDefaultCollection(self):
        if not self.listPackageCollection.currentItem().collection.default:
            self.listPackageCollection.currentItem().collection.setDefault("True")
            currentIndex = self.listPackageCollection.currentRow()
            for index in xrange(self.listPackageCollection.count()):
                if index == currentIndex:
                    pass
                else:
                    self.listPackageCollection.item(index).collection.default = ""

            self.pushSetDefaultCollection.setChecked(True)


    def slotShowPackageCollection(self, index):
        if self.comboSize.currentIndex() == 1:
            self.collectionFrame.show()
            self.pushSelectPackages.hide()
        else:
            self.collectionFrame.hide()
            self.pushSelectPackages.show()

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

    def updateCollection(self):
        #if not self.project.package_collections:
        #    print "cd kurulumu"
        #    self.listPackageCollection.clear()
        if not self.project.media.__eq__("dvd"):
            print "dvd kurulum degil clear"
            self.listPackageCollection.clear()
        else:
            self.project.package_collections = []
            for index in xrange(self.listPackageCollection.count()):
                self.project.package_collections.append(self.listPackageCollection.item(index).collection)

    def checkProject(self):
        """
            Checks required fields for the project.
        """
        if not len(self.lineTitle.text()):
            QMessageBox.warning(self, self.windowTitle(),  _("Image title is missing."))
            return False
        if not len(self.lineRepository.text()):
            QMessageBox.warning(self, self.windowTitle(), _("Repository URL is missing."))
            return False
        if not len(self.lineWorkFolder.text()):
            QMessageBox.warning(self, self.windowTitle(),  _("Work folder is missing."))
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
        self.updateCollection()

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

        self.listPackageCollection.clear()
        if self.project.package_collections:
            print "loadProject package_collections"
            print "project.media:%s" % self.project.media
            for collection in self.project.package_collections:
                PackageCollectionListItem(self.listPackageCollection, collection)

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
            QMessageBox.warning(self, self.title, _("Unable to load package index. URL is wrong, or file is corrupt."))
            return False
        except ExPackageCycle, e:
            self.progress.finished()
            cycle = " > ".join(e.args[0])
            QMessageBox.warning(self, self.title, _("Package index has errors. Cyclic dependency found:\n  %s.") % cycle)
            return False
        except ExPackageMissing, e:
            self.progress.finished()
            QMessageBox.warning(self, self.title, _("Package index has errors. '%s' depends on non-existing '%s'.") % e.args)
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
