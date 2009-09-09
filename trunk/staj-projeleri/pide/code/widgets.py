#!/usr/bin/python
# -*- coding: utf-8 -*-
# System
import sys

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# KDE Stuff
from PyKDE4 import kdeui

# Application Stuff
from dbus.mainloop.qt import DBusQtMainLoop
from socket import gethostname
from item import Ui_ServiceItemWidget
import avahiservices

class ServiceItemWidget(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self, None)
        
        self.ui = Ui_ServiceItemWidget()
        self.ui.setupUi(self)

    def fillWidget(self, contact):
        self.ui.labelName.setText(contact)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    DBusQtMainLoop(set_as_default=True)
    # Create Main Widget
    main = ServiceItemWidget()
    main.show()

    # Run the application
    app.exec_()


