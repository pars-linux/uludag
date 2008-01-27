# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

from PyQt4 import QtGui
from PyQt4.QtCore import *

import time
import yali4.gui.context as ctx

def pix(name):
    return QtGui.QPixmap(":/gui/pics/%s.png" % name)

class YaliSteps(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        # poor man's status icons =)
        # No no no; I'm rich now :-p
        self.iconFree      = pix("iconFree")
        self.iconWorking   = pix("iconWorking")
        self.iconDone      = pix("iconDone")
        self.iconFailed    = pix("iconFailed")

        self.StepsLayout = QtGui.QVBoxLayout(self)
        self.items = []

    def setOperations(self, stepItems):
        for item in stepItems:
            _item = stepItem(self,item["text"],item["operation"])
            self.StepsLayout.addLayout(_item.getLayout())
            self.items.append(_item)

    def slotRunOperations(self):
        for item in self.items:
            if not item.status:
                item.runOperation()
                time.sleep(0.5)

class stepItem:
    def __init__(self,parent,text,operation):
        self.text = text
        self.parent = parent
        self.operation = operation
        self.status = False

        self.mainLayout = QtGui.QHBoxLayout(None)

        self.pixmapLabel = QtGui.QLabel(parent,"StatusPixmap")
        self.pixmapLabel.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,
                                                   QSizePolicy.Fixed,0,0,
                                                   self.pixmapLabel.sizePolicy().hasHeightForWidth()))
        self.pixmapLabel.setPixmap(parent.iconFree)
        self.pixmapLabel.setScaledContents(1)
        self.mainLayout.addWidget(self.pixmapLabel)

        self.textLabel = QtGui.QLabel(parent)
        #self.textLabel.setText(text)
        self.mainLayout.addWidget(self.textLabel)

    def getLayout(self):
        return self.mainLayout

    def runOperation(self):
        self.textLabel.setText("<b>%s</b>" % self.text)
        qApp.processEvents()
        self.pixmapLabel.setPixmap(self.parent.iconWorking)
        self.status = self.operation()
        self.textLabel.setText(self.text)
        ctx.debugger.log("Running step : %s" % self.text)
        if self.status:
            self.pixmapLabel.setPixmap(self.parent.iconDone)
        else:
            self.pixmapLabel.setPixmap(self.parent.iconFailed)
        qApp.processEvents()

