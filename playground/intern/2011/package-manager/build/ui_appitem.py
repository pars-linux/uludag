# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/appitem.ui'
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

class Ui_ApplicationItem(object):
    def setupUi(self, ApplicationItem):
        ApplicationItem.setObjectName(_fromUtf8("ApplicationItem"))
        ApplicationItem.resize(369, 51)
        ApplicationItem.setMinimumSize(QtCore.QSize(0, 50))
        ApplicationItem.setMaximumSize(QtCore.QSize(16777215, 51))
        self.gridLayout_2 = QtGui.QGridLayout(ApplicationItem)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.appIcon = QtGui.QLabel(ApplicationItem)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.appIcon.sizePolicy().hasHeightForWidth())
        self.appIcon.setSizePolicy(sizePolicy)
        self.appIcon.setMinimumSize(QtCore.QSize(36, 32))
        self.appIcon.setMaximumSize(QtCore.QSize(36, 32))
        self.appIcon.setText(_fromUtf8(""))
        self.appIcon.setPixmap(QtGui.QPixmap(_fromUtf8(":/data/package.png")))
        self.appIcon.setObjectName(_fromUtf8("appIcon"))
        self.gridLayout_2.addWidget(self.appIcon, 0, 0, 2, 1)
        self.appGenericName = QtGui.QLabel(ApplicationItem)
        self.appGenericName.setObjectName(_fromUtf8("appGenericName"))
        self.gridLayout_2.addWidget(self.appGenericName, 0, 1, 1, 1)
        self.widget = QtGui.QWidget(ApplicationItem)
        self.widget.setMinimumSize(QtCore.QSize(0, 18))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.appName = QtGui.QLabel(self.widget)
        self.appName.setStyleSheet(_fromUtf8("color:gray"))
        self.appName.setWordWrap(True)
        self.appName.setObjectName(_fromUtf8("appName"))
        self.gridLayout.addWidget(self.appName, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.widget, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 2)

        self.retranslateUi(ApplicationItem)
        QtCore.QMetaObject.connectSlotsByName(ApplicationItem)

    def retranslateUi(self, ApplicationItem):
        ApplicationItem.setWindowTitle(i18n("Application"))
        self.appGenericName.setText(i18n("Web Tarayıcı"))
        self.appName.setText(i18n("Firefox"))

import data_rc
