
#!/usr/bin/env python
# Generated by pykdeuic4 from uimain.ui on Wed Feb 25 14:51:45 2009
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

class Ui_MainManager(object):
    def setupUi(self, MainManager):
        MainManager.setObjectName("MainManager")
        MainManager.resize(712, 439)
        self.gridLayout = QtGui.QGridLayout(MainManager)
        self.gridLayout.setObjectName("gridLayout")
        self.componentList = QtGui.QListWidget(MainManager)
        self.componentList.setMinimumSize(QtCore.QSize(250, 0))
        self.componentList.setMaximumSize(QtCore.QSize(250, 16777215))
        self.componentList.setObjectName("componentList")
        self.gridLayout.addWidget(self.componentList, 0, 0, 2, 1)
        self.searchLine = kdeui.KLineEdit(MainManager)
        self.searchLine.setProperty("showClearButton", QtCore.QVariant(True))
        self.searchLine.setObjectName("searchLine")
        self.gridLayout.addWidget(self.searchLine, 0, 1, 1, 1)
        self.actionButton = QtGui.QPushButton(MainManager)
        self.actionButton.setObjectName("actionButton")
        self.gridLayout.addWidget(self.actionButton, 0, 2, 1, 1)
        self.packageList = QtGui.QListWidget(MainManager)
        self.packageList.setMinimumSize(QtCore.QSize(450, 0))
        self.packageList.setObjectName("packageList")
        self.gridLayout.addWidget(self.packageList, 1, 1, 1, 2)

        self.retranslateUi(MainManager)
        QtCore.QMetaObject.connectSlotsByName(MainManager)

    def retranslateUi(self, MainManager):
        MainManager.setWindowTitle(kdecore.i18n("Form"))
        self.searchLine.setClickMessage(kdecore.i18n("Click to search"))


