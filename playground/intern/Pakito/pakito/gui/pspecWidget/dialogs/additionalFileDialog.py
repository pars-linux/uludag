#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *
from kdecore import KGlobal, KIcon, i18n
from kfile import KFileDialog
import kdedesigner

import os

from pakito.gui.pspecWidget.dialogs.additionalFileDialogUI import AdditionalFileDialogUI

class AdditionalFileDialog(AdditionalFileDialogUI):
    def __init__(self, parent = None, file = None, name= None):
        AdditionalFileDialogUI.__init__(self, parent, name)
        self.realLoc = ""
        il = KGlobal.iconLoader()
        self.pbFile.setIconSet(il.loadIconSet("fileopen", KIcon.Toolbar))
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        if file:
            self.cbOwner.setCurrentText(file[0])
            self.lePermission.setText(file[1])
            self.leTarget.setText(file[2])
            self.leFile.setText(file[3])
        self.connect(self.pbFile, SIGNAL("clicked()"), self.slotFile)

    def slotFile(self):
        self.realLoc = KFileDialog.getOpenFileName(QString.null, QString.null, self, i18n("Select Additional File"))
        if not self.realLoc or str(self.realLoc).strip() == "":
            return
        self.leFile.setText(os.path.split(str(self.realLoc))[1])

    def getResult(self):
        res = []
        res.append(str(self.cbOwner.currentText()))
        res.append(str(self.lePermission.text()))
        res.append(str(self.leTarget.text()))
        res.append(str(self.leFile.text()))
        res.append(str(self.realLoc))
        return res
