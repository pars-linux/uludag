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


from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n

from gui.ScreenWidget import ScreenWidget
from gui.progressWidget import Ui_bugWidget


class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Bug Reporting Tool")
    desc = ki18n("Progress Screen")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_bugWidget()
        self.ui.setupUi(self)

    def shown(self):
        pass

    def execute(self):
        summary = self.ui.summary.text()
        description = self.ui.description.toPlainText()
        if len(summary) == 0 or len(description) == 0:
            return False
        else:
            self.shared['summary'] = str(summary)
            self.shared['description'] = str(description)
            return True

    @property
    def shared(self):
        return self.parent().parent().parent().shared_data
