#!/usr/bin/python
# -*- coding: utf-8 -*-

# Qt
from PyQt4 import QtGui

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
        self.ui.spinInterval.setValue(int(config.readEntry("pollinterval", "5")))
        self.ui.checkTraffic.setChecked(config.readEntry("showtraffic", "true") == "true")
        self.ui.checkWifi.setChecked(config.readEntry("showwifi", "true") == "true")
        self.ui.checkStatus.setChecked(config.readEntry("showstatus", "true") == "true")

    def writeConf(self, config):
        config.writeEntry("showtraffic", str(self.ui.checkTraffic.isChecked()).lower())
        config.writeEntry("showwifi", str(self.ui.checkWifi.isChecked()).lower())
        config.writeEntry("showstatus", str(self.ui.checkStatus.isChecked()).lower())
        config.writeEntry("pollinterval", str(self.ui.spinInterval.value()))

class ConfigPopup(QtGui.QWidget):

    def __init__(self, config):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_configPopup()
        self.ui.setupUi(self)

