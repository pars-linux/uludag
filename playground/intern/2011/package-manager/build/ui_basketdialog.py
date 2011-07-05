# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/basketdialog.ui'
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

class Ui_BasketDialog(object):
    def setupUi(self, BasketDialog):
        BasketDialog.setObjectName(_fromUtf8("BasketDialog"))
        BasketDialog.resize(630, 483)
        BasketDialog.setStyleSheet(_fromUtf8("#Basket {\n"
"background-color: rgb(164, 164, 164);\n"
"border:0px solid white ;\n"
"border-radius:4px;\n"
"}\n"
""))
        self.gridLayout_2 = QtGui.QGridLayout(BasketDialog)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.Basket = QtGui.QWidget(BasketDialog)
        self.Basket.setStyleSheet(_fromUtf8("#packageList, #extraList {\n"
"    border:1px solid #888;\n"
"    border-radius:3px;\n"
"    background-color:rgba(252,252,252,100);\n"
"    color:rgba(20,20,20);\n"
"}\n"
"QLabel { color:rgb(20,20,20); }"))
        self.Basket.setObjectName(_fromUtf8("Basket"))
        self.gridLayout_3 = QtGui.QGridLayout(self.Basket)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setVerticalSpacing(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.widget = QtGui.QWidget(self.Basket)
        self.widget.setMinimumSize(QtCore.QSize(0, 26))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 26))
        self.widget.setStyleSheet(_fromUtf8("QWidget#widget{\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"\n"
"border:0px solid #666;\n"
"border-top-left-radius:4px;\n"
"border-top-right-radius:4px;\n"
"border-bottom:1px solid #999;\n"
"}\n"
""))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(4, 0, 3, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.infoLabel = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.infoLabel.setFont(font)
        self.infoLabel.setIndent(3)
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.horizontalLayout.addWidget(self.infoLabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setStyleSheet(_fromUtf8("color:rgb(20,20,20);"))
        self.cancelButton.setText(_fromUtf8(""))
        self.cancelButton.setFlat(True)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)
        self.widget_2 = QtGui.QWidget(self.Basket)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout = QtGui.QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.packageList = PackageView(self.widget_2)
        self.packageList.setMinimumSize(QtCore.QSize(400, 0))
        self.packageList.setStyleSheet(_fromUtf8(""))
        self.packageList.setFrameShadow(QtGui.QFrame.Plain)
        self.packageList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.packageList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.packageList.setProperty(_fromUtf8("showDropIndicator"), False)
        self.packageList.setDragDropOverwriteMode(False)
        self.packageList.setAlternatingRowColors(False)
        self.packageList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.packageList.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.packageList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.packageList.setShowGrid(False)
        self.packageList.setWordWrap(True)
        self.packageList.setCornerButtonEnabled(False)
        self.packageList.setObjectName(_fromUtf8("packageList"))
        self.packageList.horizontalHeader().setVisible(False)
        self.packageList.horizontalHeader().setStretchLastSection(True)
        self.packageList.verticalHeader().setVisible(False)
        self.packageList.verticalHeader().setDefaultSectionSize(52)
        self.packageList.verticalHeader().setMinimumSectionSize(52)
        self.gridLayout.addWidget(self.packageList, 0, 0, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 3)
        self.extrasLabel = QtGui.QLabel(self.widget_2)
        self.extrasLabel.setIndent(3)
        self.extrasLabel.setObjectName(_fromUtf8("extrasLabel"))
        self.gridLayout.addWidget(self.extrasLabel, 2, 0, 1, 3)
        self.extraList = PackageView(self.widget_2)
        self.extraList.setMinimumSize(QtCore.QSize(400, 0))
        self.extraList.setStyleSheet(_fromUtf8(""))
        self.extraList.setFrameShadow(QtGui.QFrame.Plain)
        self.extraList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.extraList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.extraList.setProperty(_fromUtf8("showDropIndicator"), False)
        self.extraList.setDragDropOverwriteMode(False)
        self.extraList.setAlternatingRowColors(False)
        self.extraList.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.extraList.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.extraList.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.extraList.setShowGrid(False)
        self.extraList.setWordWrap(True)
        self.extraList.setCornerButtonEnabled(False)
        self.extraList.setObjectName(_fromUtf8("extraList"))
        self.extraList.horizontalHeader().setVisible(False)
        self.extraList.horizontalHeader().setStretchLastSection(True)
        self.extraList.verticalHeader().setVisible(False)
        self.extraList.verticalHeader().setDefaultSectionSize(52)
        self.extraList.verticalHeader().setMinimumSectionSize(52)
        self.gridLayout.addWidget(self.extraList, 3, 0, 1, 3)
        spacerItem2 = QtGui.QSpacerItem(20, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 3)
        self.label_3 = QtGui.QLabel(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setIndent(3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.totalSize = QtGui.QLabel(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.totalSize.sizePolicy().hasHeightForWidth())
        self.totalSize.setSizePolicy(sizePolicy)
        self.totalSize.setObjectName(_fromUtf8("totalSize"))
        self.gridLayout.addWidget(self.totalSize, 5, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.clearButton = QtGui.QPushButton(self.widget_2)
        self.clearButton.setStyleSheet(_fromUtf8(""))
        self.clearButton.setAutoDefault(False)
        self.clearButton.setFlat(False)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_2.addWidget(self.clearButton)
        self.actionButton = QtGui.QPushButton(self.widget_2)
        self.actionButton.setStyleSheet(_fromUtf8(""))
        self.actionButton.setDefault(True)
        self.actionButton.setObjectName(_fromUtf8("actionButton"))
        self.horizontalLayout_2.addWidget(self.actionButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 2, 2, 1)
        self.downloadSizeLabel = QtGui.QLabel(self.widget_2)
        self.downloadSizeLabel.setIndent(3)
        self.downloadSizeLabel.setObjectName(_fromUtf8("downloadSizeLabel"))
        self.gridLayout.addWidget(self.downloadSizeLabel, 6, 0, 1, 1)
        self.downloadSize = QtGui.QLabel(self.widget_2)
        self.downloadSize.setObjectName(_fromUtf8("downloadSize"))
        self.gridLayout.addWidget(self.downloadSize, 6, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 3, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem3, 7, 1, 1, 1)
        self.gridLayout.setColumnMinimumWidth(1, 1)
        self.gridLayout.setColumnMinimumWidth(2, 2)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 2)
        self.gridLayout_3.addWidget(self.widget_2, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.Basket, 0, 0, 1, 1)

        self.retranslateUi(BasketDialog)
        QtCore.QMetaObject.connectSlotsByName(BasketDialog)
        BasketDialog.setTabOrder(self.packageList, self.extraList)

    def retranslateUi(self, BasketDialog):
        BasketDialog.setWindowTitle(i18n("Basket"))
        self.infoLabel.setText(i18n("Selected package(s) for install:"))
        self.extrasLabel.setText(i18n("Extra dependencies of the selected package(s) that are also going to be installed:"))
        self.label_3.setText(i18n("Total Size:"))
        self.totalSize.setText(i18n("<b>2.2 MB</b>"))
        self.clearButton.setText(i18n("Clear Basket"))
        self.actionButton.setText(i18n("Install Package(s)"))
        self.downloadSizeLabel.setText(i18n("Download Size:"))
        self.downloadSize.setText(i18n("<b>2.0 MB</"))

from packageview import PackageView
