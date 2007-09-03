#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *
from historyDialogUI import HistoryDialogUI

class HistoryDialog(HistoryDialogUI):
    def __init__(self, parent = None, release = None, name = None):
        HistoryDialogUI.__init__(self, parent, name)
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        if release:
            self.niRelease.setValue(int(release[0]))

    def getResult(self):
        pass
