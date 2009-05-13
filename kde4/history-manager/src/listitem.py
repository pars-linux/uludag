#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyKDE4.kdecore import *

from uiitem import Ui_HistoryItemWidget

class HistoryItem(QListWidgetItem):
    def __init__(self, parent):
        QListWidgetItem.__init__(self, parent)

class NewOperation(QWidget):
    def __init__(self, operation, parent=None):
        super(NewOperation, self).__init__(None)

        self.parent = parent
        self.ui = Ui_HistoryItemWidget()
        self.ui.setupUi(self)

        self.toggled = False
        self.toggleButtons()

        self.op_no = operation.no
        self.op_type = operation.type
        self.op_date = operation.date
        self.op_time = operation.time
        self.op_pack = []
        self.op = operation

        for i in operation.packages:
            self.op_pack.append(i.__str__())

        self.op_tag = operation.tag
        self.op_pack_len = len(self.op_pack)

        self.icon = ":/pics/%s.png" % self.op_type

        if self.op_type == 'snapshot':
            self.op_type_int = 1
            self.op_type_tr = i18n("snapshot")
        elif self.op_type == 'upgrade':
            self.op_type_int = 2
            self.op_type_tr = i18n("upgrade")
        elif self.op_type == 'remove':
            self.op_type_int = 3
            self.op_type_tr = i18n("remove")
        elif self.op_type == 'install':
            self.op_type_int = 4
            self.op_type_tr = i18n("install")
        elif self.op_type == 'takeback':
            self.op_type_int = 5
            self.op_type_tr = i18n("takeback")
        elif self.op_type == "repoupdate":
            self.op_type_int = 6
            self.op_type_tr = i18n("repo update")

        self.ui.labelLabel.setText(" - ".join([self.op_date, self.op_time]))
        self.ui.typeLabel.setText("No: %d   Type: %s" % (self.op_no, self.op_type_tr))
        self.ui.iconLabel.setPixmap(QPixmap(self.icon))

        self.connect(self.ui.restorePB, SIGNAL("clicked()"), self.parent.takeBack)
        self.connect(self.ui.detailsPB, SIGNAL("clicked()"), self.parent.loadDetails)
        self.connect(self.ui.planPB, SIGNAL("clicked()"), self.parent.loadPlan)

    def enterEvent(self, event):
        if not self.toggled:
            self.toggleButtons(True)
            self.toggled = True

    def leaveEvent(self, event):
        if self.toggled:
            self.toggleButtons()
            self.toggled = False

    def toggleButtons(self, toggle=False):
        self.ui.planPB.setVisible(toggle)
        self.ui.restorePB.setVisible(toggle)
        self.ui.detailsPB.setVisible(toggle)

    def __cmp__(self, other):
        return cmp(int(self.op_no), int(other.op_no))
