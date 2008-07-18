# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/uis/ui_availablemodules.ui'
#
# Created: Fri Jul 18 15:40:54 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_availableModulesDlg(object):
    def setupUi(self, availableModulesDlg):
        availableModulesDlg.setObjectName("availableModulesDlg")
        availableModulesDlg.setWindowModality(QtCore.Qt.NonModal)
        availableModulesDlg.resize(291,450)

        font = QtGui.QFont()
        font.setPointSize(8)


        self.cmbListType = QtGui.QComboBox(availableModulesDlg)
        self.cmbListType.setObjectName("cmbListType")
        self.cmbListType.setGeometry(QtCore.QRect(14,10,261,23))
        self.cmbListType.setFont(font)
        self.cmbListType.addItem("Select listing filter")
        self.cmbListType.addItem("All available")
        self.cmbListType.addItem("Blacklisted")
        self.cmbListType.addItem("Autoloading")

        self.lblListType = QtGui.QLabel(availableModulesDlg)
        self.lblListType.setObjectName("lblListType")
        self.lblListType.setFont(font)
        self.lblListType.setText("Listing all available modules")
        self.lblListType.setGeometry(QtCore.QRect(14,37,261,16))
        
        
        self.listAllModules = QtGui.QListWidget(availableModulesDlg)
        self.listAllModules.setGeometry(QtCore.QRect(14,55,261,375))
        self.listAllModules.setFont(font)
        self.listAllModules.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listAllModules.setObjectName("listAllModules")

        loadAction = QtGui.QAction(QtGui.QIcon(":/load.png"),"&Load", self)
        self.listAllModules.addAction(loadAction)
        loadAction.setFont(font)

        blacklistAction = QtGui.QAction(QtGui.QIcon(":/blacklist.png"),"&Blacklist", self)
        self.listAllModules.addAction(blacklistAction)
        blacklistAction.setFont(font)

        addAutoloadAction = QtGui.QAction(QtGui.QIcon(":/autoload.png"),"&Add to autoload", self)
        self.listAllModules.addAction(addAutoloadAction)
        addAutoloadAction.setFont(font)

        #removeAutoloadAction

        self.retranslateUi(availableModulesDlg)
        QtCore.QMetaObject.connectSlotsByName(availableModulesDlg)

    def retranslateUi(self, availableModulesDlg):
        availableModulesDlg.setWindowTitle(QtGui.QApplication.translate("availableModulesDlg", "Available Modules", None, QtGui.QApplication.UnicodeUTF8))

