# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/preview.ui'
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

class Ui_Preview(object):
    def setupUi(self, Preview):
        Preview.setObjectName(_fromUtf8("Preview"))
        Preview.resize(802, 628)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Preview.sizePolicy().hasHeightForWidth())
        Preview.setSizePolicy(sizePolicy)
        Preview.setStyleSheet(_fromUtf8("QWebView { background-color:rgba(0,0,0,0); }"))
        self.gridLayout_2 = QtGui.QGridLayout(Preview)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        spacerItem = QtGui.QSpacerItem(767, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 0, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(Preview)
        self.cancelButton.setMaximumSize(QtCore.QSize(32, 16777215))
        self.cancelButton.setText(_fromUtf8(""))
        self.cancelButton.setAutoDefault(True)
        self.cancelButton.setFlat(True)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.gridLayout_2.addWidget(self.cancelButton, 0, 1, 1, 1)
        self.webLayout = QtGui.QGridLayout()
        self.webLayout.setObjectName(_fromUtf8("webLayout"))
        self.webView = QtWebKit.QWebView(Preview)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.webLayout.addWidget(self.webView, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.webLayout, 1, 0, 1, 2)
        self.gridLayout_2.setRowStretch(1, 3)

        self.retranslateUi(Preview)
        QtCore.QMetaObject.connectSlotsByName(Preview)

    def retranslateUi(self, Preview):
        Preview.setWindowTitle(i18n("Preview"))

from PyQt4 import QtWebKit
