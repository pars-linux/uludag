# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/message.ui'
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

class Ui_MessageBox(object):
    def setupUi(self, MessageBox):
        MessageBox.setObjectName(_fromUtf8("MessageBox"))
        MessageBox.resize(603, 61)
        self.mainLayout = QtGui.QHBoxLayout(MessageBox)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mainLayout.addItem(spacerItem)
        self.icon = QtGui.QLabel(MessageBox)
        self.icon.setMinimumSize(QtCore.QSize(32, 32))
        self.icon.setMaximumSize(QtCore.QSize(32, 32))
        self.icon.setText(_fromUtf8(""))
        self.icon.setScaledContents(True)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.mainLayout.addWidget(self.icon)
        self.label = QtGui.QLabel(MessageBox)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.mainLayout.addWidget(self.label)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.mainLayout.addItem(spacerItem1)

        self.retranslateUi(MessageBox)
        QtCore.QMetaObject.connectSlotsByName(MessageBox)

    def retranslateUi(self, MessageBox):
        MessageBox.setWindowTitle(i18n("Form"))

