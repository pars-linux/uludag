#!/usr/bin/python
# -*- coding: utf-8 -*-

#qlabel
from qt import *
#kglobal settings
from kdecore import *

class PLinkLabel(QLabel):
    def __init__(self, parent, name=0, flags=0):
        QLabel.__init__(self, parent, name, flags)
        self.color = KGlobalSettings.linkColor()
        self.setPaletteForegroundColor(self.color)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.method = None
        # bold, italic etc. options will be added.
        # method may take arguments

    def mousePressEvent(self, event):
        if self.method:
            self.method()

    def setLinkText(self, text):
        self.setText(text)

