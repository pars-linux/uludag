#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt Libs
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from config_ui import *

class SystemServicesConfig(QWidget, Ui_ServiceConfig):
    def __init__(self, parent, config):
        QWidget.__init__(self, parent)
        self.setupUi(self)

        # Read plasmoid config
        self.config = config

        # Get enabled services from config
        self.enabledServices = str(self.config.readEntry("services", '')).split(',')

        # Show descriptions if showDesc is checked
        self.showDesc.setChecked(self.config.readEntry("showdesc", QVariant(True)).toBool())

    def addItemToList(self, package):
        # Create an item to add the list
        item = QListWidgetItem(self.serviceList)

        # Create a widget to make it default widget for item
        check = QCheckBox(package, self.serviceList)

        # Set this widget as item widget
        self.serviceList.setItemWidget(item, check)

        # Check widget if service enabled in config
        if str(package) in self.enabledServices:
            check.setChecked(True)

