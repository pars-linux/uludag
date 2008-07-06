# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Sun Jul  6 16:42:06 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_GtkKde4(object):
    def setupUi(self, GtkKde4):
        GtkKde4.setObjectName("GtkKde4")
        GtkKde4.resize(418,158)
        self.gridLayout = QtGui.QGridLayout(GtkKde4)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtGui.QLabel(GtkKde4)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3,0,0,1,4)
        self.label = QtGui.QLabel(GtkKde4)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label,1,0,1,1)
        self.styleBox = QtGui.QComboBox(GtkKde4)
        self.styleBox.setObjectName("styleBox")
        self.gridLayout.addWidget(self.styleBox,1,1,1,3)
        self.label_2 = QtGui.QLabel(GtkKde4)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2,2,0,1,1)
        self.iconBox = QtGui.QComboBox(GtkKde4)
        self.iconBox.setObjectName("iconBox")
        self.gridLayout.addWidget(self.iconBox,2,1,1,3)
        self.label_4 = QtGui.QLabel(GtkKde4)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4,3,0,1,1)
        self.fontType = QtGui.QFontComboBox(GtkKde4)
        self.fontType.setObjectName("fontType")
        self.gridLayout.addWidget(self.fontType,3,1,1,2)
        self.fontSize = QtGui.QSpinBox(GtkKde4)
        self.fontSize.setObjectName("fontSize")
        self.gridLayout.addWidget(self.fontSize,3,3,1,1)
        spacerItem = QtGui.QSpacerItem(136,25,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem,4,0,1,2)
        self.changeStyle = QtGui.QPushButton(GtkKde4)
        self.changeStyle.setObjectName("changeStyle")
        self.gridLayout.addWidget(self.changeStyle,4,2,1,1)
        self.Cancel = QtGui.QPushButton(GtkKde4)
        self.Cancel.setObjectName("Cancel")
        self.gridLayout.addWidget(self.Cancel,4,3,1,1)
        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1,5,2,1,1)

        self.retranslateUi(GtkKde4)
        QtCore.QObject.connect(self.Cancel,QtCore.SIGNAL("clicked()"),GtkKde4.close)
        QtCore.QMetaObject.connectSlotsByName(GtkKde4)

    def retranslateUi(self, GtkKde4):
        GtkKde4.setWindowTitle(QtGui.QApplication.translate("GtkKde4", "Gtk-KDE4", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("GtkKde4", "Select style,font and icon theme below to apply GTK-2.0 apps like Firefox.", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GtkKde4", "Style :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GtkKde4", "Icon Theme :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("GtkKde4", "Font :", None, QtGui.QApplication.UnicodeUTF8))
        self.fontSize.setSuffix(QtGui.QApplication.translate("GtkKde4", " pt", None, QtGui.QApplication.UnicodeUTF8))
        self.changeStyle.setText(QtGui.QApplication.translate("GtkKde4", "Change &GTK Styles", None, QtGui.QApplication.UnicodeUTF8))
        self.Cancel.setText(QtGui.QApplication.translate("GtkKde4", "&Cancel", None, QtGui.QApplication.UnicodeUTF8))

