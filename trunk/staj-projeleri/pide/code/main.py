# System
import sys

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# UI
from ui_main import Ui_MainWidget

# Backend
from avahiservices import Zeroconf
from receiver import StreamHandler

# Item widget
from item import ItemListWidgetItem, ItemWidget

# Application Stuff
from dbus.mainloop.qt import DBusQtMainLoop
from socket import gethostname

# Config
from config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME


class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.setupUi(self)

        # Filling Window
        self.connect(self.pushNew, QtCore.SIGNAL("clicked()"), self.fillWindow)

        self.iface = Zeroconf("moon", gethostname(), "_pide._tcp")
        self.iface.connect_dbus()
        self.iface.connect_avahi()
        self.iface.connect()

    def fillWindow(self):
        self.buildItemList()


    def clearItemList(self):
        self.listItems.clear()

    def makeItemWidget(self, name, address):
        widget = ItemWidget(name, address)
        return widget

    def addItem(self, name, address):
        # Build widget and widget item
        widget = self.makeItemWidget(name, address)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

    def buildItemList(self):
        self.clearItemList()

        # Lists of all contacts
        self.users=[]

        self.iface.get_contacts()

        contacts = self.iface.get_contacts()
        for name in contacts.keys():
            name, domain, interface, protocol, host, address, port, bare_name, txt = contacts[name]
            name = self.splitName(name)
            # For Safety :D
            #if name == "saturn":
            self.users.append([name, address])
            self.addItem(name, address)

    def splitName(self, name):
        first, second = name.split("@")
        return first


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    DBusQtMainLoop(set_as_default=True)
    # Create Main Widget
    main = MainWidget()
    main.show()

    # Run the application
    app.exec_()

