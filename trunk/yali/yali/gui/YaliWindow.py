# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from os.path import join
from qt import *

import gettext
__trans = gettext.translation('yali', fallback=True)
_ = __trans.ugettext


import yali.gui.context as ctx

import GUITop
import GUIContentStack
import GUIHelp
import GUIBottom

##
# Widget for YaliWindow (you can call it MainWindow too ;).
class Widget(QMainWindow):

    def __init__(self, *args):
        apply(QMainWindow.__init__, (self,) + args)

        self.topWidget = GUITop.Widget(self)
        self.contentWidget = GUIContentStack.Widget(self)
        self.helpWidget = GUIHelp.Widget(self)
        self.bottomWidget = GUIBottom.Widget(self)


        # Place the widgets using layouts and yada, yada, yada...
        self.__setUpWidgets()


        self.connect(self, PYSIGNAL("signalWindowSize"),
                     self.topWidget.slotResize)
        self.connect(self, PYSIGNAL("signalWindowSize"),
                     self.helpWidget.slotResize)

        self.connect(ctx.screens, PYSIGNAL("nextButtonDisabled"),
                     self.slotNextDisabled)
        self.connect(ctx.screens, PYSIGNAL("prevButtonDisabled"),
                     self.slotPrevDisabled)
        self.connect(ctx.screens, PYSIGNAL("nextButtonEnabled"),
                     self.slotNextEnabled)
        self.connect(ctx.screens, PYSIGNAL("prevButtonEnabled"),
                     self.slotPrevEnabled)

        self.setPaletteBackgroundColor(ctx.consts.bg_color)
        self.setPaletteForegroundColor(ctx.consts.fg_color)

    ##
    # set up the main window layout...
    def __setUpWidgets(self):
#        l = self.layout()

        main = QVBoxLayout(self)
        main.setSpacing(0)
        main.setMargin(0)

        main.addWidget(self.topWidget)

        center = QHBoxLayout()
        center.setSpacing(20)
        center.setMargin(20)
        center.addWidget(self.contentWidget)
        
        centerRight = QVBoxLayout()
        centerRight.setSpacing(10)
        centerRight.setMargin(0)
        centerRight.addWidget(self.helpWidget)

        centerRight.addStretch(1)
        center.addLayout(centerRight)

        main.addLayout(center)
        
        main.addWidget(self.bottomWidget)


    # Enable/Disable buttons

    def slotNextDisabled(self):
        self.bottomWidget.nextButton.setEnabled(False)

    def slotPrevDisabled(self):
        self.bottomWidget.prevButton.setEnabled(False)

    def slotNextEnabled(self):
        self.bottomWidget.nextButton.setEnabled(True)

    def slotPrevEnabled(self):
        self.bottomWidget.prevButton.setEnabled(True)


    ##
    # resizeEvent notifies others..
    # @param e(QResizeEvent): Qt resize event
    def resizeEvent(self, e):
        self.emit(PYSIGNAL("signalWindowSize"), (self, e.size()))


    def mousePressEvent(self, e):
        if not e.globalX() and not e.globalY():
            OiEvent(self)


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

