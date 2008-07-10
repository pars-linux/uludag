# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created: Thu Jul 10 16:37:01 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(316,456)
        self.splitter = QtGui.QSplitter(moduleManagerDlg)
        self.splitter.setGeometry(QtCore.QRect(10,20,291,431))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtGui.QWidget(self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listModules = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listModules.setObjectName("listModules")
        self.verticalLayout.addWidget(self.listModules)
        self.horizontalLayoutWidget = QtGui.QWidget(self.splitter)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnList = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.btnList.setObjectName("btnList")
        self.horizontalLayout.addWidget(self.btnList)
        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)

        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.btnList.setText(QtGui.QApplication.translate("moduleManagerDlg", "Listele", None, QtGui.QApplication.UnicodeUTF8))

