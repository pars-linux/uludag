# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2008, TUBITAK/UEKAE
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
from yali4.gui.YaliDialog import Dialog
import yali4.gui.context as ctx

# Aspect oriented huh ;)
from pyaspects.weaver import *
from yali4.gui.aspects import *

# Release Notes
import GUIRelNotes

# QTerm
import QTermWidget

##
# Widget for YaliWindow (you can call it MainWindow too ;).
class Widget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self, None)

        self.ui = Ui_YaliMain()
        self.ui.setupUi(self)

        self.screenData = None
        # shortcut to open debug window
        self.debugShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F2),self)

        # shortcut to open a console
        self.consoleShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F11),self)

        # something funny
        self.cursorShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F7),self)
        self.themeShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F8),self)

        # set style
        self._style = ctx.consts.stylesheet
        self.updateStyle()

        # move one step at a time
        self.moveInc = 1

        # Dont need help as default
        self.ui.helpContent.hide()
        self.ui.toggleHelp.setText(_("Show Help"))

        # Main Slots
        self.connect(self.debugShortCut,    SIGNAL("activated()"),  self.toggleDebug)
        self.connect(self.consoleShortCut,  SIGNAL("activated()"),  self.toggleConsole)
        self.connect(self.cursorShortCut,   SIGNAL("activated()"),  self.toggleCursor)
        self.connect(self.themeShortCut,    SIGNAL("activated()"),  self.toggleTheme)
        self.connect(self.ui.buttonNext,    SIGNAL("clicked()"),    self.slotNext)
        self.connect(self.ui.buttonBack,    SIGNAL("clicked()"),    self.slotBack)
        self.connect(self.ui.toggleHelp,    SIGNAL("clicked()"),    self.slotToggleHelp)
        self.connect(self.ui.releaseNotes,  SIGNAL("clicked()"),    self.showReleaseNotes)

        self.terminal = None

    def updateStyle(self):
        self.setStyleSheet(file(self._style).read())

    def toggleTheme(self):
        if self._style == ctx.consts.stylesheet:
            self._style = ctx.consts.alternatestylesheet
        else:
            self._style = ctx.consts.stylesheet
        self.updateStyle()

    def toggleConsole(self):
        if not self.terminal:
            _terminal = QTermWidget.QTermWidget()
            self.terminal = Dialog(_('Terminal'), _terminal, self, True, QtGui.QKeySequence(Qt.Key_F11))
            self.terminal.resize(700,500)
        self.terminal.exec_()

    def toggleCursor(self):
        if self.cursor().shape() == QtGui.QCursor(Qt.ArrowCursor).shape():
            raw = QtGui.QPixmap(":/gui/pics/pardusman-icon.png")
            raw.setMask(raw.mask())
            self.setCursor(QtGui.QCursor(raw,2,2))
        else:
            self.unsetCursor()

    # show/hide help text
    def slotToggleHelp(self):
        if self.ui.helpContent.isVisible():
            self.ui.helpContent.hide()
            self.ui.toggleHelp.setText(_("Show Help"))
        else:
            self.ui.helpContent.show()
            self.ui.toggleHelp.setText(_("Hide Help"))
        _w = self.ui.mainStack.currentWidget()
        _w.update()

    # show/hide debug window
    def toggleDebug(self):
        if ctx.debugger.isVisible():
            ctx.debugger.hideWindow()
        else:
            ctx.debugger.showWindow()

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
        _w = self.ui.mainStack.currentWidget()
        ret = True
        if not dryRun:
            ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1

    # execute previous step
    def slotBack(self):
        _w = self.ui.mainStack.currentWidget()
        if _w.backCheck():
            self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    # move to id numbered stack
    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)
            _w = self.ui.mainStack.currentWidget()
            self.ui.screenName.setText(_w.title)
            self.ui.screenDescription.setText(_w.desc)
            self.ui.screenIcon.setPixmap(QtGui.QPixmap(":/gui/pics/%s.png" % (_w.icon or "pardus")))
            self.ui.helpContent.setText(_w.help)
            # shown functions contain necessary instructions before
            # showing a stack ( updating gui, disabling some buttons etc. )
            ctx.mainScreen.processEvents()
            _w.update()
            ctx.mainScreen.processEvents()
            _w.shown()

    # create all widgets and add inside stack
    # see runner.py/_all_screens for the list
    def createWidgets(self, screens=[]):
        if not self.screenData:
            self.screenData = screens
        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()

            if ctx.options.debug == True or yali4.sysutils.checkYaliParams(param="debug"):
                # debug all screens.
                weave_all_object_methods(ctx.debugger.aspect, _scr)

            # enable navigation buttons before shown
            weave_object_method(enableNavButtonsAspect, _scr, "shown")
            # disable navigation buttons before the execute.
            weave_object_method(disableNavButtonsAspect, _scr, "execute")

            self.ui.mainStack.addWidget(_scr)

        weave_all_object_methods(ctx.debugger.aspect, self)
        self.stackMove(0)

    # Enable/Disable buttons
    def disableNext(self):
        self.ui.buttonNext.setEnabled(False)

    def disableBack(self):
        self.ui.buttonBack.setEnabled(False)

    def enableNext(self):
        self.ui.buttonNext.setEnabled(True)

    def enableBack(self):
        self.ui.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.ui.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.ui.buttonBack.isEnabled()

    # processEvents
    def processEvents(self):
        QObject.emit(self, SIGNAL("signalProcessEvents"))

    def showReleaseNotes(self):
        # make a release notes dialog
        r = GUIRelNotes.Widget(self)
        d = Dialog(_('Release Notes'), r, self)
        d.resize(500,400)
        d.exec_()

