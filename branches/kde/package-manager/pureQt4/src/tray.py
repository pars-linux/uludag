#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import *

from pmutils import *
from context import *

import config
import backend

class PTray:
    def __init__(self):
        self.defaultIcon = QtGui.QIcon(":/data/package-manager.png")
        self.setIcon(self.defaultIcon)
        self.lastUpgrades = []
        self.unread = 0
        self.iface = backend.pm.Iface()
        self.notification = None

        self.initializeTimer()
        self.initializePopup()

        self.settingsChanged()

    def initializeTimer(self):
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), self.checkUpdate)
        self.interval = config.PMConfig().updateCheckInterval()
        self.updateInterval(self.interval)

    def initializePopup(self):
        pass

    def populateRepositoryMenu(self):
        pass

    def _addAction(self, name, menu):
        action = QtGui.QAction(name, self)
        menu.addAction(action)
        self.connect(action, SIGNAL("triggered()"), self.updateRepo)

    def updateRepo(self):
        if not self.iface.operationInProgress():
            repoName = unicode(self.sender().iconText())
            if repoName == i18n("All"):
                self.iface.updateRepositories()
            else:
                self.iface.updateRepository(repoName)

    def checkUpdate(self):
        if not self.appWindow.isVisible() and not self.iface.operationInProgress():
            self.iface.updateRepositories()

    def _ready_to_popup(self):
        upgrades = self.iface.getUpdates()
        self.slotSetUnread(len(upgrades))

        if config.PMConfig().installUpdatesAutomatically():
            if not self.appWindow.isVisible() and not self.iface.operationInProgress():
                self.iface.upgradePackages(upgrades)
            return False

        newUpgrades = set(upgrades) - set(self.lastUpgrades)
        self.lastUpgrades = upgrades
        if not len(upgrades) or not newUpgrades:
            return False

        return True

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
            self.updateTrayUnread()
        else:
            self.hide()

        self.updateInterval(cfg.updateCheckInterval())

    def updateTrayUnread(self):
        waitCursor()
        noUpgrades = len(self.iface.getUpdates())
        self.slotSetUnread(noUpgrades)
        restoreCursor()

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
            f = QtGui.QFont(Pds.settings('font','Sans'))
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
            scheme = QtGui.QBrush() #KColorScheme(QtGui.QPalette.Active, KColorScheme.View)

            fm = QtGui.QFontMetrics(f)
            boundingRect = QRect(fm.tightBoundingRect(countStr))
            boundingRect.adjust(0, 0, 0, 2)
            boundingRect.setHeight(min(boundingRect.height(), oldWidth))
            boundingRect.moveTo((oldWidth - boundingRect.width()) / 2,
                                ((oldWidth - boundingRect.height()) / 2) - 1)
            p.setOpacity(0.7)
            p.setBrush(scheme)
            p.setPen(QtGui.QColor('blue'))

            p.setBrush(Qt.NoBrush)
            p.setPen(QtGui.QColor('blue'))
            p.setOpacity(1.0)
            p.drawText(overlayImg.rect(), Qt.AlignCenter, countStr)

            p.end()

            self.setIcon(QtGui.QIcon(overlayImg))

if not Pds.session == pds.Kde4:

    class Tray(QtGui.QSystemTrayIcon, PTray):
        def __init__(self, parent):
            QtGui.QSystemTrayIcon.__init__(self, parent)
            PTray.__init__(self)

            self.appWindow = parent
            self.activated.connect(self.__activated)

        def __activated(self, reason):
            if not reason == QtGui.QSystemTrayIcon.Context:
                if self.appWindow.isVisible():
                    self.appWindow.hide()
                else:
                    self.appWindow.show()

        def initializePopup(self):
            self.setIcon(self.defaultIcon)
            self.actionMenu = QtGui.QMenu(i18n("Update"))
            self.populateRepositoryMenu()
            self.setContextMenu(self.actionMenu)
            self.contextMenu().addSeparator()

        def populateRepositoryMenu(self):
            self.actionMenu.clear()
            for name, address in self.iface.getRepositories():
                self._addAction(name, self.actionMenu)
            self._addAction(i18n("All"), self.actionMenu)

        def showPopup(self):
            if self._ready_to_popup():
                self.showMessage(i18n('Updates'), i18n("There are %1 updates available!", self.unread))

else:

    from PyKDE4.kdeui import KNotification, KSystemTrayIcon, KActionMenu
    from PyKDE4.kdecore import KComponentData

    class Tray(KSystemTrayIcon, PTray):
        def __init__(self, parent):
            KSystemTrayIcon.__init__(self, parent)
            PTray.__init__(self)
            self.appWindow = parent

        def initializePopup(self):
            self.setIcon(self.defaultIcon)
            self.actionMenu = KActionMenu(i18n("Update"), self)
            self.populateRepositoryMenu()
            self.contextMenu().addAction(self.actionMenu)
            self.contextMenu().addSeparator()

        def populateRepositoryMenu(self):
            self.actionMenu.menu().clear()
            for name, address in self.iface.getRepositories():
                self._addAction(name, self.actionMenu)
            self._addAction(i18n("All"), self.actionMenu)

        def showPopup(self):
            if self._ready_to_popup():
                if self.notification:
                    del self.notification
                self.notification = KNotification("Updates")
                self.notification.setText(i18n("There are <b>%1</b> updates available!", self.unread))
                self.notification.setActions(QStringList((i18n("Show Updates"), i18n("Ignore"))))
                self.notification.setFlags(KNotification.Persistent)
                self.notification.setComponentData(KComponentData("package-manager","package-manager"))
                self.connect(self.notification, SIGNAL("action1Activated()"), lambda:self.emit(SIGNAL("showUpdatesSelected()")))
                self.notification.sendEvent()
