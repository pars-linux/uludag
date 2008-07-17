# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/uis/ui_mainwindow.ui'
#
# Created: Fri Jul 18 00:15:28 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(329,505)
        self.listModules = QtGui.QListWidget(moduleManagerDlg)
        self.listModules.setGeometry(QtCore.QRect(10,68,311,391))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setStrikeOut(False)
        self.listModules.setFont(font)
        self.listModules.setAcceptDrops(False)
        self.listModules.setSortingEnabled(True)
        self.listModules.setObjectName("listModules")
        self.lblSearch = QtGui.QLabel(moduleManagerDlg)
        self.lblSearch.setGeometry(QtCore.QRect(9,9,28,28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lblSearch.setFont(font)
        self.lblSearch.setScaledContents(True)
        self.lblSearch.setWordWrap(True)
        self.lblSearch.setObjectName("lblSearch")
        self.editSearch = QtGui.QLineEdit(moduleManagerDlg)
        self.editSearch.setGeometry(QtCore.QRect(47,8,241,28))
        self.editSearch.setMaximumSize(QtCore.QSize(16777215,28))
        self.editSearch.setObjectName("editSearch")
        self.btnSearch = QtGui.QPushButton(moduleManagerDlg)
        self.btnSearch.setGeometry(QtCore.QRect(292,8,30,28))
        self.btnSearch.setMaximumSize(QtCore.QSize(30,28))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.btnSearch.setFont(font)
        self.btnSearch.setObjectName("btnSearch")
        self.label = QtGui.QLabel(moduleManagerDlg)
        self.label.setGeometry(QtCore.QRect(10,44,171,22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnNewModule = QtGui.QPushButton(moduleManagerDlg)
        self.btnNewModule.setGeometry(QtCore.QRect(10,466,121,32))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnNewModule.setFont(font)
        self.btnNewModule.setObjectName("btnNewModule")
        self.lblSearch.setBuddy(self.editSearch)

        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)
        moduleManagerDlg.setTabOrder(self.editSearch,self.btnSearch)
        moduleManagerDlg.setTabOrder(self.btnSearch,self.listModules)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Kernel Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", "Ara: ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("moduleManagerDlg", "Currently loaded modules", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNewModule.setText(QtGui.QApplication.translate("moduleManagerDlg", "Load New Module", None, QtGui.QApplication.UnicodeUTF8))

