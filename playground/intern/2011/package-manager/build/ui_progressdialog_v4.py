# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/progressdialog_v4.ui'
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

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName(_fromUtf8("ProgressDialog"))
        ProgressDialog.resize(550, 100)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProgressDialog.sizePolicy().hasHeightForWidth())
        ProgressDialog.setSizePolicy(sizePolicy)
        ProgressDialog.setStyleSheet(_fromUtf8("QTextEdit, QTextBrowser {\n"
"background:rgba(0,0,0,0);\n"
"}"))
        self.mainLayout = QtGui.QVBoxLayout(ProgressDialog)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(0)
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.widget = QtGui.QWidget(ProgressDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.operationInfo = QtGui.QTextBrowser(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.operationInfo.sizePolicy().hasHeightForWidth())
        self.operationInfo.setSizePolicy(sizePolicy)
        self.operationInfo.setMinimumSize(QtCore.QSize(0, 24))
        self.operationInfo.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.operationInfo.setFont(font)
        self.operationInfo.setFrameShape(QtGui.QFrame.NoFrame)
        self.operationInfo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.operationInfo.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.operationInfo.setHtml(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
"<table border=\"0\" style=\"-qt-table-type: root; margin-top:4px; margin-bottom:4px; margin-left:4px; margin-right:4px;\">\n"
"<tr>\n"
"<td style=\"border: none;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Droid Sans\'; font-size:9pt; font-weight:400;\"></p></td></tr></table></body></html>"))
        self.operationInfo.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.operationInfo.setObjectName(_fromUtf8("operationInfo"))
        self.verticalLayout.addWidget(self.operationInfo)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.actionLabel = QtGui.QTextBrowser(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.actionLabel.sizePolicy().hasHeightForWidth())
        self.actionLabel.setSizePolicy(sizePolicy)
        self.actionLabel.setMinimumSize(QtCore.QSize(0, 17))
        self.actionLabel.setMaximumSize(QtCore.QSize(16777215, 17))
        self.actionLabel.setFrameShape(QtGui.QFrame.NoFrame)
        self.actionLabel.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.actionLabel.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.actionLabel.setHtml(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\"-qt-table-type: root; margin-top:4px; margin-bottom:4px; margin-left:4px; margin-right:4px;\">\n"
"<tr>\n"
"<td style=\"border: none;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Droid Sans\';\"></p></td></tr></table></body></html>"))
        self.actionLabel.setObjectName(_fromUtf8("actionLabel"))
        self.horizontalLayout_2.addWidget(self.actionLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.percentage = QtGui.QTextEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.percentage.sizePolicy().hasHeightForWidth())
        self.percentage.setSizePolicy(sizePolicy)
        self.percentage.setMinimumSize(QtCore.QSize(140, 44))
        self.percentage.setMaximumSize(QtCore.QSize(140, 44))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setWeight(75)
        font.setBold(True)
        self.percentage.setFont(font)
        self.percentage.setStyleSheet(_fromUtf8(""))
        self.percentage.setFrameShape(QtGui.QFrame.NoFrame)
        self.percentage.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.percentage.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.percentage.setUndoRedoEnabled(False)
        self.percentage.setHtml(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:22pt; font-weight:600; font-style:normal;\">\n"
"<table border=\"0\" style=\"-qt-table-type: root; margin-top:4px; margin-bottom:4px; margin-left:4px; margin-right:4px;\">\n"
"<tr>\n"
"<td style=\"border: none;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Droid Sans\';\"></p></td></tr></table></body></html>"))
        self.percentage.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.percentage.setObjectName(_fromUtf8("percentage"))
        self.gridLayout.addWidget(self.percentage, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(self.widget)
        self.progressBar.setMinimumSize(QtCore.QSize(220, 15))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 15))
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.cancelButton = QtGui.QPushButton(self.widget)
        self.cancelButton.setMaximumSize(QtCore.QSize(25, 16777215))
        self.cancelButton.setText(_fromUtf8(""))
        self.cancelButton.setFlat(True)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout.addWidget(self.cancelButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        spacerItem = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 2, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.completedInfo = QtGui.QTextEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.completedInfo.sizePolicy().hasHeightForWidth())
        self.completedInfo.setSizePolicy(sizePolicy)
        self.completedInfo.setMaximumSize(QtCore.QSize(340, 20))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.completedInfo.setFont(font)
        self.completedInfo.setStyleSheet(_fromUtf8(""))
        self.completedInfo.setFrameShape(QtGui.QFrame.NoFrame)
        self.completedInfo.setFrameShadow(QtGui.QFrame.Plain)
        self.completedInfo.setLineWidth(0)
        self.completedInfo.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.completedInfo.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.completedInfo.setReadOnly(True)
        self.completedInfo.setHtml(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:600; font-style:normal;\">\n"
"<table border=\"0\" style=\"-qt-table-type: root; margin-top:4px; margin-bottom:4px; margin-left:4px; margin-right:4px;\">\n"
"<tr>\n"
"<td style=\"border: none;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Droid Sans\';\"></p></td></tr></table></body></html>"))
        self.completedInfo.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.completedInfo.setObjectName(_fromUtf8("completedInfo"))
        self.horizontalLayout_3.addWidget(self.completedInfo)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.timeRemaining = QtGui.QTextEdit(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.timeRemaining.sizePolicy().hasHeightForWidth())
        self.timeRemaining.setSizePolicy(sizePolicy)
        self.timeRemaining.setMaximumSize(QtCore.QSize(80, 20))
        self.timeRemaining.setStyleSheet(_fromUtf8(""))
        self.timeRemaining.setFrameShape(QtGui.QFrame.NoFrame)
        self.timeRemaining.setLineWidth(0)
        self.timeRemaining.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.timeRemaining.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.timeRemaining.setUndoRedoEnabled(False)
        self.timeRemaining.setHtml(_fromUtf8("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<table border=\"0\" style=\"-qt-table-type: root; margin-top:4px; margin-bottom:4px; margin-left:4px; margin-right:4px;\">\n"
"<tr>\n"
"<td style=\"border: none;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Droid Sans\';\"></p></td></tr></table></body></html>"))
        self.timeRemaining.setAcceptRichText(False)
        self.timeRemaining.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.timeRemaining.setObjectName(_fromUtf8("timeRemaining"))
        self.horizontalLayout_3.addWidget(self.timeRemaining)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 2)
        self.mainLayout.addWidget(self.widget)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        ProgressDialog.setWindowTitle(i18n("Form"))
        self.cancelButton.setShortcut(i18n("Alt+C"))

