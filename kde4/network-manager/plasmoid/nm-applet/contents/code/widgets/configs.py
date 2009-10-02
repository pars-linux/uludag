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
        def readEntry(config, entryName, default):
            entry = config.readEntry(entryName, default)
            if type(entry) == type(QVariant()):
                return entry.toString()
            else:
                return entry

        self.ui.spinInterval.setValue(int(readEntry(config, "pollinterval", "5")))
        self.ui.checkTraffic.setChecked(readEntry(config, "showtraffic", "true") == "true")
        self.ui.checkWifi.setChecked(readEntry(config, "showwifi", "true") == "true")
        self.ui.checkStatus.setChecked(readEntry(config, "showstatus", "true") == "true")
        self.ui.checkBattery.setChecked(readEntry(config, "followsolid", "true") == "true")

    def writeConf(self, config):
        config.writeEntry("showtraffic", str(self.ui.checkTraffic.isChecked()).lower())
        config.writeEntry("showwifi", str(self.ui.checkWifi.isChecked()).lower())
        config.writeEntry("showstatus", str(self.ui.checkStatus.isChecked()).lower())
        config.writeEntry("followsolid", str(self.ui.checkBattery.isChecked()).lower())
        config.writeEntry("pollinterval", str(self.ui.spinInterval.value()))

class ConfigPopup(QtGui.QWidget):

    def __init__(self, config):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_configPopup()
        self.ui.setupUi(self)

