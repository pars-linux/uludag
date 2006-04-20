# -*- coding: utf-8 -*-
# Copyright 2006 TUBİTAK/UEKAE
# Licensed under GPL v2 or later at your option
#
# This file is based on code
# Copyright (c) 2004 Daniel Molkentin <molkentin@kde.org>
# based on code by Cornelius Schumacher <schumacher@kde.org>
# Licensed under GNU Library General Public v2 or later at your option

from qt import *
from kdeui import *
from kdecore import *

class ClickLineEdit(KLineEdit):
    def __init__(self,parent):
        KLineEdit.__init__(self,parent)
        self.clickMessage = i18n("Enter some text to search")
        self.repaint()

    def setText(self,text):
        self.repaint()
        KLineEdit.setText(self,text)
        
    def drawContents(self,painter):
        if not self.hasFocus():
            tmp = painter.pen()
            painter.setPen(self.palette().color(QPalette.Disabled, QColorGroup.Text))
            cr = self.contentsRect()
            cr.setLeft(cr.left() + 3)
            painter.drawText(cr,Qt.AlignAuto|Qt.AlignVCenter,self.clickMessage)
            painter.setPen(tmp)
        else:
            KLineEdit.drawContents(self,painter)

    def focusInEvent(self,event):
        self.clear()
        self.repaint()
        KLineEdit.focusInEvent(self,event)

    def focusOutEvent(self,event):
        self.repaint()
        KLineEdit.focusOutEvent(self,event)
