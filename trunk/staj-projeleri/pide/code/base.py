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

        DBusQtMainLoop(set_as_default=True)

        instance = avahiservices.Zeroconf("moon", gethostname(), "_presence._tcp")
        instance.connect_dbus()
        instance.connect_avahi()
        instance.connect()

        self.interface = iface.Iface()
        print self.interface

#        self.connect(self.listWidget, SIGNAL("itemClicked(QListWidgetItem*)"), self.itemDetail)
#        for package in self.interface.getInstalledPackageList():
#            item = QtGui.QListWidgetItem("%s" % (package), self.listWidget)
#            item.setData(Qt.UserRole, QVariant(unicode(package)))
#    def itemDetail(self, item):
#        self.pkg = self.interface.getPackage(str(item.data(Qt.UserRole).toString()))
#        self.lineEdit_2.setText(unicode(self.pkg.name))
#        self.textEdit.setText(unicode(self.pkg.summary))
#        self.textEdit_2.setText(unicode(self.pkg.description))




if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    # Create Main Widget
    main = MainWindow()
    main.show()

    # Run the application
    app.exec_()

