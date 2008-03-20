# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from PyQt4 import QtGui
from PyQt4.QtCore import *

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import yali4.gui.context as ctx
from yali4.gui.Ui.partresize import Ui_PartResizeWidget
from yali4.gui.Ui.autopartquestion import Ui_autoPartQuestion

class ResizeWidget(QtGui.QWidget):

    def __init__(self, dev, part):
        QtGui.QWidget.__init__(self, ctx.mainScreen.ui)
        self.ui = Ui_PartResizeWidget()
        self.ui.setupUi(self)
        self.setStyleSheet("""
                QSlider::groove:horizontal {
                     border: 1px solid #999999;
                     height: 12px;
                     background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4);
                     margin: 2px 0;
                 }

                 QSlider::handle:horizontal {
                     background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);
                     border: 1px solid #5c5c5c;
                     width: 18px;
                     margin: 0 0;
                     border-radius: 2px;
                 }

                QFrame#mainFrame {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }

                QWidget#PartResizeWidget {
                    background-image: url(:/gui/pics/trans.png); 
                }
        """)
        self.resize(ctx.mainScreen.ui.size())
        self.dev = dev
        self.part = part
        minSize = self.part.getMinResizeMB()
        maxSize = self.part.getMB()
        self.ui.resizeMB.setMaximum(maxSize)
        self.ui.resizeMBSlider.setMaximum(maxSize)
        self.ui.resizeMB.setMinimum(minSize)
        self.ui.resizeMBSlider.setMinimum(minSize)
        self.connect(self.ui.cancelButton, SIGNAL("clicked()"), self.hide)
        self.connect(self.ui.resizeButton, SIGNAL("clicked()"), self.slotResize)

    def slotResize(self):
        ctx.debugger.log("Resize started on partition %s " % self.part.getPath())
        self.dev.resizePartition(self.part._fsname, int(self.ui.resizeMB.value()),self.part)

class AutoPartQuestionWidget(QtGui.QWidget):

    def __init__(self, rootWidget):
        QtGui.QWidget.__init__(self, ctx.mainScreen.ui)
        self.ui = Ui_autoPartQuestion()
        self.ui.setupUi(self)
        self.setStyleSheet("""
                QFrame#mainFrame {
                    background-image: url(:/gui/pics/transBlack.png);
                    border: 1px solid #BBB;
                    border-radius:8px;
                }
                QWidget#autoPartQuestion {
                    background-image: url(:/gui/pics/trans.png); 
                }
        """)
        self.rootWidget = rootWidget
        self.resize(ctx.mainScreen.ui.size())
        self.connect(self.ui.useSelectedButton, SIGNAL("clicked()"), self.slotUseSelected)

    def slotUseSelected(self):
        self.rootWidget.execute_(True)
        self.hide()

