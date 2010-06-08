#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Rasta RST Editor
    2010 - Gökmen Göksel <gokmen:pardus.org.tr> """

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as Published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import QAbstractTableModel

class LogTableModel(QAbstractTableModel):
    def __init__(self, logs, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = logs
        self.headerdata = ["Line", "Message"]

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.headerdata)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()
