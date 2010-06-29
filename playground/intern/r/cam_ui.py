# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cam_ui.ui'
#
# Created: Mon Jun 28 14:58:23 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!
import Image
import ImageQt

from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n
from PyQt4 import QtGui, QtCore
import pyv4l2


from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(615, 487)
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(100, 80, 391, 281))
        self.label.setText("")
        self.label.setObjectName("label")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.image = ImageQt.ImageQt(pyv4l2.test(123))
        self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

