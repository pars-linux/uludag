#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

import sys

import parser
from utility import *

xorg_conf = "/etc/X11/xorg.conf"

modes = (
    "2048x1536",
    "1920x1440",
    "1920x1200",
    "1680x1050",
    "1600x1024",
    "1440x900",
    "1400x1050",
    "1280x1024",
    "1280x960",
    "1280x800",
    "1280x768",
    "1152x864",
    "1152x768",
    "1024x768",
    "800x600",
    "640x480"
)

class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        modeLabel = QLabel(i18n("Resolution:"), self)
        modeList = QComboBox(self)
        for mode in modes:
            modeList.insertItem(mode)
        modeList.setEditable(True)

        depthLabel = QLabel(i18n("Color depth:"), self)
        depthList = QComboBox(self)
        depthList.insertItem(i18n("True Color (24 bit)"))
        depthList.insertItem(i18n("High Color (16 bit)"))

        applyButton = QPushButton(i18n("Apply"), self)

        vb = QVBoxLayout(self, 6, 6, "mainLayout")

        vb.addWidget(modeLabel)
        vb.addWidget(modeList)
        vb.addWidget(depthLabel)
        vb.addWidget(depthList)
        vb.addStretch()

        hb = QHBoxLayout(self)

        hb.addStretch()
        hb.addWidget(applyButton)
        vb.addLayout(hb)

        self.connect(applyButton, SIGNAL("clicked()"), self.slotApply)

        self.modeList = modeList
        self.depthList = depthList

        self.readConfig()

    def readConfig(self):
        p = parser.XorgParser()
        try:
            p.parseFile(xorg_conf)
        except IOError:
            QMessageBox.critical(self, i18n("Error"), i18n("Unable to read configuration."))
            sys.exit(1)

        screenSec = p.getSections("Screen")[0]
        depth = screenSec.get("DefaultDepth", 0, 16)

        displaySec = screenSec.getSections("Display")[0]
        mode = displaySec.get("Modes", 0)
        if not mode:
            mode = "800x600"

        if depth == 16:
            self.depthList.setCurrentItem(1)
        else:
            self.depthList.setCurrentItem(0)

        self.modeList.setCurrentText(mode)

    def writeConfig(self):
        p = parser.XorgParser()
        try:
            p.parseFile(xorg_conf)
        except IOError:
            QMessageBox.critical(self, i18n("Error"), i18n("Unable to read configuration."))
            sys.exit(1)

        mode = str(self.modeList.currentText())

        deviceSec = p.getSections("Device")[0]
        driver = deviceSec.get("Driver", 0, "vesa")

        if driver == "intel":
            deviceSec.options["Monitor-VGA"] = "Monitor0"

            monitorSec = p.getSections("Monitor")[0]
            monitorSec.options["PreferredMode"] = mode

        screenSec = p.getSections("Screen")[0]

        if self.depthList.currentItem() == 0:
            depth = 24
        else:
            depth = 16

        screenSec.set("DefaultDepth", depth)

        displaySec = screenSec.getSections("Display")[0]
        displaySec.set("Depth", depth)

        displaySec.set("Modes", mode, "800x600", "640x480")

        try:
            open(xorg_conf, "w").write(p.toString())
        except IOError:
            QMessageBox.critical(self, i18n("Error"), i18n("Unable to save configuration."))
            sys.exit(1)

    def slotApply(self):
        self.writeConfig()

        QMessageBox.information(self, i18n("Configuration saved"),
                i18n("Xorg configuration saved. The changes will effect upon next start of Xorg server."))

        self.readConfig()

    def slotHelp(self):
        help = HelpDialog('display-config', i18n('Help'), self.parent())
        help.show()
