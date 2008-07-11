# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/ui_mainwindow.ui'
#
# Created: Fri Jul 11 09:36:40 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(311,443)
        self.layoutWidget = QtGui.QWidget(moduleManagerDlg)
        self.layoutWidget.setGeometry(QtCore.QRect(10,10,291,431))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblSearch = QtGui.QLabel(self.layoutWidget)
        self.lblSearch.setScaledContents(True)
        self.lblSearch.setWordWrap(True)
        self.lblSearch.setObjectName("lblSearch")
        self.horizontalLayout.addWidget(self.lblSearch)
        self.editSearch = QtGui.QLineEdit(self.layoutWidget)
        self.editSearch.setMaximumSize(QtCore.QSize(16777215,28))
        self.editSearch.setObjectName("editSearch")
        self.horizontalLayout.addWidget(self.editSearch)
        self.btnSearch = QtGui.QPushButton(self.layoutWidget)
        self.btnSearch.setMaximumSize(QtCore.QSize(30,28))
        self.btnSearch.setObjectName("btnSearch")
        self.horizontalLayout.addWidget(self.btnSearch)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.listModules = QtGui.QListWidget(self.layoutWidget)
        self.listModules.setObjectName("listModules")
        self.verticalLayout.addWidget(self.listModules)
        self.chkLoaded = QtGui.QCheckBox(self.layoutWidget)
        self.chkLoaded.setObjectName("chkLoaded")
        self.verticalLayout.addWidget(self.chkLoaded)

        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", "Ara  ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", ">>", None, QtGui.QApplication.UnicodeUTF8))
        self.chkLoaded.setText(QtGui.QApplication.translate("moduleManagerDlg", "Sadece yüklü olanları listele", None, QtGui.QApplication.UnicodeUTF8))

