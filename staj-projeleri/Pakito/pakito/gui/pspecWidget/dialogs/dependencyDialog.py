#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *

import kdedesigner

from pakito.gui.pspecWidget.dialogs.dependencyDialogUI import DependencyDialogUI

class DependencyDialog(DependencyDialogUI):
    def __init__(self, dep = None, parent = None, title = None, secondLabel = None, name = None):
        DependencyDialogUI.__init__(self, parent, name)
        self.connect(self.btnOk, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.btnCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
        if dep:
            cond = dep[0].split()
            if len(cond) == 3:
                self.cbRelease.setCurrentText(cond[0])
                self.cbToFrom.setCurrentText(cond[1])
                self.leCondition.setText(cond[2])
            self.leDependency.setText(dep[1])
        if title:
            self.setCaption(title)
        if secondLabel:
            self.lblDependency.setText(secondLabel)

    def getResult(self):
        rel = str(self.cbRelease.currentText()).strip()
        toFrom = str(self.cbToFrom.currentText()).strip()
        cond =str(self.leCondition.text()).strip()
        if rel == "" or toFrom == "" or cond == "":
            return "", str(self.leDependency.text())
        else:
            return "%s %s %s" % (rel, toFrom, cond), str(self.leDependency.text())


