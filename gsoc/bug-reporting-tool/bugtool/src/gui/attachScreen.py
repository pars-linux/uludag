# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n
from os.path import basename

from gui.ScreenWidget import ScreenWidget
from gui.attachmentsWidget import Ui_bugWidget

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Bug Reporting Tool")
    desc = ki18n("Attachment Screen")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_bugWidget()
        self.ui.setupUi(self)
        QObject.connect(self.ui.addButton, SIGNAL("clicked()"), self.add_file)
        QObject.connect(self.ui.removeButton, SIGNAL("clicked()"),
                        self.remove_file)
        self.files = {}
        self.model = QtGui.QStandardItemModel()
        self.ui.filelist.setModel(self.model)

    def add_file(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,
                                                     'Choose a file to attach')
        try:
            f = open(filename)
            content = f.read()
            desc, result = QtGui.QInputDialog.getText(self, 'File description',
                                                      'Describe %s briefly:' %\
                                                      basename(str(filename)))
            if len(desc) == 0:
                desc = basename(str(filename))
        except OSError:
            QtGui.QMessageBox.critical(self, 'Unable to read %s' % filename)

        item = QtGui.QStandardItem(desc)
        self.files[item] = content
        self.model.appendRow(item)

    def remove_file(self):
        for item in self.ui.filelist.selectedIndexes():
            col = item.column()
            row = item.row()
            it = self.model.item(row, col)
            if it in self.files:
                self.files.pop(it)
                self.model.removeRow(row)
        pass

    def shown(self):
        pass

    def execute(self):
        return True


