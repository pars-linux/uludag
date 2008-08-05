#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os

from PyQt4 import QtGui, QtCore, uic
import gettext

_ = gettext.gettext

from screens import ScrRepo
from screens import ScrMedia
from screens import ScrSystemType
from screens import ScrUsers
from screens import ScrGrub

screenId = {"":""}

class Pardusman(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi("screens/mainWindowUi.ui", self)

        self.getWidgets()
        self.initialize()
        self.setMainWindow()

    def getWidgets(self):
        self.avail_screens = [ScrRepo.Widget(),
                              ScrMedia.Widget(),
                              ScrSystemType.Widget(),
                              ScrUsers.Widget(),
                              ScrGrub.Widget()]

    def initialize(self):
        leftPanel = ""
        for screen in self.avail_screens:
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
        for widget in self.avail_screens:
            self.pageStack.addWidget(widget)

    def getCurrent(self):
        return self.pageStack.indexOf(self.pageStack.currentWidget())

    def stackMove(self,where):
        if where<=2:
            where = 2
        if where>len(self.avail_screens):
            where = len(self.avail_screens)+1

        self.pageStack.setCurrentIndex(where)
        _w = self.pageStack.currentWidget()
        self.pageDesc.setText(_(_w.desc))
        #self.pageIcon.setPixmap(QPixmap(locate("data", _w.icon)))

        _w.show()

        # hide next and show finish buttons on last screen
        if self.getCurrent() == len(screenId):
            self.buttonNext.hide()
            self.buttonFinish.show()
        else:
            self.buttonNext.show()
            self.buttonFinish.hide()

        # hide back button on first screen
        if self.getCurrent()-1 == 1:
            self.buttonBack.hide()
        else:
            self.buttonBack.show()

    def slotNext(self):
        #_w = self.pageStack.currentWidget()
        #_w.show()

        if not self.avail_screens[2].radioLive.isChecked() and self.getCurrent() == 4:
            next = self.getCurrent() + 2
        else:
            next = self.getCurrent() + 1

        stepBatch = ""

        for sId in screenId:
            if  sId <= len(screenId):
                if sId == next:
                    stepBatch+= self.putBold(screenId[sId])
                else:
                    stepBatch+= self.putBr(screenId[sId])

        self.pixSteps.setText(stepBatch)
        self.stackMove(next)

    def putBr(self, item):
        return unicode("» ") + item + "<br>"

    def putBold(self, item):
        return "<b>" + unicode("» ") + item + "</b><br>"

    def slotBack(self):
        if not self.avail_screens[2].radioLive.isChecked() and self.getCurrent() == 6:
            prev = self.getCurrent() - 2
        else:
            prev = self.getCurrent() - 1
 
        stepBatch = ""
        for sId in screenId:
            if  sId < len(screenId) and not sId == 1:
                if sId == prev:
                    stepBatch+= self.putBold(screenId[sId])
                else:
                    stepBatch+= self.putBr(screenId[sId])
        stepBatch+= self.putBr(screenId[len(screenId)])
        self.pixSteps.setText(stepBatch)

        self.stackMove(prev)

    def setMainWindow(self):
        self.pageDesc.setText(_("Welcome to Pardus CD/DVD/USB Distribution Wizard"))
        
        icon = QtGui.QPixmap(QtCore.QString("data/pardusman.png"))
        self.pageIcon.setPixmap(icon)
        
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
    pm = Pardusman()
    pm.show()
    sys.exit(app.exec_())

