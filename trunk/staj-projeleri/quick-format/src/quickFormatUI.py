# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quickFormat.ui'
#
# Created: Tue Sep  8 13:41:29 2009
#      by: PyQt4 UI code generator 4.5.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(270, 278)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(270, 278))
        MainWindow.setMaximumSize(QtCore.QSize(270, 278))
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.grpBoxDeviceName = QtGui.QGroupBox(self.centralwidget)
        self.grpBoxDeviceName.setMinimumSize(QtCore.QSize(0, 170))
        self.grpBoxDeviceName.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(False)
        self.grpBoxDeviceName.setFont(font)
        self.grpBoxDeviceName.setObjectName("grpBoxDeviceName")
        self.grpBoxDeviceName.setStyleSheet("QGroupBox::Title{color: red;}")
        self.verticalLayoutWidget = QtGui.QWidget(self.grpBoxDeviceName)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 25, 241, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_deviceName = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.lbl_deviceName.setFont(font)
        self.lbl_deviceName.setObjectName("lbl_deviceName")
        self.verticalLayout_2.addWidget(self.lbl_deviceName)
        self.cmb_deviceName = QtGui.QComboBox(self.verticalLayoutWidget)
        self.cmb_deviceName.setObjectName("cmb_deviceName")
        self.verticalLayout_2.addWidget(self.cmb_deviceName)
        self.lbl_fileSystem = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.lbl_fileSystem.setFont(font)
        self.lbl_fileSystem.setObjectName("lbl_fileSystem")
        self.verticalLayout_2.addWidget(self.lbl_fileSystem)
        self.cmb_fileSystem = QtGui.QComboBox(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.cmb_fileSystem.setFont(font)
        self.cmb_fileSystem.setObjectName("cmb_fileSystem")
        self.verticalLayout_2.addWidget(self.cmb_fileSystem)
        self.lbl_volumeLabel = QtGui.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.lbl_volumeLabel.setFont(font)
        self.lbl_volumeLabel.setObjectName("lbl_volumeLabel")
        self.verticalLayout_2.addWidget(self.lbl_volumeLabel)
        self.txt_volumeLabel = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.txt_volumeLabel.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.txt_volumeLabel.setFont(font)
        self.txt_volumeLabel.setObjectName("txt_volumeLabel")
        self.verticalLayout_2.addWidget(self.txt_volumeLabel)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.verticalLayout.addWidget(self.grpBoxDeviceName)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setContentsMargins(10, -1, 10, 20)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lbl_progress = QtGui.QLabel(self.centralwidget)
        self.lbl_progress.setMaximumSize(QtCore.QSize(16777215, 20))
        self.lbl_progress.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_progress.setObjectName("lbl_progress")
        self.verticalLayout_3.addWidget(self.lbl_progress)
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setMinimumSize(QtCore.QSize(0, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(16777215, 20))
        self.progressBar.setAutoFillBackground(False)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", QtCore.QVariant(192831))
        self.progressBar.setTextVisible(True)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtGui.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_3.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.btn_format = QtGui.QPushButton(self.centralwidget)
        self.btn_format.setObjectName("btn_format")
        self.horizontalLayout.addWidget(self.btn_format)
        self.btn_cancel = QtGui.QPushButton(self.centralwidget)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout.addWidget(self.btn_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 270, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        
        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Disk Formatting Utility", None, QtGui.QApplication.UnicodeUTF8))
        self.grpBoxDeviceName.setTitle(QtGui.QApplication.translate("MainWindow", "WARNING: All data will be erased on the disk", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_deviceName.setText(QtGui.QApplication.translate("MainWindow", "Device Name", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_fileSystem.setText(QtGui.QApplication.translate("MainWindow", "File System", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_volumeLabel.setText(QtGui.QApplication.translate("MainWindow", "Volume Label", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_progress.setText(QtGui.QApplication.translate("MainWindow", "Please wait while formatting...", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_format.setText(QtGui.QApplication.translate("MainWindow", "Format", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

