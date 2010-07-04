# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgetInstalling.ui'
#
# Created: Sun Jul 04 17:43:54 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_widgetInstalling(object):
    def setupUi(self, widgetInstalling):
        widgetInstalling.setObjectName("widgetInstalling")
        widgetInstalling.resize(421, 234)
        widgetInstalling.setWindowTitle("")
        self.label = QtGui.QLabel(widgetInstalling)
        self.label.setGeometry(QtCore.QRect(10, 10, 401, 21))
        self.label.setObjectName("label")
        self.progressBar = QtGui.QProgressBar(widgetInstalling)
        self.progressBar.setGeometry(QtCore.QRect(10, 40, 401, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.formLayoutWidget = QtGui.QWidget(widgetInstalling)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 70, 401, 51))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.lblInstalling = QtGui.QLabel(self.formLayoutWidget)
        self.lblInstalling.setObjectName("lblInstalling")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.lblInstalling)
        self.lblVersion = QtGui.QLabel(self.formLayoutWidget)
        self.lblVersion.setObjectName("lblVersion")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.lblVersion)
        self.lblInfo = QtGui.QLabel(self.formLayoutWidget)
        self.lblInfo.setObjectName("lblInfo")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.lblInfo)
        self.lblStatus = QtGui.QLabel(self.formLayoutWidget)
        self.lblStatus.setObjectName("lblStatus")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.lblStatus)
        self.textEdit = QtGui.QTextEdit(widgetInstalling)
        self.textEdit.setGeometry(QtCore.QRect(10, 130, 401, 101))
        self.textEdit.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>")
        self.textEdit.setTabStopWidth(82)
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi(widgetInstalling)
        QtCore.QMetaObject.connectSlotsByName(widgetInstalling)

    def retranslateUi(self, widgetInstalling):
        self.label.setText(QtGui.QApplication.translate("widgetInstalling", "Please wait while PaW completes your Pardus installation.", None, QtGui.QApplication.UnicodeUTF8))
        self.lblInstalling.setText(QtGui.QApplication.translate("widgetInstalling", "Installing: ", None, QtGui.QApplication.UnicodeUTF8))
        self.lblVersion.setText(QtGui.QApplication.translate("widgetInstalling", "Pardus 2009.2 Geronticus eremita", None, QtGui.QApplication.UnicodeUTF8))
        self.lblInfo.setText(QtGui.QApplication.translate("widgetInstalling", "Status:", None, QtGui.QApplication.UnicodeUTF8))
        self.lblStatus.setText(QtGui.QApplication.translate("widgetInstalling", "Preparing installation...", None, QtGui.QApplication.UnicodeUTF8))

