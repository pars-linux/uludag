# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/ui_mainwindow.ui'
#
# Created: Sun Jul 13 21:59:55 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(308,427)
        self.listModules = QtGui.QListWidget(moduleManagerDlg)
        self.listModules.setGeometry(QtCore.QRect(8,43,291,353))
        self.listModules.setObjectName("listModules")
        self.chkLoaded = QtGui.QCheckBox(moduleManagerDlg)
        self.chkLoaded.setGeometry(QtCore.QRect(7,402,299,24))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.chkLoaded.setFont(font)
        self.chkLoaded.setObjectName("chkLoaded")
        self.lblSearch = QtGui.QLabel(moduleManagerDlg)
        self.lblSearch.setGeometry(QtCore.QRect(9,9,28,28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lblSearch.setFont(font)
        self.lblSearch.setScaledContents(True)
        self.lblSearch.setWordWrap(True)
        self.lblSearch.setObjectName("lblSearch")
        self.editSearch = QtGui.QLineEdit(moduleManagerDlg)
        self.editSearch.setGeometry(QtCore.QRect(37,8,224,28))
        self.editSearch.setMaximumSize(QtCore.QSize(16777215,28))
        self.editSearch.setObjectName("editSearch")
        self.btnSearch = QtGui.QPushButton(moduleManagerDlg)
        self.btnSearch.setGeometry(QtCore.QRect(271,8,30,28))
        self.btnSearch.setMaximumSize(QtCore.QSize(30,28))
        font = QtGui.QFont()
        font.setPointSize(6)
        self.btnSearch.setFont(font)
        self.btnSearch.setObjectName("btnSearch")

        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Kernel Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLoaded.setText(QtGui.QApplication.translate("moduleManagerDlg", "Sadece yüklü olanları listele", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", "Ara  ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", ">>", None, QtGui.QApplication.UnicodeUTF8))

