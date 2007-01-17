# -*- coding: utf-8 -*-
#
# Copyright (C) 2005,2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# KDE/Qt imports
from kdecore import i18n
from kdeui import *
from qt import *

# Local imports
import HelpDialog
import PreferencesDialog
import RepoDialog
import Settings

class Preferences(PreferencesDialog.PreferencesDialog):
    def __init__(self, parent=None):
        PreferencesDialog.PreferencesDialog.__init__(self, parent)
        self.parent = parent
        self.connect(self.addButton, SIGNAL("clicked()"), self.addNewRepo)
        self.connect(self.editButton, SIGNAL("clicked()"), self.editRepo)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeRepo)
        self.connect(self.repoListView, SIGNAL("selectionChanged()"), self.updateButtons)
        self.connect(self.moveUpButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.moveDownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)
        self.connect(self.intervalCheck, SIGNAL("toggled(bool)"), self.enableCheckInterval)
        self.connect(self.useCacheCheck, SIGNAL("toggled(bool)"), self.enableUseCache)
        self.connect(self.clearCacheButton, SIGNAL("clicked()"), self.clearAllCached)
        self.connect(self.buttonHelp, SIGNAL("clicked()"), self.showHelp)

        self.editButton.setEnabled(False)
        self.removeButton.setEnabled(False)

        self.repoListView.setSorting(-1)
        self.updateListView()
        self.updateButtons()

        self.onlyGuiApp.setChecked(self.parent.settings.getBoolValue(Settings.general, "ShowOnlyGuiApp"))
        self.intervalCheck.setChecked(self.parent.settings.getBoolValue(Settings.general, "UpdateCheck"))
        self.intervalSpin.setValue(self.parent.settings.getNumValue(Settings.general, "UpdateCheckInterval"))
        self.systemTray.setChecked(self.parent.settings.getBoolValue(Settings.general, "SystemTray"))
        self.useCacheCheck.setChecked(self.parent.settings.getBoolValue(Settings.general, "PackageCache"))
        self.useCacheSize.setValue(self.parent.settings.getNumValue(Settings.general, "CacheLimit"))
        self.reposChanged = False

    def updateButtons(self):
        if self.repoListView.childCount() > 1:
            moreThanOne = True
        else:
            moreThanOne = False

        if self.repoListView.currentItem() and self.repoListView.currentItem().isSelected():
            self.editButton.setEnabled(True)
            self.removeButton.setEnabled(moreThanOne)
            self.moveUpButton.setEnabled(moreThanOne)
            self.moveDownButton.setEnabled(moreThanOne)

        else:
            self.editButton.setEnabled(False)
            self.removeButton.setEnabled(False)
            self.moveUpButton.setEnabled(False)
            self.moveDownButton.setEnabled(False)

    def updateAllRepos(self):
        self.parent.command.updateAllRepos()

    def addNewRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption(i18n("Add New Repository"))
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.processNewRepo)
        self.repo.show()

    def editRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption(i18n("Edit Repository"))
        self.oldRepoName = self.repoListView.currentItem().text(0)
        self.oldRepoAddress = self.repoListView.currentItem().text(1)
        self.repo.repoName.setText(self.oldRepoName)
        self.repo.repoAddress.insertItem(self.oldRepoAddress, 0)
        self.repo.repoAddress.setCurrentItem(0)
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.updateRepoSettings)
        self.repo.show()

    def removeRepo(self):
        repoItem = self.repoListView.currentItem()
        self.repoListView.takeItem(repoItem)
        self.reposChanged = True

    def moveUp(self):
        item = self.repoListView.currentItem()
        parent = item.itemAbove()

        if not parent:
            return

        if parent.itemAbove():
            item.moveItem(parent.itemAbove())
        else:
            self.repoListView.takeItem(item)
            self.repoListView.insertItem(item)
            self.repoListView.setSelected(item, True)

        self.reposChanged = True

    def moveDown(self):
        item = self.repoListView.currentItem()
        sibling = item.itemBelow()

        if not sibling:
            return

        item.moveItem(sibling)
        self.reposChanged = True

    def processNewRepo(self):
        repoName = unicode(self.repo.repoName.text())
        repoAddress = str(self.repo.repoAddress.currentText())

        if not repoAddress.endswith("xml") and not repoAddress.endswith("xml.bz2"):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml or xml.bz2 suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return

        item = QListViewItem(self.repoListView, self.repoListView.currentItem())
        item.setText(0, unicode(repoName))
        item.setText(1, repoAddress)
        self.repoListView.insertItem(item)

        self.reposChanged = True
        self.repo.close()

    def updateRepoSettings(self):
        newRepoName = unicode(self.repo.repoName.text())
        newRepoAddress = str(self.repo.repoAddress.currentText())

        if not newRepoAddress.endswith("xml") and not newRepoAddress.endswith("xml.bz2"):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml or xml.bz2 suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return

        self.repoListView.currentItem().setText(0,newRepoName)
        self.repoListView.currentItem().setText(1,newRepoAddress)

        self.reposChanged = True
        self.repo.close()

    def saveSettings(self):
        self.parent.settings.setValue(Settings.general, "ShowOnlyGuiApp", self.onlyGuiApp.isChecked())
        self.parent.settings.setValue(Settings.general, "SystemTray", self.systemTray.isChecked())
        self.parent.settings.setValue(Settings.general, "UpdateCheck", self.intervalCheck.isChecked())
        self.parent.settings.setValue(Settings.general, "UpdateCheckInterval", self.intervalSpin.value())
        self.parent.settings.setValue(Settings.general, "PackageCache", self.useCacheCheck.isChecked())
        self.parent.settings.setValue(Settings.general, "CacheLimit", self.useCacheSize.value())

        if self.intervalCheck.isChecked():
            self.parent.parent.tray.updateInterval(self.intervalSpin.value())
        else:
            self.parent.parent.tray.updateInterval(0)

        if self.reposChanged:
            repoList = []
            item = self.repoListView.firstChild()
            while item:
                repoList.append(unicode(item.text(0)))
                repoList.append(str(item.text(1)))
                item = item.nextSibling()

            self.reposChanged = False
            self.parent.command.setRepositories(repoList)
            self.parent.progressDialog.setCurrentOperation(i18n("<b>Applying Repository Changes</b>"))
            self.parent.progressDialog.show()

        self.parent.refreshState()

    def updateListView(self):
        self.repoList = self.parent.command.getRepoList()
        self.repoListView.clear()

        index = len(self.repoList)-1
        while index >= 0:
            repoName = self.repoList[index]
            item = QListViewItem(self.repoListView,None)
            item.setText(0, unicode(self.repoList[index]))
            item.setText(1, self.parent.command.getRepoUri(str(repoName)))
            index -= 1

    def enableCheckInterval(self, state):
        self.intervalLabel.setEnabled(state)
        self.intervalSpin.setEnabled(state)

    def enableUseCache(self, state):
        self.useCacheLabel.setEnabled(state)
        self.useCacheSize.setEnabled(state)
        self.useCacheInfo.setEnabled(state)

    def showHelp(self):
        helpwin = HelpDialog.HelpDialog(self, HelpDialog.PREFERENCES)
        helpwin.show()

    def clearAllCached(self):
        if KMessageBox.Yes == KMessageBox.warningYesNo(self, 
                                                       i18n("All the cached packages will be deleted. Are you sure? "),
                                                       i18n("Warning"),
                                                       KGuiItem(i18n("Delete"), "trashcan_empty"),
                                                       KStdGuiItem.cancel()
                                                       ):
            self.parent.command.clearCache(0)
