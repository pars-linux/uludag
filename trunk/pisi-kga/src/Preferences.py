#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################################
# PiSi KGA - Repository Settings                                          #
# ------------------------------                                          #
# begin     : Çrş Eyl  7 19:02:05 EEST 2005                               #
# copyright : (C) 2005 by UEKAE/TÜBİTAK                                   #
# email     : ismail@uludag.org.tr                                        #
#                                                                         #
###########################################################################
#                                                                         #
#   This program is free software; you can redistribute it and/or modify  #
#   it under the terms of the GNU General Public License as published by  #
#   the Free Software Foundation; either version 2 of the License, or     #
#   (at your option) any later version.                                   #
#                                                                         #
###########################################################################

from qt import *
import PreferencesWidget
import RepoDialog
from kdecore import *
import PisiKga # for loadIcon

# Pisi imports
import pisi.api

class Preferences(PreferencesWidget.PrefsDialog):
    def __init__(self, parent=None):
        PreferencesWidget.PrefsDialog.__init__(self, parent)

        self.setCaption(i18n("PiSi KGA - Depo Ayarları"))
        self.infoLabel.setPixmap(PisiKga.loadIcon('info', KIcon.Desktop))
        self.networkLabel.setPixmap(PisiKga.loadIcon('network', KIcon.Desktop))
        self.connect(self.addButton, SIGNAL("clicked()"), self.addNewRepo)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeRepo)
        self.connect(self.repoListView, SIGNAL("selectionChanged()"), self.updateButtons)
        self.connect(self.moveupButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.movedownButton, SIGNAL("clicked()"), self.moveDown)
        self.removeButton.setEnabled(False)
        self.readConfig()
        self.repoListView.setSorting(-1)
        self.updateListView()

    def updateButtons(self):
        if self.repoListView.currentItem().isSelected():
            self.removeButton.setEnabled(True)
            self.moveupButton.setEnabled(True)
            self.movedownButton.setEnabled(True)
        else:
            self.removeButton.setEnabled(False)
            self.moveupButton.setEnabled(False)
            self.movedownButton.setEnabled(False)

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

        self.updateRepoList()
        
    def moveDown(self):
        item = self.repoListView.currentItem()
        sibling = item.itemBelow()

        if not sibling:
            return

        item.moveItem(sibling)
        self.updateRepoList()

    def updateRepoList(self):
        newList = []

        firstItem = self.repoListView.firstChild()

        while firstItem:
            newList.append(str(firstItem.text(0)))
            newList.append(str(firstItem.text(1)))
            firstItem = firstItem.itemBelow()

        self.repoList = newList
        self.writeConfig()
        
    def addNewRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption(i18n("PiSi KGA - Yeni Depo Ekle"))
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.processNewRepo)
        self.repo.show()

    def removeRepo(self):
        if self.repoListView.currentItem().isSelected():
            repoName = self.repoListView.currentItem().text(0)
            newList = QStringList()
            index = 0

            while index <= len(self.repoList)-1:
                if self.repoList[index] != repoName:
                    newList.append(self.repoList[index])
                    newList.append(self.repoList[index+1])
                index += 2
                
            self.repoList = newList
            self.writeConfig()
            self.updateListView()
            
    def processNewRepo(self):
        repoName = self.repo.repoNameLineEdit.text()
        repoAddress = self.repo.repoAddressLineEdit.text()

        self.repoList.append(repoName)
        self.repoList.append(repoAddress)
        self.writeConfig()
        self.updateListView()
        self.repo.close()

    def updateListView(self):
        self.repoListView.clear()
        
        index = 0
        while index <= len(self.repoList)-1:
            item = QListViewItem(self.repoListView,None)
            item.setText(0, self.repoList[index])
            item.setText(1, self.repoList[index+1])
            index += 2

    def readConfig(self):
        self.config = PisiKga.KGlobal.config()
        self.repoList = self.config.readListEntry('RepositoryList')

        if self.repoList.isEmpty():
            self.repoList.append('uludag')
            self.repoList.append('ftp://ftp.uludag.org.tr/pub/pisi/binary/system/base/pisi-index.xml')
            self.config.writeEntry('RepositoryList', self.repoList)
            self.config.sync()
            self.updatePisiConfig()

    def writeConfig(self):
        self.config.writeEntry('RepositoryList', self.repoList)
        self.config.sync()
        self.updatePisiConfig()

    def updatePisiConfig(self):
        index = 0
        length = len(self.repoList)-1

        if False:
            while index <= length:
                print 'Removing repo ',str(self.repoList[index])
                pisi.api.remove_repo(str(self.repoList[index]))
                index += 2
        
        index = 0
        while index <= length:
            print 'Adding repo ',str(self.repoList[index])
            try:
                pisi.api.add_repo(str(self.repoList[index]), str(self.repoList[index+1]))
            except pisi.repodb.Error:
                pass
            index += 2
