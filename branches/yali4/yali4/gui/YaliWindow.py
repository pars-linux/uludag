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

##
# Widget for YaliWindow (you can call it MainWindow too ;).
class Widget(Ui_YaliMain):
    def __init__(self):
        self.ui = QtGui.QWidget()
        self.setupUi(self.ui)
        self.screenData = None
        self.debugShortCut = QtGui.QShortcut(QtGui.QKeySequence(Qt.Key_F2),self.ui)

        QObject.connect(self.debugShortCut, SIGNAL("activated()"), self.toggleDebug)
        QObject.connect(self.buttonNext, SIGNAL("clicked()"), self.slotNext)
        QObject.connect(self.buttonBack, SIGNAL("clicked()"), self.slotBack)

    def toggleDebug(self):
        if ctx.debugger.isVisible():
            ctx.debugger.hideWindow()
        else:
            ctx.debugger.showWindow()

    def getCur(self,d):
        new   = self.mainStack.currentIndex() + d
        total = self.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    def setCurrent(self,cur=None):
        if cur:
            self.stackMove(cur)

    def slotNext(self):
        _w = self.mainStack.currentWidget()
        _w.execute()
        self.stackMove(self.getCur(+1))

    def slotBack(self):
        self.stackMove(self.getCur(-1))

    def stackMove(self,new):
        self.mainStack.setCurrentIndex(new)
        _w = self.mainStack.currentWidget()
        _w.shown()
        self.screenName.setText(_w.title)
        self.screenDescription.setText(_w.desc)
        self.helpContent.setText(_w.help)

    def createWidgets(self,screens=[]):
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

"""
    count = 0
    def mousePressEvent(self, e):
        if not e.globalX() and not e.globalY():
            OiEvent(self)
            self.count += 1
            if self.count > 10:
                OiEvent2(self)
                self.count = 0

class OiEvent(QMainWindow):
    def __init__(self, parent):
        self.pix = ctx.iconfactory.newPixmap("oi")
        self.w = self.pix.width()
        self.h = self.pix.height()
        QMainWindow.__init__(self, parent, "ewin1", Qt.WStyle_NoBorder)
        self.setFixedSize(self.w, self.h)
        self.top_x = parent.width() - self.w
        self.top_y = parent.height() - self.h
        self.setPaletteBackgroundPixmap(self.pix)
        self.setMask(self.pix.mask())
        self.x = self.top_x
        self.y = parent.height()
        self.move(self.x, self.y)
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.slotTimeTick)
        self.timer.start(50, False)
        self.dir = 0
        self.accel = 20
        self.show()
    
    def slotTimeTick(self):
        if self.dir == 0:
            self.y -= self.accel
            if self.y < self.top_y:
                self.dir = 1
                self.count = 0
                self.y = self.top_y
            if self.accel > 1:
                self.accel -= 1
        elif self.dir == 1:
            self.count += 1
            if self.count > 15:
                self.dir = 2
        elif self.dir == 2:
            self.x += self.accel
            if self.x >= self.top_x + self.pix.width():
                self.timer.stop()
                self.close(True)
                return
            if self.accel < 6:
                self.accel += 1
        self.move(self.x, self.y)

class OiEvent2(QMainWindow):
    def __init__(self, parent):
        self.pix = ctx.iconfactory.newPixmap("oi2")
        self.w = self.pix.width()
        self.h = self.pix.height()
        QMainWindow.__init__(self, parent, "ewin2", Qt.WStyle_NoBorder)
        self.setFixedSize(self.w, self.h)
        self.end = parent.width() + self.w
        self.x = 0 - self.w
        self.y = (parent.height() - self.h)/2
        self.setPaletteBackgroundPixmap(self.pix)
        self.setMask(self.pix.mask())
        self.move(self.x, self.y)
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.slotTimeTick)
        self.timer.start(50, False)
        self.first_y = self.y
        self.dir = 1
        self.show()
    
    def slotTimeTick(self):
        self.x += 2
        
        if self.x >= self.end:
            self.timer.stop()
            self.close(True)
            return

        dif = self.y - self.first_y
        if abs(dif) == 8 and self.dir:
            self.dir = 0
        elif dif >= 8:
            self.dir = -1
        elif dif <= -8:
            self.dir = 1

        if self.dir == 1:
            self.y += 1
        elif self.dir == -1:
            self.y -= 1
        
        self.move(self.x, self.y)
"""
