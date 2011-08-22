# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_detailWidget.ui'
#
# Created: Mon Aug 22 08:23:30 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_InfoWidget(object):
    def setupUi(self, InfoWidget):
        InfoWidget.setObjectName(_fromUtf8("InfoWidget"))
        InfoWidget.resize(422, 308)
        InfoWidget.setMinimumSize(QtCore.QSize(0, 48))
        self.gridLayout = QtGui.QGridLayout(InfoWidget)
        self.gridLayout.setContentsMargins(8, -1, 8, -1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.webView = QtWebKit.QWebView(InfoWidget)
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout.addWidget(self.webView, 0, 0, 1, 1)

        self.retranslateUi(InfoWidget)
        QtCore.QMetaObject.connectSlotsByName(InfoWidget)

    def retranslateUi(self, InfoWidget):
        InfoWidget.setWindowTitle(QtGui.QApplication.translate("InfoWidget", "Form", None, QtGui.QApplication.UnicodeUTF8))

from PyQt4 import QtWebKit
