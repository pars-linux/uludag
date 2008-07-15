# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/ui_mainwindow.ui'
#
# Created: Tue Jul 15 19:46:22 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(308,451)
        self.listModules = QtGui.QListWidget(moduleManagerDlg)
        self.listModules.setGeometry(QtCore.QRect(8,43,291,353))
        self.listModules.setObjectName("listModules")
        self.chkLoaded = QtGui.QCheckBox(moduleManagerDlg)
        self.chkLoaded.setGeometry(QtCore.QRect(9,428,299,24))
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
        self.label = QtGui.QLabel(moduleManagerDlg)
        self.label.setGeometry(QtCore.QRect(10,399,64,22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.line = QtGui.QFrame(moduleManagerDlg)
        self.line.setGeometry(QtCore.QRect(10,417,291,16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lblCount = QtGui.QLabel(moduleManagerDlg)
        self.lblCount.setGeometry(QtCore.QRect(54,400,64,22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.lblCount.setFont(font)
        self.lblCount.setObjectName("lblCount")

        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Kernel Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLoaded.setText(QtGui.QApplication.translate("moduleManagerDlg", "List only loaded modules", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", "Ara: ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("moduleManagerDlg", "Count: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCount.setText(QtGui.QApplication.translate("moduleManagerDlg", "0", None, QtGui.QApplication.UnicodeUTF8))

