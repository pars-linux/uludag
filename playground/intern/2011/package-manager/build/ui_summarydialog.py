# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/summarydialog.ui'
#
# Created: Mon Jul  4 14:25:13 2011
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

import gettext
__trans = gettext.translation('package-manager', fallback=True)
i18n = __trans.ugettext
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SummaryDialog(object):
    def setupUi(self, SummaryDialog):
        SummaryDialog.setObjectName(_fromUtf8("SummaryDialog"))
        SummaryDialog.resize(385, 391)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SummaryDialog.sizePolicy().hasHeightForWidth())
        SummaryDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(SummaryDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(SummaryDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(32, 32))
        self.label_2.setMaximumSize(QtCore.QSize(32, 32))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setPixmap(QtGui.QPixmap(_fromUtf8(":/data/package-manager.png")))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.startAppInfo = QtGui.QLabel(SummaryDialog)
        self.startAppInfo.setEnabled(True)
        font = QtGui.QFont()
        self.startAppInfo.setFont(font)
        self.startAppInfo.setTextFormat(QtCore.Qt.AutoText)
        self.startAppInfo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.startAppInfo.setWordWrap(True)
        self.startAppInfo.setObjectName(_fromUtf8("startAppInfo"))
        self.gridLayout.addWidget(self.startAppInfo, 0, 1, 1, 2)
        self.appList = QtGui.QListWidget(SummaryDialog)
        self.appList.setObjectName(_fromUtf8("appList"))
        self.gridLayout.addWidget(self.appList, 1, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(307, 23, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 2)
        self.closeButton = QtGui.QPushButton(SummaryDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.gridLayout.addWidget(self.closeButton, 2, 2, 1, 1)

        self.retranslateUi(SummaryDialog)
        QtCore.QMetaObject.connectSlotsByName(SummaryDialog)

    def retranslateUi(self, SummaryDialog):
        SummaryDialog.setWindowTitle(i18n("Operation Summary"))
        self.startAppInfo.setText(i18n("You can start the new installed application by double-clicking on the list below or later from the applications menu."))
        self.closeButton.setText(i18n("&Ok"))

import data_rc
