# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
#
# Authors: İsmail Dönmez <ismail@pardus.org.tr>

# KDE/Qt imports
from kdecore import i18n
from kdeui import *
from qt import *

# Local imports
import PreferencesDialog
import RepoDialog

class Preferences(PreferencesDialog.PreferencesDialog):
    def __init__(self, parent=None):
        PreferencesDialog.PreferencesDialog.__init__(self, parent)
        self.parent = parent
        self.connect(self.addButton, SIGNAL("clicked()"), self.addNewRepo)
        self.connect(self.editButton, SIGNAL("clicked()"), self.editRepo)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeRepo)
        self.connect(self.repoListView, SIGNAL("selectionChanged()"), self.updateButtons)
        self.connect(self.updateRepoButton, SIGNAL("clicked()"), self.updateAllRepos)
        self.connect(self.moveUpButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.moveDownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.buttonOk, SIGNAL("clicked()"), self.saveSettings)
     
        self.editButton.setEnabled(False)
        self.removeButton.setEnabled(False)
        
        self.repoListView.setSorting(-1)
        self.updateListView()
        self.updateButtons()

        self.onlyShowPrograms.setChecked(self.parent.getShowOnlyPrograms())
        
    def updateButtons(self):
        if self.repoListView.childCount() > 1:
            moreThanOne = True
        else:
            moreThanOne = False
        
        if self.repoListView.currentItem().isSelected():
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
        self.repo.repoAddress.setText(self.oldRepoAddress)
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.updateRepoSettings)
        self.repo.show()
                        
    def removeRepo(self):
        repoItem = self.repoListView.currentItem()
        self.repoListView.takeItem(repoItem)
        self.parent.command.removeRepo(str(repoItem.text(0)))
        
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

        self.parent.command.swapRepos(self.repoList.index(item.text(0)),self.repoList.index(parent.text(0)))

    def moveDown(self):
        item = self.repoListView.currentItem()
        sibling = item.itemBelow()
        
        if not sibling:
            return
        
        item.moveItem(sibling)
        self.parent.command.swapRepos(str(self.repoList.index(item.text(0))),str(self.repoList.index(sibling.text(0))))
        
    def processNewRepo(self):
        repoName = unicode(self.repo.repoName.text())
        repoAddress = str(self.repo.repoAddress.text())

        if not (repoAddress.endswith("xml") or repoAddress.endswith("xml.bz2")):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml or xml.bz2 suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return
        else:
            self.parent.command.addRepo(repoName,repoAddress)
                    
        self.repo.close()

        confirm = KMessageBox.questionYesNo(self,i18n('<qt>Do you want to update repository <b>%1</b></qt>').arg(repoName),i18n("Pisi Question"))
        if confirm == KMessageBox.Yes:
            self.parent.command.updateRepo(repoName)

    def updateRepoSettings(self):
        # FIXME there should be a better way to do this
        newRepoName = str(self.repo.repoName.text())
        newRepoAddress = str(self.repo.repoAddress.text())

        if not newRepoAddress.endswith("xml"):
            KMessageBox.error(self,i18n('<qt>Repository address should end with xml suffix.<p>Please try again.</qt>'), i18n("Pisi Error"))
            return
        else:
            self.parent.command.removeRepo(self.oldRepoName)
            self.parent.command.addRepo(newRepoName,newRepoAddress)

        self.updateListView()
        self.repo.close()
   
    def updateListView(self):
        self.repoList = self.parent.command.getRepoList()
        self.repoListView.clear()
        
        index = len(self.repoList)-1
        while index >= 0:
            repoName = self.repoList[index]
            item = QListViewItem(self.repoListView,None)
            item.setText(0, self.repoList[index])
            item.setText(1, self.parent.command.getRepoUri(str(repoName)))
            index -= 1

        self.updateRepoButton.setEnabled(self.repoListView.childCount() > 0 )

    def saveSettings(self):
        self.parent.setShowOnlyPrograms(self.onlyShowPrograms.isChecked())
        self.parent.updateListing()
