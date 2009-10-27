#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *


class UserPage(QWidget):
    "first page of wizard which includes user list"
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        lay = QVBoxLayout(self, 0, 10, "lay")
        # Paragraph 1:
        self.paragraph1 = QLabel(self,"paragraph1")
        self.paragraph1.setText(i18n("Welcome to Pardus Migration Tool. You can transfer files and settings from your existing operating systems to Pardus with this application."))
        self.paragraph1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)
        lay.addWidget(self.paragraph1)
        # Paragraph 2:
        self.paragraph2 = QLabel(self,"paragraph2")
        self.paragraph2.setText(i18n("After selecting user, you will be able to copy wallpaper, bookmarks, e-mail accounts, e-mail messages, news accounts, instant messenger accounts and files to Pardus. Please choose the user and click \"next\" to continue..."))
        self.paragraph2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)
        lay.addWidget(self.paragraph2)
        # Users Box:
        self.usersBox = QComboBox(0, self, "usersBox")
        lay.addWidget(self.usersBox)
        # Spaces
        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        lay.addItem(spacer)
