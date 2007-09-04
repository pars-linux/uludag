#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *
from kdeui import *
from kdecore import i18n, KGlobal, KIcon
from kfile import *

import os.path
import shutil

from patchDialogUI import PatchDialogUI

class PatchDialog(PatchDialogUI):
    def __init__(self, parent = None, patch = None, name = None):
        PatchDialogUI.__init__(self, parent, name)
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        self.connect(self.pbPatch, SIGNAL("clicked()"), self.slotPatch)
        il = KGlobal.iconLoader()
        self.pbPatch.setIconSet(il.loadIconSet("fileopen", KIcon.Toolbar))
        if patch:
            self.niLevel.setValue(int(patch[0]))
            self.cbType.setCurrentText(patch[1])
            self.lePatch.setText(patch[2])

    def slotPatch(self):
        self.realLoc = KFileDialog.getOpenFileName(QString.null, QString.null, self, i18n("Select Patch File"))
        self.lePatch.setText(os.path.split(str(self.realLoc))[1])

    def getResult(self):
        res = []
        if self.niLevel.value() == 0:
            lev = ""
        else:
            lev = str(self.niLevel.value())
        res.append(lev)
        res.append(str(self.cbType.currentText()))
        res.append(str(self.lePatch.text()))
        res.append(self.realLoc)
        return res

