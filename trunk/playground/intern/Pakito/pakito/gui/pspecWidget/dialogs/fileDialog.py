#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *

import kdedesigner

from pakito.gui.pspecWidget.dialogs.fileDialogUI import FileDialogUI

class FileDialog(FileDialogUI):
    def __init__(self, parent = None, file = None, name = None):
        FileDialogUI.__init__(self, parent, name)
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        if file:
            self.cbType.setCurrentText(file[0])
            if file[1]:
                self.chbPermanent.setChecked(True)
            self.lePath.setText(file[2])

    def getResult(self):
        ret = []
        ret.append(str(self.cbType.currentText()))
        if self.chbPermanent.isChecked():
            ret.append("True")
        else:
            ret.append("")
        ret.append(self.lePath.text())
        return ret
