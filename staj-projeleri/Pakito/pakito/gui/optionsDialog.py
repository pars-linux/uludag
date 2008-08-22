#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import SIGNAL, SLOT
import kdedesigner

from pakito.gui.optionsDialogUI import OptionsDialogUI

class OptionsDialog(OptionsDialogUI):
    def __init__(self, parent = None, name = None):
        OptionsDialogUI.__init__(self, parent, name)
        self.connect(self.pbOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.pbCancel, SIGNAL("clicked()"), self, SLOT("reject()"))