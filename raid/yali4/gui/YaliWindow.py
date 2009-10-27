# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from os.path import join
from PyQt4 import QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.sysutils
from yali4.gui.Ui.main import Ui_YaliMain
import yali4.gui.context as ctx

# Aspect oriented huh ;)
from pyaspects.weaver import *
from yali4.gui.aspects import *

# Release Notes
import GUIRelNotes

##
# Widget for YaliWindow (you can call it MainWindow too ;).
class Widget(Ui_YaliMain):
    def __init__(self):
        self.ui = QtGui.QWidget()
        self.setupUi(self.ui)
        self.screenData = None
        # shortcut to open debug window
        self.debugShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F2),self.ui)
        self.ui.setAttribute(Qt.WA_OpaquePaintEvent)
        # move one step at a time
        self.moveInc = 1

        # Dont need help as default
        self.slotToggleHelp()

        # Main Slots
        QObject.connect(self.debugShortCut, SIGNAL("activated()"), self.toggleDebug)
        QObject.connect(self.buttonNext, SIGNAL("clicked()"), self.slotNext)
        QObject.connect(self.buttonBack, SIGNAL("clicked()"), self.slotBack)
        QObject.connect(self.toggleHelp, SIGNAL("clicked()"), self.slotToggleHelp)
        QObject.connect(self.releaseNotes, SIGNAL("clicked()"), self.showReleaseNotes)

    # show/hide help text
    def slotToggleHelp(self):
        if self.helpContent.isVisible():
            self.helpContent.hide()
        else:
            self.helpContent.show()

    # show/hide debug window
    def toggleDebug(self):
        if ctx.debugger.isVisible():
            ctx.debugger.hideWindow()
        else:
            ctx.debugger.showWindow()

    # returns the id of current stack
    def getCur(self, d):
        new   = self.mainStack.currentIndex() + d
        total = self.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    # move to id numbered step
    def setCurrent(self, id=None):
        if id:
            self.stackMove(id)

    # execute next step
    def slotNext(self, dryRun=False):
        if not dryRun:
            _w = self.mainStack.currentWidget()
            _w.execute()
        self.stackMove(self.getCur(self.moveInc))
        self.moveInc = 1

    # execute previous step
    def slotBack(self):
        _w = self.mainStack.currentWidget()
        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    # move to id numbered stack
    def stackMove(self, id):
        self.mainStack.setCurrentIndex(id)
        _w = self.mainStack.currentWidget()
        self.screenName.setText(_w.title)
        self.screenDescription.setText(_w.desc)
        self.screenIcon.setPixmap(QtGui.QPixmap(":/gui/pics/%s.png" % (_w.icon or "pardus")))
        self.helpContent.setText(_w.help)
        # shown functions contain necessary instructions before
        # showing a stack ( updating gui, disabling some buttons etc. )
        _w.shown()

    # create all widgets and add inside stack
    # see runner.py/_all_screens for the list
    def createWidgets(self, screens=[]):
        if not self.screenData:
            self.screenData = screens
        self.mainStack.removeWidget(self.page)
        for screen in screens:
            _scr = screen.Widget()

            if ctx.options.debug == True or yali4.sysutils.checkYaliParams(param="debug"):
                # debug all screens.
                weave_all_object_methods(ctx.debugger.aspect, _scr)

            # enable navigation buttons before shown
            weave_object_method(enableNavButtonsAspect, _scr, "shown")
            # disable navigation buttons before the execute.
            weave_object_method(disableNavButtonsAspect, _scr, "execute")

            self.mainStack.addWidget(_scr)

        weave_all_object_methods(ctx.debugger.aspect, self)
        self.stackMove(0)

    # Enable/Disable buttons
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

    # processEvents
    def processEvents(self):
        QObject.emit(self.ui,SIGNAL("signalProcessEvents"))

    def showReleaseNotes(self):
        # make a release notes dialog
        r = GUIRelNotes.Widget(self.ui)
        d = Dialog(_('Release Notes'), r, self)
        d.resize(500,400)
        d.exec_()

