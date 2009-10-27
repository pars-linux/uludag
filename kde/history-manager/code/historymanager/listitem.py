#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyKDE4.kdecore import *

from uiitem import Ui_HistoryItemWidget

# Keep this for translation generation
opttrans = {"upgrade":i18n("Upgrade"), "remove":i18n("Removal"), "emerge":i18n("Emerge"), \
            "install":i18n("Installation"), "snapshot":i18n("Snapshot"), "takeback":i18n("Takeback"), \
            "repoupdate":i18n("Repository Update")}

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

        self.op_no = operation[0]
        self.op_type = operation[1]
        self.op_date = operation[2]
        self.op_time = operation[3]
        self.op_pack = operation[4]
        self.op_repo = operation[5]

        self.alias = " - ".join([self.op_date, self.op_time])
        self.op_pack_len = len(self.op_pack)

        self.icon = ":/pics/%s.png" % self.op_type

        if self.settings.contains("%d/label" % self.op_no):
            self.alias = self.settings.value("%d/label" % self.op_no).toString()

        self.ui.labelLabel.setText(self.alias)

        self.ui.typeLabel.setText(i18n("No: %1   Type: %2", self.op_no, i18n(opttrans[self.op_type])))
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

