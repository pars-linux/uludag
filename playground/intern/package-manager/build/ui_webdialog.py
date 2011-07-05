# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/webdialog.ui'
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

class Ui_WebDialog(object):
    def setupUi(self, WebDialog):
        WebDialog.setObjectName(_fromUtf8("WebDialog"))
        WebDialog.resize(700, 460)
        WebDialog.setStyleSheet(_fromUtf8("#Basket {\n"
"background-color: rgb(164, 164, 164);\n"
"border:1px solid #AAA;\n"
"border-radius:4px;\n"
"\n"
"}"))
        self.gridLayout_3 = QtGui.QGridLayout(WebDialog)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.Basket = QtGui.QWidget(WebDialog)
        self.Basket.setStyleSheet(_fromUtf8("QLabel { color:rgb(20,20,20); }"))
        self.Basket.setObjectName(_fromUtf8("Basket"))
        self.gridLayout_4 = QtGui.QGridLayout(self.Basket)
        self.gridLayout_4.setMargin(0)
        self.gridLayout_4.setVerticalSpacing(0)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.widget_2 = QtGui.QWidget(self.Basket)
        self.widget_2.setAutoFillBackground(False)
        self.widget_2.setStyleSheet(_fromUtf8(""))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.gridLayout = QtGui.QGridLayout(self.widget_2)
        self.gridLayout.setMargin(1)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(self.widget_2)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setTabPosition(QtGui.QTabWidget.North)
        self.tabWidget.setDocumentMode(True)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.packageFiles = QtGui.QWidget()
        self.packageFiles.setAutoFillBackground(False)
        self.packageFiles.setObjectName(_fromUtf8("packageFiles"))
        self.gridLayout_5 = QtGui.QGridLayout(self.packageFiles)
        self.gridLayout_5.setMargin(8)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.filesList = QtGui.QListWidget(self.packageFiles)
        self.filesList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.filesList.setObjectName(_fromUtf8("filesList"))
        self.gridLayout_5.addWidget(self.filesList, 0, 0, 1, 2)
        self.tabWidget.addTab(self.packageFiles, _fromUtf8(""))
        self.packageDetails = QtGui.QWidget()
        self.packageDetails.setAutoFillBackground(False)
        self.packageDetails.setStyleSheet(_fromUtf8("QWidget#webWidget {\n"
"    border:0px solid #555;\n"
"    border-radius:6px;\n"
"\n"
"    background-color:rgba(122,122,122);\n"
"    color:rgba(20,20,20);\n"
"\n"
"}"))
        self.packageDetails.setObjectName(_fromUtf8("packageDetails"))
        self.webLayout = QtGui.QGridLayout(self.packageDetails)
        self.webLayout.setContentsMargins(4, -1, 4, 4)
        self.webLayout.setObjectName(_fromUtf8("webLayout"))
        self.noconnection = QtGui.QLabel(self.packageDetails)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.noconnection.setFont(font)
        self.noconnection.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.noconnection.setStyleSheet(_fromUtf8(""))
        self.noconnection.setAlignment(QtCore.Qt.AlignCenter)
        self.noconnection.setObjectName(_fromUtf8("noconnection"))
        self.webLayout.addWidget(self.noconnection, 0, 0, 1, 1)
        self.webWidget = QtGui.QWidget(self.packageDetails)
        self.webWidget.setStyleSheet(_fromUtf8(""))
        self.webWidget.setObjectName(_fromUtf8("webWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.webWidget)
        self.gridLayout_2.setMargin(4)
        self.gridLayout_2.setHorizontalSpacing(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.webView = QtWebKit.QWebView(self.webWidget)
        self.webView.setStyleSheet(_fromUtf8("background-color:rgba(0,0,0,0);"))
        self.webView.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.webView.setObjectName(_fromUtf8("webView"))
        self.gridLayout_2.addWidget(self.webView, 0, 0, 1, 1)
        self.webLayout.addWidget(self.webWidget, 1, 0, 1, 1)
        self.tabWidget.addTab(self.packageDetails, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        self.widget = QtGui.QWidget(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMaximumSize(QtCore.QSize(16777215, 26))
        self.widget.setStyleSheet(_fromUtf8("QWidget#widget{\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,\n"
"                                 stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);\n"
"\n"
"border-bottom:1px solid #CCC;\n"
"}\n"
""))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.packageName = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.packageName.setFont(font)
        self.packageName.setIndent(3)
        self.packageName.setObjectName(_fromUtf8("packageName"))
        self.horizontalLayout.addWidget(self.packageName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setMinimumSize(QtCore.QSize(32, 26))
        self.cancelButton.setMaximumSize(QtCore.QSize(24, 26))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setWeight(75)
        font.setBold(True)
        self.cancelButton.setFont(font)
        self.cancelButton.setStyleSheet(_fromUtf8("color:rgb(20,20,20);\n"
""))
        self.cancelButton.setText(_fromUtf8(""))
        self.cancelButton.setFlat(True)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.widget_2, 1, 0, 1, 1)
        self.gridLayout_3.addWidget(self.Basket, 0, 0, 1, 1)

        self.retranslateUi(WebDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(WebDialog)

    def retranslateUi(self, WebDialog):
        WebDialog.setWindowTitle(i18n("Basket"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.packageFiles), i18n("Package Files"))
        self.noconnection.setText(i18n("AppInfo Server is not reachable\n"
"Please check your network connection"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.packageDetails), i18n("Package Details"))
        self.packageName.setText(i18n("Package Details"))

from PyQt4 import QtWebKit
