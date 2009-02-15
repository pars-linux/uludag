# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/uis/ui_mainwindow.ui'
#
# Created: Fri Jul 18 15:40:54 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_moduleManagerDlg(object):
    def setupUi(self, moduleManagerDlg):
        moduleManagerDlg.setObjectName("moduleManagerDlg")
        moduleManagerDlg.resize(329,505)
        moduleManagerDlg.setWindowIcon(QtGui.QIcon(":/program-icon.png"))
        self.listModules = QtGui.QListWidget(moduleManagerDlg)
        self.listModules.setGeometry(QtCore.QRect(10,68,311,391))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setStrikeOut(False)
    
        self.listModules.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

        self.listModules.setFont(font)
        self.listModules.setAcceptDrops(False)
        self.listModules.setSortingEnabled(True)
        self.listModules.setObjectName("listModules")

        
        self.unloadAction = QtGui.QAction(QtGui.QIcon(":/remove.png"), "&Remove", self)
        self.listModules.addAction(self.unloadAction)
        self.unloadAction.setFont(font)

        self.addblacklistAction = QtGui.QAction(QtGui.QIcon(":/blacklist.png"),"&Add to blacklist", self)
        self.listModules.addAction(self.addblacklistAction)
        self.addblacklistAction.setFont(font)


        self.lblSearch = QtGui.QLabel(moduleManagerDlg)
        self.lblSearch.setGeometry(QtCore.QRect(9,9,45,28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblSearch.setFont(font)
        self.lblSearch.setWordWrap(True)
        self.lblSearch.setObjectName("lblSearch")
        self.editSearch = QtGui.QLineEdit(moduleManagerDlg)
        self.editSearch.setGeometry(QtCore.QRect(62,8,265,28))
        self.editSearch.setMaximumSize(QtCore.QSize(16777215,28))
        self.editSearch.setObjectName("editSearch")
        self.editSearch.setFocus()
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label = QtGui.QLabel(moduleManagerDlg)
        self.label.setGeometry(QtCore.QRect(10,44,171,22))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.btnNewModule = QtGui.QPushButton(moduleManagerDlg)
        self.btnNewModule.setGeometry(QtCore.QRect(10,466,120,32))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.btnNewModule.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/moduleedit.png"),QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.btnNewModule.setIcon(icon)
        self.btnNewModule.setIconSize(QtCore.QSize(24,24))
        self.btnNewModule.setObjectName("btnNewModule")
        self.btnNewModule.setGeometry(QtCore.QRect(10,466,150,32))
        self.lblSearch.setBuddy(self.editSearch)
        self.retranslateUi(moduleManagerDlg)
        QtCore.QMetaObject.connectSlotsByName(moduleManagerDlg)

    def retranslateUi(self, moduleManagerDlg):
        moduleManagerDlg.setWindowTitle(QtGui.QApplication.translate("moduleManagerDlg", "Kernel Module Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSearch.setText(QtGui.QApplication.translate("moduleManagerDlg", "Search", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("moduleManagerDlg", "Currently loaded modules", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNewModule.setText(QtGui.QApplication.translate("moduleManagerDlg", "Module Settings", None, QtGui.QApplication.UnicodeUTF8))

import resource_rc
