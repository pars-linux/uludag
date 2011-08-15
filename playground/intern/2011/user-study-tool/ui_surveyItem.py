# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_surveyItem.ui'
#
# Created: Thu Aug 11 15:00:15 2011
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SurveyItemWidget(object):
    def setupUi(self, SurveyItemWidget):
        SurveyItemWidget.setObjectName(_fromUtf8("SurveyItemWidget"))
        SurveyItemWidget.resize(673, 43)
        self.gridLayout = QtGui.QGridLayout(SurveyItemWidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(SurveyItemWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet(_fromUtf8("\n"
"border-color: rgb(255, 235, 249);\n"
"font: 11pt \"Sans Serif\";"))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.infoButton = QtGui.QPushButton(SurveyItemWidget)
        self.infoButton.setObjectName(_fromUtf8("infoButton"))
        self.gridLayout.addWidget(self.infoButton, 0, 1, 1, 1)
        self.joinButton = QtGui.QPushButton(SurveyItemWidget)
        self.joinButton.setObjectName(_fromUtf8("joinButton"))
        self.gridLayout.addWidget(self.joinButton, 0, 2, 1, 1)

        self.retranslateUi(SurveyItemWidget)
        QtCore.QMetaObject.connectSlotsByName(SurveyItemWidget)

    def retranslateUi(self, SurveyItemWidget):
        SurveyItemWidget.setWindowTitle(QtGui.QApplication.translate("SurveyItemWidget", "survey item", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SurveyItemWidget", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.infoButton.setText(QtGui.QApplication.translate("SurveyItemWidget", "Detaylar", None, QtGui.QApplication.UnicodeUTF8))
        self.joinButton.setText(QtGui.QApplication.translate("SurveyItemWidget", "Katıl", None, QtGui.QApplication.UnicodeUTF8))

