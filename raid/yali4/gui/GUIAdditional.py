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

    def __init__(self, dev, part, rootWidget):
        QtGui.QWidget.__init__(self, ctx.mainScreen.ui)
        self.ui = Ui_PartResizeWidget()
        self.ui.setupUi(self)
        self.rootWidget = rootWidget
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

        if minSize == 0:
            self.ui.resizeMB.setVisible(False)
            self.ui.resizeMBSlider.setVisible(False)
            self.ui.resizeButton.setVisible(False)
            self.ui.label.setText(_("""<p><span style="color:#FFF"><b>It seems this partition is not ready for resizing.</b></span></p>"""))
        else:
            maxSize = self.part.getMB()
            self.ui.resizeMB.setMaximum(maxSize)
            self.ui.resizeMBSlider.setMaximum(maxSize)
            self.ui.resizeMB.setMinimum(minSize)
            self.ui.resizeMBSlider.setMinimum(minSize)
            self.connect(self.ui.resizeButton, SIGNAL("clicked()"), self.slotResize)

        self.connect(self.ui.cancelButton, SIGNAL("clicked()"), self.hide)

    def slotResize(self):
        self.hide()
        ctx.yali.info.updateAndShow(_("Resizing to %s MB..") % (self.ui.resizeMB.value()))
        ctx.debugger.log("Resize started on partition %s " % self.part.getPath())
        QTimer.singleShot(500,self.res)

    def res(self):
        self.dev.resizePartition(self.part._fsname, int(self.ui.resizeMB.value()),self.part)
        self.rootWidget.update()
        ctx.yali.info.hide()

class AutoPartQuestionWidget(QtGui.QWidget):

    def __init__(self, rootWidget, partList):
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

        self.connect(self.ui.bestChoice, SIGNAL("clicked()"), self.slotDisableList)
        self.connect(self.ui.userChoice, SIGNAL("clicked()"), self.slotEnableList)
        self.connect(self.ui.useSelectedButton, SIGNAL("clicked()"), self.slotUseSelected)

        for part in partList:
            pi = PartitionItem(self.ui.partition_list, part)

        self.ui.bestChoice.toggle()
        self.slotDisableList()
        self.resize(ctx.mainScreen.ui.size())

    def slotEnableList(self):
        self.ui.partition_list.setEnabled(True)

    def slotDisableList(self):
        self.rootWidget.autoPartPartition = self.ui.partition_list.item(0).getPartition()
        self.ui.partition_list.setEnabled(False)

    def slotUseSelected(self):
        self.hide()
        if self.ui.partition_list.isEnabled():
            self.rootWidget.autoPartPartition = self.ui.partition_list.currentItem().getPartition()
        ctx.mainScreen.processEvents()
        self.rootWidget.execute_(True)

class PartitionItem(QtGui.QListWidgetItem):

    def __init__(self, parent, _part):
        part = _part["partition"]
        text = _("(%s) [%s] Size : %s - Free : %s" % (part.getDevice().getName(),
                                                      part.getFSLabel() or _("Partition %d") % part.getMinor(),
                                                      part.getSizeStr(),
                                                      part.getSizeStr(_part["newSize"])))
        QtGui.QListWidgetItem.__init__(self, text, parent)
        self.part = _part

    def getPartition(self):
        return self.part

