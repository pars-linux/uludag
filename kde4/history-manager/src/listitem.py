#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n

from interface import getEmptyHistory

class OperationDataModel(QAbstractTableModel):
    def __init__(self):
        super(OperationDataModel, self).__init__()

        self.items = []

    def rowCount(self, index=QModelIndex()):
        return len(self.items)

    def columnCount(self, index=QModelIndex()):
        return 4

    def getPackages(self, index):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]
        column = index.column()

        return QVariant(item.op_pack)

    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows-1)

        for row in range(rows):
            self.items.insert(position+row, getEmptyHistory())

        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex, position, position + row -1)

        self.items = self.items[:position] + self.items[position+rows:]

        self.endRemoveRows()
        return True

    def sortByNumber(self):
        self.items = sorted(self.items)
        self.reset()

    def getTypeTr(self, index):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]
        column = index.column()

        return QVariant(item.op_type_tr)

    def getTypeInt(self, index):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]
        column = index.column()

        return QVariant(item.op_type_int)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()

        item = self.items[index.row()]
        column = index.column()

        if role == Qt.DisplayRole:
            if column == ICON:
                return QVariant(item.icon)
            elif column == NUMBER:
                return QVariant(item.op_no)
            elif column == DATE:
                return QVariant(item.op_date)
            elif column == TIME:
                return QVariant(item.op_time)
        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if not index.isValid() and 0 <= index.row() < len(self.item):
            return False

        item = self.items(index.row())
        column = index.column()

        if column == ICON:
            item.icon = value.toString()
        if column == NUMBER:
            item.op_no = value.toString()
        if column == DATE:
            item.op_date = value.toString()
        if column == TIME:
            item.op_time = value.toString()

        self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
        return True

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role !=  Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            if section == ICON:
                return QVariant("")
            elif section == NUMBER:
                return QVariant(ki18n("No"))
            elif section == DATE:
                return QVariant(ki18n("Date"))
            elif section == TIME:
                return QVariant(ki18n("Time"))
        return QVariant(int(section+1))

class NewOperation:
    def __init__(self, operation):
        self.op_no = operation.no
        self.op_type = operation.type
        self.op_date = operation.date
        self.op_time = operation.time
        self.op_pack = operation.packages
        self.op_tag = operation.tag

        self.op_type_int = 0
        self.op_type_tr = ""
        self.icon = None

        if self.op_type == 'snapshot':
            self.icon = ":/icons/update.png"
            self.op_type_int = 1
            self.op_type_tr = ki18n("snapshot")
        elif self.op_type == 'upgrade':
            self.icon = ":/icons/upgrade.png"
            self.op_type_int = 2
            self.op_type_tr = ki18n("upgrade")
        elif self.op_type == 'remove':
            self.icon = ":/icons/remove.png"
            self.op_type_int = 3
            self.op_type_tr = ki18n("remove")
        elif self.op_type == 'install':
            self.icon = ":/icons/install.png"
            self.op_type_int = 4
            self.op_type_tr = ki18n("install")
        elif self.op_type == 'takeback':
            self.icon = ":/icons/takeback.png"
            self.op_type_int = 5
            self.op_type_tr = ki18n("takeback")

    def __cmp__(self, ot):
        return self.op_no == ot.getOpNo()
