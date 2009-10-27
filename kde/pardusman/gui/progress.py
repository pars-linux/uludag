#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Qt
from PyQt4.QtCore import QEventLoop
#from PyQt4.QtGui import QDialog

# PyKDE
from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KProgressDialog, KApplication

class Progress:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = None

    def started(self, title):
        self.dialog = KProgressDialog(self.parent, "pardusman", title)
        self.dialog.showCancelButton(False)
        self.dialog.show()
        KApplication.kApplication().processEvents()

    def progress(self, msg, percent):
        self.dialog.setLabelText(msg)
        # otherwise KProgressDialog automatically closes itself, sigh
        if percent < 100:
            self.dialog.progressBar().setValue(percent)
        KApplication.kApplication().processEvents(QEventLoop.AllEvents)

    def finished(self):
        if self.dialog:
            self.dialog.done(0)
        self.dialog = None
