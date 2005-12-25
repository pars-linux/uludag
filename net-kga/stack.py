#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
import widgets


class Window(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        
        self.setCaption(i18n("Network Settings"))
        self.setMinimumSize(280, 320)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(6)
        self.setCentralWidget(vb)
        
        widgets.HLine(i18n("Computer"), vb)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        QLabel(i18n("Host name:"), hb)
        widgets.Edit(hb)
        
        widgets.HLine(i18n("Name servers"), vb)
        
        self.dns = QListBox(vb)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        QPushButton(i18n("Add"), hb)
        QPushButton(i18n("Remove"), hb)
