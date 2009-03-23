#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyKDE4.kdecore import *

import inspect
from new import instancemethod

ICON, DATE, TIME = range(3)

class OperationDataModel(QAbstractItemModel):
    def __init__(self):
        super(OperationDataModel, self).__init__()

        self.items = []

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def columnCount(self, index=QModelIndex()):
        return 3

    def index(self, row, column, parent=QModelIndex()):
        return QAbstractItemModel.createIndex(self, row, column)

    def parent(self, index):
        return QModelIndex()

    def getPackages(self, index):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]
        column = index.column()

        return QVariant(item.op_pack)

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex, position, position + row -1)

        self.items = self.items[:position] + self.items[position+rows:]

        self.endRemoveRows()
        return True

    def sortByNumber(self):
        self.items = sorted(self.items)
        self.reset()

    def getProperty(self, index, property):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]

        members = inspect.getmembers(item)

        i = 3
        while i < len(members):
            if not isinstance(members[i][1], instancemethod):
                if property == members[i][0]:
                    return QVariant(members[i][1])
            i += 1

        return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == DATE:
                return QVariant(item.op_date)
            elif column == TIME:
                return QVariant(item.op_time)
        elif role == Qt.DecorationRole:
            if column == ICON:
                return QVariant(QPixmap(item.icon))

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() and 0 <= index.row() < len(self.item):
            return False

        item = self.items(index.row())
        column = index.column()

        if role == Qt.DisplayRole:
            if column == DATE:
                item.op_date = value.toString()
            if column == TIME:
                item.op_time = value.toString()

        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.TextAlignmentRole:
            if orientation == Qt.Horizontal:
                return QVariant(int(Qt.AlignLeft|Qt.AlignVCenter))
            return QVariant(int(Qt.AlignRight|Qt.AlignVCenter))

        if role !=  Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            if section == ICON:
                return QVariant("")
            elif section == DATE:
                return QVariant(i18n("Date"))
            elif section == TIME:
                return QVariant(i18n("Time"))
        elif orientation == Qt.Vertical:
            return QVariant(self.items[section].op_no)

        return QVariant(int(section+1))

class NewOperation:
    def __init__(self, operation):
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

        self.op_type_int = 0
        self.op_type_tr = ""
        self.icon = None

        if self.op_type == 'snapshot':
            self.icon = ":/pics/snapshot.png"
            self.op_type_int = 1
            self.op_type_tr = i18n("snapshot")
        elif self.op_type == 'upgrade':
            self.icon = ":/pics/upgrade.png"
            self.op_type_int = 2
            self.op_type_tr = i18n("upgrade")
        elif self.op_type == 'remove':
            self.icon = ":/pics/remove.png"
            self.op_type_int = 3
            self.op_type_tr = i18n("remove")
        elif self.op_type == 'install':
            self.icon = ":/pics/install.png"
            self.op_type_int = 4
            self.op_type_tr = i18n("install")
        elif self.op_type == 'takeback':
            self.icon = ":/pics/takeback.png"
            self.op_type_int = 5
            self.op_type_tr = i18n("takeback")
        else:
            self.icon = "?"
            self.op_type_int = 6
            self.op_type_tr = i18n("unknown")

class SortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(SortFilterProxyModel, self).__init__(parent)

        self.sortby = None

    def lessThan(self, left, right):
        lno = self.sourceModel().getProperty(left, "op_no").toInt()
        rno = self.sourceModel().getProperty(right, "op_no").toInt()
        ltype = self.sourceModel().getProperty(left, "op_type").toString()
        rtype = self.sourceModel().getProperty(right, "op_type").toString()

        if self.sortby == None or self.sortby == "all":
            return lno < rno

        if ltype == rtype == self.sortby:
            return lno < rno

        if ltype == self.sortby:
            return False

        if rtype == self.sortby:
            return True

        return lno < rno
