#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyKDE4.kdecore import *

class NewOperation(QTreeWidgetItem):
    def __init__(self, operation, parent=None):
        super(NewOperation, self).__init__(parent)

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

        self.sortby = 0
        self.icon = ":/pics/%s.png" % self.op_type
        self.op_type_tr = i18n("unknown")
        self.op_type_int = -1

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

        self.setIcon(0, QIcon(self.icon))
        self.setText(1, str(self.op_date))
        self.setText(2, str(self.op_time))

    def setSortColumn(self, val):
        self.sortby = val

    def __lt__(self, other):
        if self.sortby == 0:
            return int(self.op_no) < int(other.op_no)
        return QTreeWidgetItem.__lt__(self, other)

