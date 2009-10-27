#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import sys
import thread

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *

# GUI Modules
from gui.help import HelpDialog
from gui.sidebar import SideBar
from gui.userpage import UserPage
from gui.optionspage import OptionsPage
from gui.filespage import FilesPage
from gui.progresspage import ProgressPage

# Utility Modules
from utility import partition, info, files
import applythread

class MigrationWizard(KWizard):
    "Modified KWizard for migration tool"
    def __init__(self, app):
        "Constructor of migration wizard"
        KWizard.__init__(self)
        self.kapp = app
        self.resize(700, 500)
        self.setCaption(i18n("Pardus Migration Tool"))
        # TODO : load icon
        # i18n:
        self.nextButton().setText(i18n("Next"))
        self.backButton().setText(i18n("Back"))
        self.finishButton().setText(i18n("Finish"))
        self.cancelButton().setText(i18n("Cancel"))
        self.helpButton().setText(i18n("Help"))
        # User page:
        self.userpage = UserPage(self)
        self.addPage(self.userpage, i18n("Selecting User"))
        self.addUsers()
        # Empty Options page:
        self.optionspage = QWidget(self)
        self.addPage(self.optionspage, i18n("Selecting Options"))
        # Empty Files page:
        self.filespage = QWidget(self)
        self.addPage(self.filespage, i18n("Selecting Files"))
        # Progress page:
        self.progresspage = QWidget(self)
        self.addPage(self.progresspage, i18n("Applying Changes"))
        # Connections:
        self.connect(self.helpButton(), SIGNAL("clicked()"), self.slotHelp)
        self.connect(self.kapp, SIGNAL("aboutToQuit()"), self.slotQuit)
    
    def slotHelp(self):
        self.helpwin = HelpDialog("migration", i18n("Migration Tool Help"), self)
        self.helpwin.show()
    
    def slotQuit(self):
        self.deleteLater()
    
    def modify(self, page, name):
        "Modifies widgets to add left panel before adding pages"
        container = QWidget(self)
        container.lay = QHBoxLayout(container, 10)
        container.left = SideBar(container, name)
        container.right = page
        page.reparent(container, 0, QPoint())
        container.lay.addWidget(container.left)
        container.lay.addWidget(container.right)
        container.left.setSizePolicy(QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum))
        return container
    
    def addPage(self, page, name):
        "Adds a modified page to wizard"
        newpage = self.modify(page, name)
        KWizard.addPage(self, newpage, name)
    
    def insertPage(self, page, name, position):
        "Inserts a modified page to wizard"
        newpage = self.modify(page, name)
        KWizard.insertPage(self, newpage, name, position)
    
    def removePage(self, page):
        "Removes a modified page from wizard"
        KWizard.removePage(self, page.parent())
    
    def setBackEnabled(self, page, value):
        "Sets functionality of back button"
        KWizard.setBackEnabled(self, page.parent(), value)
    
    def setNextEnabled(self, page, value):
        "Sets functionality of next button"
        KWizard.setNextEnabled(self, page.parent(), value)
    
    def setHelpEnabled(self, page, value):
        "Sets functionality of help button"
        KWizard.setHelpEnabled(self, page.parent(), value)
    
    def setFinishEnabled(self, page, value):
        "Sets functionality of finish button"
        KWizard.setFinishEnabled(self, page.parent(), value)
    
    def currentPage(self):
        "Returns the base part of the current page of wizard"
        container = KWizard.currentPage(self)
        if container:
            return container.right
    
    def indexOf(self, page):
        "Finds the index of given page"
        return KWizard.indexOf(self, page.parent())
    
    def layOutTitleRow(self, layout, title):
        "Finds the index of given page"
        arguments = {"title":title, "step":i18n("Step"), "index":self.indexOf(self.currentPage()) + 1}
        title = u"%(title)s (%(step)s %(index)d/4)" % arguments
        KWizard.layOutTitleRow(self, layout, title)
    
    def addUsers(self):
        "Searches old users and adds them to userpage's combo box"
        self.users = partition.allUsers()
        if len(self.users) == 0:
            message = i18n("Migration tool couldn't find any old users in your computer. You can't use this aplication.")
            QMessageBox.critical(self, i18n("No User"), message, QMessageBox.Ok, QMessageBox.NoButton)
            sys.exit()
        for user in self.users:
            part, parttype, username, userdir = user
            self.userpage.usersBox.insertItem("%s - %s (%s)" % (username, parttype, part))
    
    def next(self):
        "Runs when user clicks next button"
        if self.currentPage() == self.userpage:
            # Get user and collect information:
            user = self.users[self.userpage.usersBox.currentItem()]
            part, ostype, username, userdir = user
            self.sources = {"Partition":part, "OS Type":ostype, "User Name":username, "Home Path":userdir}
            self.sources = info.userInfo(self.sources)
            self.destinations = info.localInfo()
            # Update old settings page with the new one:
            self.removePage(self.optionspage)
            self.optionspage = OptionsPage(self.sources, self.destinations)
            self.insertPage(self.optionspage, i18n("Selecting Options"), 1)
            # Update old files page with the new one:
            self.removePage(self.filespage)
            self.filespage = FilesPage(self, self.sources)
            self.insertPage(self.filespage, i18n("Selecting Files"), 2)
            KWizard.next(self)
        elif self.currentPage() == self.optionspage:
            self.options = self.optionspage.getOptions()
            KWizard.next(self)
        elif self.currentPage() == self.filespage:
            # Update old progress page with the new one:
            self.removePage(self.progresspage)
            self.progresspage = ProgressPage(self)
            self.insertPage(self.progresspage, i18n("Applying Changes"), 3)
            # Apply:
            self.setBackEnabled(self.progresspage, False)
            thread.start_new_thread(applythread.run, (self,))
            KWizard.next(self)
