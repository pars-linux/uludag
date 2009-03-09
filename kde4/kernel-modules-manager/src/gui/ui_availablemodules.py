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
        availableModulesDlg.resize(291,489)
        availableModulesDlg.setWindowIcon(QtGui.QIcon("tt:/program-icon.png"))

        font = QtGui.QFont()
        font.setPointSize(10)


        self.cmbListType = QtGui.QComboBox(availableModulesDlg)
        self.cmbListType.setObjectName("cmbListType")
        self.cmbListType.setGeometry(QtCore.QRect(14,45,261,23))
        self.cmbListType.setFont(font)
        self.cmbListType.addItem("Select listing filter")
        self.cmbListType.addItem("All available")
        self.cmbListType.addItem("Blacklisted")
        self.cmbListType.addItem("Autoloading")
        
        self.lblSearch = QtGui.QLabel(availableModulesDlg)
        self.lblSearch.setFont(font)
        self.lblSearch.setScaledContents(True)
        self.lblSearch.setGeometry(QtCore.QRect(14,10,28,28))


        self.editSearch = QtGui.QLineEdit(availableModulesDlg)
        self.editSearch.setGeometry(QtCore.QRect(44,10,231,28))
        self.editSearch.setObjectName("editSearch")
        self.editSearch.setFocus()

        self.listAllModules = QtGui.QListWidget(availableModulesDlg)
        self.listAllModules.setGeometry(QtCore.QRect(14,79,261,400))
        self.listAllModules.setFont(font)
        self.listAllModules.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.listAllModules.setObjectName("listAllModules")

        self.loadAction = QtGui.QAction(QtGui.QIcon(":/load.png"),"&Load", self)
        self.listAllModules.addAction(self.loadAction)
        self.loadAction.setFont(font)

        self.addBlacklistAction = QtGui.QAction(QtGui.QIcon(":/blacklist.png"),"Add to &blacklist", self)
        self.listAllModules.addAction(self.addBlacklistAction)
        self.addBlacklistAction.setFont(font)

        self.removeBlacklistAction = QtGui.QAction(QtGui.QIcon(":/removeblacklist.png"),"Remove from blacklist", self)
        self.listAllModules.addAction(self.removeBlacklistAction)
        self.removeBlacklistAction.setFont(font)

        self.addAutoloadAction = QtGui.QAction(QtGui.QIcon(":/autoload.png"), "&Add to autoload", self)
        self.listAllModules.addAction(self.addAutoloadAction)
        self.addAutoloadAction.setFont(font)

        self.removeAutoloadAction = QtGui.QAction(QtGui.QIcon(":/removeautoload.png"), "&Remove from autoload", self)
        self.listAllModules.addAction(self.removeAutoloadAction)
        self.removeAutoloadAction.setFont(font)

        self.retranslateUi(availableModulesDlg)
        QtCore.QMetaObject.connectSlotsByName(availableModulesDlg)

    def retranslateUi(self, availableModulesDlg):
        availableModulesDlg.setWindowTitle(QtGui.QApplication.translate("availableModulesDlg", "Available Modules", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSearch.setText(QtGui.QApplication.translate("availableModulesDlg", "Ara:",None,QtGui.QApplication.UnicodeUTF8))

