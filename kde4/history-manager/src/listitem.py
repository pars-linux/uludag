#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QListWidgetItem

class NewWidgetItem(QListWidgetItem):
    """ class for listviewitem's """

    def __init__(self, parent, operation):
        QListWidgetItem.__init__(self, parent)

        self.op_no = operation.no
        self.op_type = operation.type
        self.op_date = operation.date
        self.op_time = operation.time
        self.op_pack = operation.packages
        self.op_tag = operation.tag
        self.op_type_int = 0
        self.op_type_tr = ""

        self.setText("%s | %s - %s" % (self.op_no, self.op_date, self.op_time))

        # op_type_int = 0 -> All Operations
        if self.op_type == 'snapshot':
            # self.setIcon(0, loadIcon("snapshot", KIcon.Small))
            self.op_type_int = 1
            # self.op_type_tr = i18n("snapshot")
        elif self.op_type == 'upgrade':
            # self.setPixmap(0, loadIcon("upgrade", KIcon.Small))
            self.op_type_int = 2
            # self.op_type_tr = i18n("upgrade")
        elif self.op_type == 'remove':
            # self.setPixmap(0, loadIcon("remove", KIcon.Small))
            self.op_type_int = 3
            # self.op_type_tr = i18n("remove")
        elif self.op_type == 'install':
            # self.setPixmap(0, loadIcon("install", KIcon.Small))
            self.op_type_int = 4
            # self.op_type_tr = i18n("install")
        elif self.op_type == 'takeback':
            # self.setPixmap(0, loadIcon("takeback", KIcon.Small))
            self.op_type_int = 5
            # self.op_type_tr = i18n("takeback")

    def getNumPackages(self):
        return len(self.op_pack)

    def getOpNo(self):
        return self.op_no

    def getDate(self):
        return self.op_date

    def getTime(self):
        return self.op_time

    def getType(self):
        return self.op_type

    def getTypeInt(self):
        return self.op_type_int

    def getTypeTr(self):
        return self.op_type_tr

