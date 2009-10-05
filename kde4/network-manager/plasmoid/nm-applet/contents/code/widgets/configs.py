#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt
from PyQt4 import QtGui
from PyQt4.Qt import QVariant

# Configuration widgets
from configIconui import Ui_configIcon
from configPopupui import Ui_configPopup

class ConfigIcon(QtGui.QWidget):

    def __init__(self, config):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_configIcon()
        self.ui.setupUi(self)
        self.parseConf(config)

    def parseConf(self, config):
        self.ui.spinInterval.setValue(int(config.readEntry("pollinterval", QVariant("5")).toInt()[0]))
        self.ui.checkTraffic.setChecked(config.readEntry("showtraffic", QVariant("true")).toBool())
        self.ui.checkWifi.setChecked(config.readEntry("showwifi", QVariant("true")).toBool())
        self.ui.checkStatus.setChecked(config.readEntry("showstatus", QVariant("true")).toBool())
        self.ui.checkBattery.setChecked(config.readEntry("followsolid", QVariant("true")).toBool())

    def writeConf(self, config):
        config.writeEntry("showtraffic", self.ui.checkTraffic.isChecked())
        config.writeEntry("showwifi", self.ui.checkWifi.isChecked())
        config.writeEntry("showstatus", self.ui.checkStatus.isChecked())
        config.writeEntry("followsolid", self.ui.checkBattery.isChecked())
        config.writeEntry("pollinterval", self.ui.spinInterval.value())

class ConfigPopup(QtGui.QWidget):

    def __init__(self, config):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_configPopup()
        self.ui.setupUi(self)

