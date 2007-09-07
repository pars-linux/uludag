#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *
from historyDialogUI import HistoryDialogUI

class HistoryDialog(HistoryDialogUI):
    def __init__(self, parent = None, release = None, relValue = 1, name = None):
        HistoryDialogUI.__init__(self, parent, name)
        self.dwDate.setDate(QDate.currentDate())
        self.niRelease.setValue(relValue)
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.leVersion.setFocus()
        if release:
            self.niRelease.setValue(int(release[0]))
            self.dwDate.setDate(QDate.fromString(release[1], Qt.ISODate))
            self.leVersion.setText(release[2])
            self.cbType.setCurrentText(release[3])
            self.teComment.setText(release[4])
            self.leName.setText(release[5])
            self.leEmail.setText(release[6])

    def getResult(self):
        res = []
        res.append(str(self.niRelease.value()))
        res.append(str(self.dwDate.date().toString("yyyy-MM-dd")))
        res.append(str(self.leVersion.text()))
        res.append(str(self.cbType.currentText()))
        res.append(unicode(self.teComment.text()))
        res.append(unicode(self.leName.text()))
        res.append(str(self.leEmail.text()))
        return res
