# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widgetMain.ui'
#
# Created: Tue Jul 06 15:04:09 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWidget(object):
    def setupUi(self, MainWidget):
        MainWidget.setObjectName("MainWidget")
        MainWidget.resize(500, 300)
        MainWidget.setMinimumSize(QtCore.QSize(500, 300))
        MainWidget.setMaximumSize(QtCore.QSize(500, 300))
        self.gridLayout_2 = QtGui.QGridLayout(MainWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lblHeading = QtGui.QLabel(MainWidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.lblHeading.setFont(font)
        self.lblHeading.setObjectName("lblHeading")
        self.verticalLayout.addWidget(self.lblHeading)
        self.line = QtGui.QFrame(MainWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.stackedWidget = QtGui.QStackedWidget(MainWidget)
        self.stackedWidget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.stackedWidget.setObjectName("stackedWidget")
        self.gridLayout.addWidget(self.stackedWidget, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnBack = QtGui.QPushButton(MainWidget)
        self.btnBack.setObjectName("btnBack")
        self.horizontalLayout.addWidget(self.btnBack)
        self.btnNext = QtGui.QPushButton(MainWidget)
        self.btnNext.setObjectName("btnNext")
        self.horizontalLayout.addWidget(self.btnNext)
        self.btnFinish = QtGui.QPushButton(MainWidget)
        self.btnFinish.setObjectName("btnFinish")
        self.horizontalLayout.addWidget(self.btnFinish)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lblCompany = QtGui.QLabel(MainWidget)
        self.lblCompany.setEnabled(False)
        self.lblCompany.setObjectName("lblCompany")
        self.horizontalLayout_2.addWidget(self.lblCompany)
        self.line_2 = QtGui.QFrame(MainWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(MainWidget)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWidget)

    def retranslateUi(self, MainWidget):
        MainWidget.setWindowTitle(QtGui.QApplication.translate("MainWidget", "PaW: Pardus Windows Installer", None, QtGui.QApplication.UnicodeUTF8))
        self.lblHeading.setText(QtGui.QApplication.translate("MainWidget", "Title Here", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBack.setText(QtGui.QApplication.translate("MainWidget", "< &Back", None, QtGui.QApplication.UnicodeUTF8))
        self.btnNext.setText(QtGui.QApplication.translate("MainWidget", "&Next >", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFinish.setText(QtGui.QApplication.translate("MainWidget", "&Finish!", None, QtGui.QApplication.UnicodeUTF8))
        self.lblCompany.setText(QtGui.QApplication.translate("MainWidget", "Pardus Linux", None, QtGui.QApplication.UnicodeUTF8))

