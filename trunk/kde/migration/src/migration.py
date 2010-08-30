#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import os, sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import i18n, KAboutData, KConfig, KCmdLineArgs

from migration.gui.ui.main import Ui_migration
from migration.about import aboutData

import migration.gui.context as ctx

from migration.utils import tools
from migration.utils.progress_pie import DrawPie
from migration.utils.migration_menu import Menu


class Migration(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.initializeGlobals()
        self.initializeUI()
        self.signalHandler()

    def initializeGlobals(self):
        ''' initializes global variables '''
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.titles = []
        self.descriptions = []
        self.currentDir = os.path.dirname(os.path.realpath(__file__))
        self.screensPath = self.currentDir + "/migration/gui/Scr*py"
        self.migrationConfig = KConfig("migrationrc")

    def signalHandler(self):
        ''' connects signals to slots '''
        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        QtCore.QObject.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        QtCore.QObject.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))

    def initializeUI(self):
        ''' initializes the human interface '''
        self.ui = Ui_migration()
        self.ui.setupUi(self)

        self.ui.buttonApply.hide()
        self.ui.buttonFinish.hide()

        # load screens
        tools.loadScreens(self.screensPath, globals())
        self.screens = [ScrWelcome, ScrUser, ScrOptions, ScrUserFiles, ScrSummary, ScrProgress]

        # Add screens to StackWidget
        self.createWidgets(self.screens)

        # Get Screen Titles
        for screen in self.screens:
            title = str(screen.Widget.title)
            self.titles.append(title)

        # draw progress pie
        self.countScreens = len(self.screens)
        self.pie = DrawPie(self.countScreens, self.ui.labelProgress)

        # Initialize Menu
        self.menu = Menu(self.titles, self.ui.labelMenu)
        self.menu.start()


    def createWidgets(self, screens=[]):
        ''' create all widgets and add inside stack '''
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()

            # Append screen descriptions to list
            self.descriptions.append(str(_scr.desc))

            # Append screens to stack widget
            self.ui.mainStack.addWidget(_scr)


    def getCur(self, d):
        ''' returns the id of current stack '''
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    def setCurrent(self, id=None):
        ''' move to id numbered step '''
        if id: self.stackMove(id)

    def slotNext(self,dryRun=False):
        ''' execute next step '''
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() + 1

        # update pie progress
        self.pie.updatePie(curIndex)

        # animate menu
        self.menu.next()

        _w = self.ui.mainStack.currentWidget()

        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    def slotBack(self):
        ''' execute previous step '''
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()

        # update pie progress
        self.pie.updatePie(curIndex-1)

        # animate menu
        self.menu.prev()

        _w = self.ui.mainStack.currentWidget()

        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    def stackMove(self, id):
        ''' move to id numbered stack '''
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)

            # Set screen title
            self.ui.screenTitle.setText(self.descriptions[id])

            _w = self.ui.mainStack.currentWidget()
            _w.update()
            _w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 3:
            self.ui.buttonNext.show()
            self.ui.buttonApply.hide()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 2:
            self.ui.buttonNext.hide()
            self.ui.buttonApply.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 1:
            self.ui.buttonApply.hide()
            self.ui.buttonFinish.show()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
            self.ui.buttonFinish.hide()
            self.ui.buttonApply.hide()
        else:
            self.ui.buttonBack.show()

    def enableNext(self):
        self.ui.buttonNext.setEnabled(True)

    def disableNext(self):
        self.ui.buttonNext.setEnabled(False)

    def enableBack(self):
        self.ui.buttonBack.setEnabled(True)

    def disableBack(self):
        self.ui.buttonBack.setEnabled(False)

    def isNextEnabled(self):
        return self.ui.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.ui.buttonBack.isEnabled()

    def __del__(self):
        group = self.config.group("General")
        group.writeEntry("RunOnStart", "False")

if __name__ =="__main__":

    KCmdLineArgs.init(sys.argv, aboutData)
    application = kdeui.KApplication()
    migration = Migration()
    migration.show()
    tools.centerWindow(migration)
    application.exec_()
