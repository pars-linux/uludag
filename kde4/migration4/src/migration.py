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

import sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import i18n, KAboutData, KConfig, KCmdLineArgs

from migration.gui.ui.main import Ui_MigrationUI
from migration.about import aboutData

#Screens
import migration.gui.ScrWelcome as welcome
import migration.gui.ScrUser as user
import migration.gui.ScrUserFiles as userfiles
import migration.gui.ScrOptions as options
import migration.gui.ScrSummary as summary
import migration.gui.ScrProgress as progress

import migration.gui.context as ctx


def loadFile(_file):
    try:
        f = file(_file)
        d = [a.strip() for a in f]
        d = (x for x in d if x and x[0] != "#")
        f.close()
        return d
    except:
        return []

def getKernelOpt(cmdopt=None):
    if cmdopt:
        for cmd in "".join(loadFile("/proc/cmdline")).split():
            if cmd.startswith("%s=" % cmdopt):
                return cmd[len(cmdopt)+1:].split(",")
    else:
        return "".join(loadFile("/proc/cmdline")).split()

    return ""


def isLiveCD():
    opts = getKernelOpt("mudur")

    if opts and "livecd" in opts:
        return True

    return False

if isLiveCD():
    availableScreens = [welcome, user, options, userfiles, summary, progress]
else:
    availableScreens = [welcome, user, options, userfiles, summary, progress]

class Migration(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MigrationUI()
        self.ui.setupUi(self)

        self.screens = availableScreens
        self.moveInc = 1
        self.menuText = ""
        self.config = KConfig("migrationrc")
        self.createWidget(self.screens)

        self.screenId = []

        for each in self.screens:
            title = each.Widget().title
            self.screenId.append(title)
            if self.screens.index(each) == 0:
                self.menuText += self.putBold(title)
            else:
                self.menuText += self.putBr(title)
        self.ui.labelMenu.setText(self.menuText)

        QtCore.QObject.connect(self.ui.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        QtCore.QObject.connect(self.ui.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        QtCore.QObject.connect(self.ui.buttonFinish, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        QtCore.QObject.connect(self.ui.buttonCancel, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))


    def slotNext(self):
        self.menuText = ""
        currentIndex = self.ui.mainStack.currentIndex() + 1

        for each in self.screenId:
            i = self.screenId.index(each)
            if currentIndex < len(self.screenId):
                if i == currentIndex:
                    self.menuText += self.putBold(self.screenId[i])
                else:
                    self.menuText += self.putBr(self.screenId[i])

        self.ui.labelMenu.setText(self.menuText)
        _widget = self.ui.mainStack.currentWidget()
        _return = _widget.execute()

        if _return[0]:
            self.stackMove(self.getCurrentStackId(self.moveInc))
            self.moveInc = 1
        elif not _return[0]:
            if not _return[1]:
                self.stackMove(self.getCurrentStackId(self.moveInc))
                self.moveInc = 1
            else:
                kdeui.KMessageBox.error(self, i18n(_return[1]))

    def slotBack(self):
        self.menuText = ""
        currentIndex = self.ui.mainStack.currentIndex()
        for each in self.screenId:
            i = self.screenId.index(each)
            if i<= len(self.screenId) and not i ==0:
                if i == currentIndex:
                    self.menuText += self.putBold(self.screenId[i-1])
                else:
                    self.menuText += self.putBr(self.screenId[i-1])

        self.menuText += self.putBr(self.screenId[i-1])
        self.ui.labelMenu.setText(self.menuText)
        _widget = self.ui.mainStack.currentWidget() 
        _widget.backCheck()
        self.moveInc = 1

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

    def putBr(self, item):
        return unicode("» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode("» ") + item + "</b><br>"

    def getCurrentStackId(self, d):
        new = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0 : new = 0
        if new > total: new = total
        return new

    def setCurrentStack(self,id=None):
        if id:
            self.stackMove(id)

    def createWidget(self, screens = []):
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _screen = screen.Widget()
            self.ui.mainStack.addWidget(_screen)

        self.stackMove(0)

    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id == 0:
            self.ui.mainStack.setCurrentIndex(id)
            _widget = self.ui.mainStack.currentWidget()
            _widget.update()
            print "_widget.shown() çağrılacak..."
            print "_widget.title:%s" % _widget.title
            _widget.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens) - 1 :
            self.ui.buttonNext.hide()
            self.ui.buttonFinish.show()
        else:
            self.ui.buttonNext.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
        else:
            self.ui.buttonBack.show()

    def __del__(self):
        group = self.config.group("General")
        group.writeEntry("RunOnStart", "False")

if __name__ =="__main__":

    KCmdLineArgs.init(sys.argv, aboutData)
    application = kdeui.KApplication()
    migration = Migration()
    migration.show()

    geometry  = QtGui.QDesktopWidget().screenGeometry()
    migration.move(geometry.width()/2 - migration.width()/2, geometry.height()/2 - migration.height()/2) 
    application.exec_()


