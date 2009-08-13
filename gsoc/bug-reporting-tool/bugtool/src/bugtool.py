#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui
from PyKDE4 import kdeui
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs

import gui, subprocess, os, dbus

from gui.bugtoolMain import Ui_bugtoolUI
import gui.welcomeScreen as welcomeWidget
import gui.credentialsScreen as credentialsWidget
import gui.progressScreen as progressWidget
import gui.attachScreen as attachmentsWidget
import gui.goodbyeScreen as goodbyeWidget

availableScreens = [welcomeWidget, credentialsWidget, progressWidget,
                    attachmentsWidget, goodbyeWidget]

class BugTool(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_bugtoolUI()

        self.ui.setupUi(self)
        self.screens = availableScreens
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        self.createWidgets(self.screens)

        self.screenId = []
        for each in self.screens:
            title = each.Widget().windowTitle()
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

    # returns the id of current stack
    def getCur(self, d):
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    # move to id numbered step
    def setCurrent(self, id=None):
        if id:
            self.stackMove(id)

    # execute next step
    def slotNext(self,dryRun=False):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() +1

        for each in self.screenId:
            i = self.screenId.index(each)
            if  curIndex < len(self.screenId):
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i])
                else:
                    self.menuText += self.putBr(self.screenId[i])

        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    # execute previous step
    def slotBack(self):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()
        for each in self.screenId:
            i = self.screenId.index(each)
            if i <= len(self.screenId) and not i == 0:
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i -1])
                else:
                    self.menuText += self.putBr(self.screenId[i -1])

        self.menuText += self.putBr(self.screenId[-1])
        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    def putBr(self, item):
        return unicode(u"» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode(u"» ") + item + "</b><br>"

    # move to id numbered stack
    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)
            _w = self.ui.mainStack.currentWidget()
            _w.update()
            _w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens)-1:
            self.ui.buttonNext.hide()
            self.ui.buttonFinish.show()
        else:
            self.ui.buttonNext.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
        else:
            self.ui.buttonBack.show()

    # create all widgets and add inside stack
    def createWidgets(self, screens=[]):
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()
            self.ui.mainStack.addWidget(_scr)

        self.stackMove(0)

    def disableNext(self):
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

if __name__ == "__main__":
    # About data
    appName     = "bugtool"
    catalog     = ""
    programName = ki18n("bugtool")
    version     = "4.0"
    description = ki18n("Bug Reporting Tool for Pardus")
    license     = KAboutData.License_GPL
    copyright   = ki18n("(c) 2009 Pardus")
    text        = ki18n("none")
    homePage    = "www.pardus.org.tr"
    bugEmail    = "pinar@pardus.org.tr"

    aboutData   = KAboutData(appName,catalog, programName, version, description,
                                license, copyright,text, homePage, bugEmail)

    KCmdLineArgs.init(sys.argv, aboutData)
    app =  kdeui.KApplication()

    if not dbus.get_default_main_loop():
        from dbus.mainloop.qt import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    bugtool = BugTool()
    bugtool.show()
    rect  = QtGui.QDesktopWidget().screenGeometry()
    bugtool.move(rect.width()/2 - bugtool.width()/2, rect.height()/2 - bugtool.height()/2)
    app.exec_()

