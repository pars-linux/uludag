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


class MainWindow(QtGui.QMainWindow, mainWindow.Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        
        # Should not be here
        self.instance = avahiservices.Zeroconf("moon", gethostname(), "_presence._tcp")
        self.instance.connect_dbus()
        self.instance.connect_avahi()
        self.instance.connect()
            print "Self Connected"

        # Filling Window
        self.connect(self.pushButton, SIGNAL("clicked()"),self.fillWidget)

    def fillWidget(self):
        if self.instance.get_contacts():
            print "Service found Yeehaaaa"
        else:
            print "Service not found o_O"

        self.listWidget.clear()
        self.connect(self.listWidget, SIGNAL("itemClicked(QListWidgetItem*)"), self.connectHost)
        for contact in self.instance.get_contacts():
            item = QtGui.QListWidgetItem("%s" % (contact), self.listWidget)
            item.setData(Qt.UserRole, QVariant(unicode(contact)))

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

