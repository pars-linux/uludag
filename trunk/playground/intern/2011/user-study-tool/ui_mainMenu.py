# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainMenu.ui'
#
# Created: Mon Aug 22 14:32:40 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_mainManager(object):
    def setupUi(self, mainManager):
        mainManager.setObjectName(_fromUtf8("mainManager"))
        mainManager.resize(480, 379)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/user_study.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainManager.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(mainManager)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.alwaysHelp = QtGui.QRadioButton(mainManager)
        self.alwaysHelp.setChecked(True)
        self.alwaysHelp.setObjectName(_fromUtf8("alwaysHelp"))
        self.gridLayout.addWidget(self.alwaysHelp, 0, 1, 1, 1)
        self.welcomeUser = QtGui.QLabel(mainManager)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.welcomeUser.sizePolicy().hasHeightForWidth())
        self.welcomeUser.setSizePolicy(sizePolicy)
        self.welcomeUser.setObjectName(_fromUtf8("welcomeUser"))
        self.gridLayout.addWidget(self.welcomeUser, 1, 0, 1, 1)
        self.askToHelp = QtGui.QRadioButton(mainManager)
        self.askToHelp.setObjectName(_fromUtf8("askToHelp"))
        self.gridLayout.addWidget(self.askToHelp, 1, 1, 1, 1)
        self.rejectHelp = QtGui.QRadioButton(mainManager)
        self.rejectHelp.setObjectName(_fromUtf8("rejectHelp"))
        self.gridLayout.addWidget(self.rejectHelp, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.surveyList = QtGui.QListWidget(mainManager)
        self.surveyList.setEnabled(True)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.surveyList.setFont(font)
        self.surveyList.setStyleSheet(_fromUtf8(""))
        self.surveyList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.surveyList.setAlternatingRowColors(True)
        self.surveyList.setIconSize(QtCore.QSize(32, 32))
        self.surveyList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerItem)
        self.surveyList.setObjectName(_fromUtf8("surveyList"))
        self.gridLayout_2.addWidget(self.surveyList, 1, 0, 1, 1)

        self.retranslateUi(mainManager)
        QtCore.QMetaObject.connectSlotsByName(mainManager)

    def retranslateUi(self, mainManager):
        mainManager.setWindowTitle(QtGui.QApplication.translate("mainManager", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.alwaysHelp.setText(QtGui.QApplication.translate("mainManager", "Her zaman katıl", None, QtGui.QApplication.UnicodeUTF8))
        self.welcomeUser.setText(QtGui.QApplication.translate("mainManager", "Bu uygulama....", None, QtGui.QApplication.UnicodeUTF8))
        self.askToHelp.setText(QtGui.QApplication.translate("mainManager", "Katılmadan sor", None, QtGui.QApplication.UnicodeUTF8))
        self.rejectHelp.setText(QtGui.QApplication.translate("mainManager", "Hiçbir zaman katılma", None, QtGui.QApplication.UnicodeUTF8))

import data_rc
