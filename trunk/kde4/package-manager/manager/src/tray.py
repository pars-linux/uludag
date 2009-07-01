#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import *

from PyKDE4.kdeui import *
from PyKDE4.kdecore import *

import config
import backend

class Tray(KSystemTrayIcon):
    def __init__(self, parent):
        KSystemTrayIcon.__init__(self, parent)
        self.defaultIcon = KIcon(":/data/package-manager.png")
        self.iface = backend.pm.Iface()
        self.notification = None
        self.appWindow = parent

        self.initializeTimer()
        self.initializePopup()

        self.settingsChanged()
        self.lastUpgrades = []
        self.unread = 0

    def initializeTimer(self):
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.checkUpdate)
        self.interval = config.PMConfig().updateCheckInterval()
        self.updateInterval(self.interval)

    def initializePopup(self):
        self.setIcon(self.defaultIcon)

        menu = KActionMenu(i18n("Update"), self)
        for name, address in self.iface.getRepositories():
            self.__addAction(name, menu)
        self.__addAction(i18n("All"), menu)
        self.contextMenu().addAction(menu)
        self.contextMenu().addSeparator()

    def __addAction(self, name, menu):
        action = QtGui.QAction(name, self)
        menu.addAction(action)
        self.connect(action, SIGNAL("triggered()"), self.updateRepo)

    def updateRepo(self):
        if not self.iface.operationInProgress():
            repoName = unicode(self.sender().iconText())
            self.iface.updateRepository(repoName)

    def checkUpdate(self):
        if not self.appWindow.isVisible() and not self.iface.operationInProgress():
            self.iface.updateRepositories()

    def showPopup(self):
        upgrades = self.iface.getUpdates()
        if config.PMConfig().installUpdatesAutomatically():
            if not self.appWindow.isVisible() and not self.iface.operationInProgress():
                self.iface.upgradePackages(upgrades)
            return

        newUpgrades = set(upgrades) - set(self.lastUpgrades)
        self.lastUpgrades = upgrades
        if not len(upgrades) or not newUpgrades:
            return

        if self.notification:
            self.notification.close()
        self.notification = KNotification("Updates")
        self.notification.setText(i18n("There are <b>%1</b> updates available!", len(upgrades)))
        self.notification.setActions(QStringList((i18n("Show Updates"), i18n("Ignore"))))
        self.notification.setFlags(KNotification.Persistent)
        self.notification.setComponentData(KComponentData("package-manager","package-manager"))
        self.connect(self.notification, SIGNAL("action1Activated()"), lambda:self.emit(SIGNAL("showUpdatesSelected()")))
        self.notification.sendEvent()

    def updateInterval(self, min):
        # minutes to milliseconds conversion
        interval = min * 60 * 1000
        if interval != self.interval:
            self.interval = interval
            self.timer.stop()
            if interval:
                self.timer.start(interval)

    def settingsChanged(self):
        cfg = config.PMConfig()
        if cfg.systemTray():
            self.show()
        else:
            self.hide()

        self.updateInterval(cfg.updateCheckInterval())

    # stolen from Akregator
    def slotSetUnread(self, unread):
        if self.unread == unread:
            return

        self.unread = unread

        if unread == 0:
            self.setIcon(self.defaultIcon)
        else:
            oldWidth = self.defaultIcon.pixmap(22).size().width()

            if oldWidth == 0:
                return

            countStr = "%s" % unread
            f = KGlobalSettings.generalFont()
            f.setBold(True)

            pointSize = f.pointSizeF()
            fm = QtGui.QFontMetrics(f)
            w = fm.width(countStr)
            if w > (oldWidth - 2):
                pointSize *= float(oldWidth - 2) / float(w)
                f.setPointSizeF(pointSize)

            # overlay
            overlayImg = QtGui.QPixmap(self.defaultIcon.pixmap(22))
            p = QtGui.QPainter(overlayImg)
            p.setFont(f)
            scheme = KColorScheme(QtGui.QPalette.Active, KColorScheme.View)

            fm = QtGui.QFontMetrics(f)
            boundingRect = QRect(fm.tightBoundingRect(countStr))
            boundingRect.adjust(0, 0, 0, 2)
            boundingRect.setHeight(min(boundingRect.height(), oldWidth))
            boundingRect.moveTo((oldWidth - boundingRect.width()) / 2,
                                ((oldWidth - boundingRect.height()) / 2) - 1)
            p.setOpacity(0.7)
            p.setBrush(scheme.background(KColorScheme.LinkBackground))
            p.setPen(scheme.background(KColorScheme.LinkBackground).color())
            p.drawRoundedRect(boundingRect, 2.0, 2.0);

            p.setBrush(Qt.NoBrush)
            p.setPen(scheme.foreground(KColorScheme.LinkText).color())
            p.setOpacity(1.0)
            p.drawText(overlayImg.rect(), Qt.AlignCenter, countStr)

            p.end()

            self.setIcon(QtGui.QIcon(overlayImg))
