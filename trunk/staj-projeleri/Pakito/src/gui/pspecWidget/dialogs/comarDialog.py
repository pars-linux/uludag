#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *
from kdecore import KGlobal, KIcon, i18n
from kfile import KFileDialog

import os

from comarDialogUI import COMARDialogUI

class COMARDialog(COMARDialogUI):
    def __init__(self, parent = None, comar = None, name= None):
        COMARDialogUI.__init__(self, parent, name)
        self.realLoc = ""
        il = KGlobal.iconLoader()
        self.pbFile.setIconSet(il.loadIconSet("fileopen", KIcon.Toolbar))
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.connect(self.pbFile, SIGNAL("clicked()"), self.slotFile)
        if comar:
            self.cbProvides.setCurrentText(comar[0])
            self.leFile.setText(comar[1])

    def slotFile(self):
        self.realLoc = KFileDialog.getOpenFileName(QString.null, QString.null, self, i18n("Select COMAR Script"))
        if not self.realLoc or str(self.realLoc).strip() == "":
            return
        self.leFile.setText(os.path.split(str(self.realLoc))[1])

    def getResult(self):
        res = []
        res.append(str(self.cbProvides.currentText()))
        res.append(str(self.leFile.text()))
        res.append(str(self.realLoc))
        return res
