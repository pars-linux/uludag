# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'module-manager.ui'
#
# Created: Thu Jul 10 14:19:30 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(400,395)
        self.gridLayoutWidget = QtGui.QWidget(moduleManagerDlg)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(30,30,341,311))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.listModule = QtGui.QListWidget(self.gridLayoutWidget)
        self.listModule.setObjectName("listModule")
        self.gridLayout_2.addWidget(self.listModule,0,0,1,1)
        self.btnListModules = QtGui.QPushButton(moduleManagerDlg)
        self.btnListModules.setGeometry(QtCore.QRect(30,354,86,30))
        self.btnListModules.setObjectName("btnListModules")

        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.btnListModules.setText(QtGui.QApplication.translate("moduleManagerDlg", "Listele", None, QtGui.QApplication.UnicodeUTF8))

