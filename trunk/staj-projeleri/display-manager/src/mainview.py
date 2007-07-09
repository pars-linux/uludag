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

import comar

from utility import *


class ScreenWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        vb = QVBoxLayout(self, 6, 6, "screenLayout")

        grid = QGridLayout(vb, 2, 3)

        cardLabel = QLabel(i18n("Video card:"), self)
        self.cardList = QComboBox(self)
        self.cardList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        cardMenu = QToolButton(self)
        cardMenu.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        cardMenu.setIconSet(getIconSet("configure.png"))

        monitorLabel = QLabel(i18n("Monitor:"), self)
        self.monitorList = QComboBox(self)
        self.monitorList.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        monitorMenu = QToolButton(self)
        monitorMenu.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        monitorMenu.setIconSet(getIconSet("configure.png"))

        grid.addWidget(cardLabel, 0, 0)
        grid.addWidget(self.cardList, 0, 1)
        grid.addWidget(cardMenu, 0, 2)

        grid.addWidget(monitorLabel, 1, 0)
        grid.addWidget(self.monitorList, 1, 1)
        grid.addWidget(monitorMenu, 1, 2)

        hb = QHBoxLayout(vb, 3)
        hb.addItem(QSpacerItem(100, 20))

        resLabel = QLabel(i18n("Resolution:"), self)
        resList = QComboBox(self)
        depthLabel = QLabel(i18n("Color depth:"), self)
        depthList = QComboBox(self)

        vb2 = QVBoxLayout(hb, 3, "modeLayout")
        vb2.addWidget(resLabel)
        vb2.addWidget(resList)
        vb2.addWidget(depthLabel)
        vb2.addWidget(depthList)
        vb2.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

class widgetMain(QWidget):
    def __init__(self, parent):
        self.setupComar()

        QWidget.__init__(self, parent)

        self.setupForm()

        self.link.Xorg.Display.listCards(id=1)

    def setupComar(self):
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)

    def setupForm(self):
        vb = QVBoxLayout(self, 6, 6, "mainLayout")

        label = QLabel(i18n("Desktop setup:"), self)
        desktopSetup = QComboBox(self)
        desktopSetup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        desktopSetupButton = QToolButton(self)
        desktopSetupButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        desktopSetupButton.setIconSet(getIconSet("configure.png"))

        hb = QHBoxLayout(vb, 3, "topLayout")
        hb.addWidget(label)
        hb.addWidget(desktopSetup)
        hb.addWidget(desktopSetupButton)

        self.tab = QTabWidget(self)
        self.tab.addTab(ScreenWidget(self), i18n("Screen &1"))
        self.tab.addTab(ScreenWidget(self), i18n("Screen &2"))
        vb.addWidget(self.tab)

        menuButton = QPushButton(i18n("&Menu"), self)
        okButton = QPushButton(i18n("&OK"), self)
        applyButton = QPushButton(i18n("&Apply"), self)
        cancelButton = QPushButton(i18n("&Cancel"), self)

        hb = QHBoxLayout(vb, 3, "bottomLayout")
        hb.addWidget(menuButton)
        hb.addItem(QSpacerItem(200, 20))
        hb.addWidget(okButton)
        hb.addWidget(applyButton)
        hb.addWidget(cancelButton)

    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.id == 1:
            for index in (0, 1):
                page = self.tab.page(index)
                cards = reply.data.splitlines()
                for card in cards:
                    cardId, name = card.split(" ", 1)
                    page.cardList.insertItem(name)

    def slotHelp(self):
        help = HelpDialog('display-manager', i18n('Help'), self.parent())
        help.show()
