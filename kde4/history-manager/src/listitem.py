#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyKDE4.kdecore import *

from uiitem import Ui_HistoryItemWidget

class HistoryItem(QListWidgetItem):
    def __init__(self, parent, no):
        QListWidgetItem.__init__(self, parent)

        self.no = no

    def __lt__(self, other):
        return int(self.no) < int(other.no)

class NewOperation(QWidget):
    def __init__(self, operation, parent=None):
        super(NewOperation, self).__init__(parent)

        self.parent = parent
        self.ui = Ui_HistoryItemWidget()
        self.ui.setupUi(self)
        self.settings = QSettings()

        self.toggled = False
        self.toggleButtons()

        self.op_no = operation.no
        self.op_type = operation.type
        self.op_date = operation.date
        self.op_time = operation.time
        self.op_pack = []
        self.op = operation
        self.alias = " - ".join([self.op_date, self.op_time])

        for i in operation.packages:
            self.op_pack.append(i.__str__())

        self.op_tag = operation.tag
        self.op_pack_len = len(self.op_pack)

        self.icon = ":/pics/%s.png" % self.op_type

        if self.op_type == 'snapshot':
            self.op_type_tr = i18n("snapshot")
        elif self.op_type == 'upgrade':
            self.op_type_tr = i18n("upgrade")
        elif self.op_type == 'remove':
            self.op_type_tr = i18n("remove")
        elif self.op_type == 'install':
            self.op_type_tr = i18n("install")
        elif self.op_type == 'takeback':
            self.op_type_tr = i18n("takeback")
        elif self.op_type == "repoupdate":
            self.op_type_tr = i18n("repo update")

        if self.settings.contains("%d/label" % self.op_no):
            self.alias = self.settings.value("%d/label" % self.op_no).toString()

        self.ui.labelLabel.setText(self.alias)

        self.ui.typeLabel.setText("No: %d   Type: %s" % (self.op_no, self.op_type_tr))
        self.ui.iconLabel.setPixmap(QPixmap(self.icon))

        self.connect(self.ui.restorePB, SIGNAL("clicked()"), self.parent.takeBack)
        self.connect(self.ui.detailsPB, SIGNAL("clicked()"), self.parent.loadDetails)
        self.connect(self.ui.planPB, SIGNAL("clicked()"), self.parent.loadPlan)

    def setAlias(self, txt):
        self.alias = txt
        self.settings.setValue("%d/label" % self.op_no, QVariant(self.alias))
        self.ui.labelLabel.setText(self.alias)

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

