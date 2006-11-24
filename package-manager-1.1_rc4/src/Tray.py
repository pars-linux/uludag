#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import sys

from qt import *
from kdeui import *
from kdecore import *

from pisi.api import list_upgradable

from BalloonMessage import *

class Tray(KSystemTray):
    def __init__(self, parent=None):
        KSystemTray.__init__(self, parent)
        self.parent = parent
        self.icon = KGlobal.iconLoader().loadIcon("package-manager", KIcon.Desktop, 24)
        self.overlayIcon = self.icon.convertToImage()
        self.setPixmap(self.icon)

        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.checkUpdate)
        self.interval = 0
        self.lastUpgrades = []

    def showPopup(self):
        from sets import Set as set 

        upgrades = list_upgradable()
        newUpgrades = set(upgrades) - set(self.lastUpgrades)
        self.lastUpgrades = upgrades
        if not len(upgrades) or not newUpgrades:
            return

        icon = KGlobal.iconLoader().loadIcon("package-manager", KIcon.Desktop, 48)
        message = i18n("There are <b>%1</b> updates available!").arg(len(upgrades))
        self.popup = BalloonMessage(self, icon, message)
        pos = self.mapToGlobal(self.pos())
        self.popup.setAnchor(pos)
        self.popup.show()

    def updateInterval(self, min):
        # minutes to milliseconds conversion
        interval = min * 60 * 1000
        if interval != self.interval:
            self.interval = interval
            self.timer.stop()
            if interval:
                self.timer.start(interval)

    def checkUpdate(self):
        manager = self.parent.mainwidget
        # if package-manager is being used, do not start update-repo operation, this may annoy users.
        # And also if a command is in progress do not try to check updates.
        if not self.parent.isHidden() or manager.command.inProgress():
            return

        manager.trayUpdateCheck()

    # stolen from Akregator
    def updateTrayIcon(self):
        nofUpgrades = len(list_upgradable())
        if not nofUpgrades:
            self.setPixmap(self.icon)
            return

        oldW = self.pixmap().size().width()
        oldH = self.pixmap().size().height()

        uStr = QString.number(nofUpgrades);
        f = KGlobalSettings.generalFont()
        f.setBold(True);
        pointSize = f.pointSizeFloat()
        fm = QFontMetrics(f)
        w = fm.width(uStr)

        if w > oldW:
            pointSize *= float(oldW) / float(w)
            f.setPointSizeFloat(pointSize)

        pix = QPixmap(oldW, oldH)
        pix.fill(Qt.white)
        p = QPainter(pix)
        p.setFont(f)
        p.setPen(Qt.blue)
        p.drawText(pix.rect(), Qt.AlignCenter, uStr)

        pix.setMask(pix.createHeuristicMask())
        img = QImage(pix.convertToImage())

        overlayImg = QImage(self.overlayIcon.copy())
        KIconEffect.overlay(overlayImg, img)

        icon = QPixmap()
        icon.convertFromImage(overlayImg)
        self.setPixmap(icon)

        # for cannot destroy paint device error
        p = None
