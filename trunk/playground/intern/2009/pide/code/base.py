#!/usr/bin/python
# -*- coding: utf-8 -*-

# System
import sys

# Qt Stuff
from PyQt4 import QtGui
from PyQt4.QtCore import *

# PyKDE4 Stuff
from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

# Application Stuff
from dbus.mainloop.qt import DBusQtMainLoop
from socket import gethostname
import mainWindow
import avahiservices
import iface
from widgets import ServiceItemWidget


class MainWindow(QtGui.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.iface = ServiceItemWidget()
        # Should not be here
        self.instance = avahiservices.Zeroconf("moon", gethostname(), "_presence._tcp")
        self.instance.connect_dbus()
        self.instance.connect_avahi()
        self.instance.connect()
        self.contacts={}

        # Filling Window
        self.connect(self.pushButton, SIGNAL("clicked()"), self.allWidgets)

    def allWidgets(self):
        self.instance.get_contacts()

        self.listWidget.clear()
        self.connect(self.listWidget, SIGNAL("itemClicked(QListWidgetItem*)"), self.connectHost)
        for contact in self.instance.get_contacts():
            self.contacts[contact] = self.iface.fillWidget(contact)


    def connectHost(self, item):
        self.pkg = self.interface.getPackage(str(item.data(Qt.UserRole).toString()))
        self.lineEdit_2.setText(unicode(self.pkg.name))
        self.textEdit.setText(unicode(self.pkg.summary))
        self.textEdit_2.setText(unicode(self.pkg.description))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    DBusQtMainLoop(set_as_default=True)
    # Create Main Widget
    main = MainWindow()
    main.show()

    # Run the application
    app.exec_()

