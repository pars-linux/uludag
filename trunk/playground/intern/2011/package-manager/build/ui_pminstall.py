# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/pminstall.ui'
#
# Created: Mon Jul  4 14:25:14 2011
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

class Ui_PmWindow(object):
    def setupUi(self, PmWindow):
        PmWindow.setObjectName(_fromUtf8("PmWindow"))
        PmWindow.resize(580, 230)
        PmWindow.setMinimumSize(QtCore.QSize(550, 170))
        self.gridLayout = QtGui.QGridLayout(PmWindow)
        self.gridLayout.setContentsMargins(4, 8, 4, 1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(PmWindow)
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
        self.gridLayout.addWidget(self.label_2, 0, 0, 2, 1)
        self.label = QtGui.QLabel(PmWindow)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 2, 1)
        self.packageList = PackageView(PmWindow)
        self.packageList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.packageList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.packageList.setProperty(_fromUtf8("showDropIndicator"), False)
        self.packageList.setDragDropOverwriteMode(False)
        self.packageList.setAlternatingRowColors(True)
        self.packageList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.packageList.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.packageList.setShowGrid(False)
        self.packageList.setWordWrap(True)
        self.packageList.setCornerButtonEnabled(False)
        self.packageList.setObjectName(_fromUtf8("packageList"))
        self.packageList.horizontalHeader().setVisible(False)
        self.packageList.horizontalHeader().setStretchLastSection(True)
        self.packageList.verticalHeader().setVisible(False)
        self.packageList.verticalHeader().setDefaultSectionSize(52)
        self.packageList.verticalHeader().setMinimumSectionSize(52)
        self.gridLayout.addWidget(self.packageList, 2, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_size = QtGui.QLabel(PmWindow)
        self.label_size.setText(_fromUtf8(""))
        self.label_size.setObjectName(_fromUtf8("label_size"))
        self.horizontalLayout.addWidget(self.label_size)
        spacerItem = QtGui.QSpacerItem(152, 21, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_install = QtGui.QPushButton(PmWindow)
        self.button_install.setObjectName(_fromUtf8("button_install"))
        self.horizontalLayout.addWidget(self.button_install)
        self.button_cancel = QtGui.QPushButton(PmWindow)
        self.button_cancel.setShortcut(_fromUtf8("Esc"))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.horizontalLayout.addWidget(self.button_cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)

        self.retranslateUi(PmWindow)
        QtCore.QMetaObject.connectSlotsByName(PmWindow)

    def retranslateUi(self, PmWindow):
        PmWindow.setWindowTitle(i18n("Package Manager Quick Install"))
        self.label.setText(i18n("Following packages are selected to install. Do you want to install these packages ?"))
        self.packageList.setWhatsThis(i18n("Package List"))
        self.button_install.setText(i18n("Install"))
        self.button_cancel.setText(i18n("Cancel"))

from packageview import PackageView
import data_rc
