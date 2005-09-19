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
import PisiKga # for loadIcon

# Pisi imports
import pisi.api

class Preferences(PreferencesWidget.PrefsDialog):
    def __init__(self, parent=None):
        PreferencesWidget.PrefsDialog.__init__(self, parent)

        self.setCaption('PiSi KGA - Depo Ayarları')
        self.infoLabel.setPixmap(PisiKga.loadIcon('info'))
        self.networkLabel.setPixmap(PisiKga.loadIcon('network'))
        self.connect(self.addButton, SIGNAL("clicked()"), self.addNewRepo)
        self.connect(self.removeButton, SIGNAL("clicked()"), self.removeRepo)
        self.connect(self.repoListView, SIGNAL("selectionChanged()"), self.updateButtons)
        self.connect(self.moveupButton, SIGNAL("clicked()"), self.moveUp)
        self.connect(self.movedownButton, SIGNAL("clicked()"), self.moveDown)
        self.connect(self.updateRepoButton, SIGNAL("clicked()"), self.updateAllRepos)
        self.removeButton.setEnabled(False)
        self.repoListView.setSorting(-1)
        self.readConfig()
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

        # TODO move in pisi config too

    def moveDown(self):
        item = self.repoListView.currentItem()
        sibling = item.itemBelow()

        if not sibling:
            return

        item.moveItem(sibling)

        # TODO move in pisi config too

    def updateAllRepos(self):
        # TODO progress
        self.updateRepoButton.setEnabled(False)
        
        for i in self.repoList:
            print 'Updating',i
            pisi.api.update_repo(i)

        self.updateRepoButton.setEnabled(True)
    
    def addNewRepo(self):
        self.repo = RepoDialog.RepoDialog(self)
        self.repo.setCaption('PiSi KGA - Yeni Depo Ekle')
        self.repo.setModal(True)
        self.connect(self.repo.okButton, SIGNAL("clicked()"), self.processNewRepo)
        self.repo.show()

    def removeRepo(self):
        repoItem = self.repoListView.currentItem()
        self.repoListView.takeItem(repoItem)
        pisi.api.remove_repo(repoItem.text(0))
                    
    def processNewRepo(self):
        repoName = self.repo.repoNameLineEdit.text()
        repoAddress = self.repo.repoAddressLineEdit.text()
        pisi.api.add_repo(str(repoName),str(repoAddress))
        item = QListViewItem(self.repoListView,None)
        item.moveItem(self.repoListView.lastChild())
        item.setText(0, str(repoName))
        self.repo.close()
    
    def updateListView(self):
        self.repoListView.clear()
        
        index = len(self.repoList)-1
        while index >= 0:
            item = QListViewItem(self.repoListView,None)
            item.setText(0, self.repoList[index])
            index -= 1

    def readConfig(self):
        self.repoList = pisi.api.ctx.repodb.list()
        if not len(self.repoList):
            pisi.api.add_repo('uludag', 'ftp://ftp.uludag.org.tr/pub/pisi/binary/system/base/pisi-index.xml')
            # TODO Make async
            pisi.api.update_repo('uludag')
