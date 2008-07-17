# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/uis/ui_availablemodules.ui'
#
# Created: Fri Jul 18 00:15:28 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_availableModulesDlg(object):
    def setupUi(self, availableModulesDlg):
        availableModulesDlg.setObjectName("availableModulesDlg")
        availableModulesDlg.setWindowModality(QtCore.Qt.NonModal)
        availableModulesDlg.resize(289,405)
        self.listAllModules = QtGui.QListWidget(availableModulesDlg)
        self.listAllModules.setGeometry(QtCore.QRect(14,12,261,371))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.listAllModules.setFont(font)
        self.listAllModules.setObjectName("listAllModules")

        self.retranslateUi(availableModulesDlg)
        QtCore.QMetaObject.connectSlotsByName(availableModulesDlg)

    def retranslateUi(self, availableModulesDlg):
        availableModulesDlg.setWindowTitle(QtGui.QApplication.translate("availableModulesDlg", "Available Modules", None, QtGui.QApplication.UnicodeUTF8))

