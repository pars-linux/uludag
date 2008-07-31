#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt4 import QtGui, QtCore, uic
import gettext

_ = gettext.gettext

screenId = {"":""}

class Wizard(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("screens/mainWindowUi.ui", self)

        self.getWidgets()
        self.initialize()
        self.setMainWindow()

    def getWidgets(self):
        self.avail_screens = {}

        for file in os.listdir("screens"):
            if file.startswith("screen"):
                self.avail_screens[file] = uic.loadUi("screens/%s" % file)

    def initialize(self):
        leftPanel = ""
        for screen in self.avail_screens.itervalues():
            _w = screen
            self.pageStack.addWidget(_w)
            sId = self.pageStack.indexOf(_w)
            sCaption = _w.windowTitle()
            screenId[sId] = sCaption

            if sId == 2:
                leftPanel += self.putBold(sCaption)
            else:
                leftPanel += self.putBr(sCaption)

        self.pixSteps.setText(leftPanel)
        self.pageStack.setCurrentIndex(2)

    def setWidgets(self):
        for widget in self.avail_screens.itervalues():
            self.pageStack.addWidget(widget)

    def getCurrent(self):
        return self.pageStack.indexOf(self.pageStack.currentWidget())

    def stackMove(self,where):
        if where<=0:
            where = 1
        if where>=len(self.avail_screens):
            where = len(self.avail_screens)

        self.pageStack.setCurrentIndex(where)
        _w = self.pageStack.currentWidget()
        self.pageDesc.setText(_(_w.desc))
        #self.pageIcon.setPixmap(QPixmap(locate("data", _w.icon)))

        _w.shown()

        if self.getCurrent() == 1:
            self.buttonBack

        # hide next and show finish buttons on last screen
        if self.getCurrent() == len(screenId):
            self.buttonNext.hide()
            self.buttonFinish.show()
        else:
            self.buttonNext.show()
            self.buttonFinish.hide()

        # hide back button on first screen
        if self.getCurrent() == 1:
            self.buttonBack.hide()
        else:
            self.buttonBack.show()

    def slotNext(self):
        _w = self.pageStack.currentWidget()
        _w.show()
        stepBatch = ""
        stepBatch += self.putBr(screenId[2])

        for sId in screenId:
            if  sId < len(screenId):
                if sId == self.getCurrent():
                    stepBatch+= self.putBold(screenId[sId+1])
                else:
                    stepBatch+= self.putBr(screenId[sId +1])

        self.pixSteps.setText(stepBatch)
        self.stackMove(self.getCurrent() + 1)

    def putBr(self, item):
        return unicode("» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode("» ") + item + "</b><br>"

    def slotBack(self):
        stepBatch = ""
        for sId in screenId:
            if  sId <= len(screenId) and not sId == 1:
                if sId == self.getCurrent():
                    stepBatch+= self.putBold(screenId[sId - 1])
                else:
                    stepBatch+= self.putBr(screenId[sId - 1])
        stepBatch+= self.putBr(screenId[len(screenId)])
        self.pixSteps.setText(stepBatch)

        self.stackMove(self.getCurrent() - 1)

    def setMainWindow(self):
        self.pageDesc.setText(_("Welcome to Pardus CD/DVD/USB Distribution Wizard"))
        self.buttonCancel.setText(_("&Cancel"))
        self.buttonBack.setText(_("&Back"))
        self.buttonNext.setText(_("&Next"))
        self.buttonFinish.setText(_("Finish"))

        self.buttonFinish.hide()
        self.buttonBack.hide()

        self.connect(self.buttonNext, QtCore.SIGNAL("clicked()"), self.slotNext)
        self.connect(self.buttonBack, QtCore.SIGNAL("clicked()"), self.slotBack)
        self.connect(self.buttonCancel, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("quit()"))
        self.connect(self.buttonFinish, QtCore.SIGNAL("clicked()"), self, QtCore.SLOT("quit()"))

        self.setWidgets()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    pmw = Wizard()
    pmw.show()
    sys.exit(app.exec_())

