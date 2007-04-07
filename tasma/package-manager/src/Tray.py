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

import pisi

from BalloonMessage import *

ID_TRAY_INTERVAL_CHECK=30

class Tray(KSystemTray):
    def __init__(self, parent=None):
        KSystemTray.__init__(self, parent)
        self.parent = parent
        self.icon = self.loadIcon("package-manager")
        self.overlayIcon = self.icon.convertToImage()
        self.setPixmap(self.icon)

        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.checkUpdate)
        self.interval = 0
        self.lastUpgrades = []

        self.popupMenu = KPopupMenu(self.contextMenu())
        self.contextMenu().insertItem(i18n("Update"), self.popupMenu)

        for repo in self.parent.mainwidget.command.getRepoList():
            self.popupMenu.insertItem("%s" % repo)
        self.popupMenu.insertSeparator()
        self.id = self.popupMenu.insertItem(i18n("All"))

        self.connect(self.popupMenu, SIGNAL("activated(int)"), self.slotUpdateRepo)

    def slotUpdateRepo(self, id):
        if id == self.id:
            self.checkUpdate(forced=True)
        else:
            self.checkUpdate(repo=self.contextMenu().text(id), forced=True)

    def showPopup(self):
        from sets import Set as set 

        upgrades = pisi.api.list_upgradable()
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

    def checkUpdate(self, repo = None, forced = False):
        manager = self.parent.mainwidget
        # timer interval check should not be run if any command is in progress
        if manager.command.inProgress():
            return

        manager.trayUpdateCheck(repo, forced)

    # stolen from Akregator
    def updateTrayIcon(self):
        nofUpgrades = len(pisi.api.list_upgradable())
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
