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
import sys

from utility import *

LIST_CARDS, CARD_INFO, MONITOR_INFO, SCREEN_INFO, SET_SCREEN = xrange(1, 6)

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
        self.resList = QComboBox(self)
        depthLabel = QLabel(i18n("Color depth:"), self)
        self.depthList = QComboBox(self)

        vb2 = QVBoxLayout(hb, 3, "modeLayout")
        vb2.addWidget(resLabel)
        vb2.addWidget(self.resList)
        vb2.addWidget(depthLabel)
        vb2.addWidget(self.depthList)
        vb2.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.curCard = None
        self.curMonitor = None
        self.curRes = None
        self.curDepth = None
        
        self.monitors = []
        self.res = []
        self.depths = ["16", "24"]


class widgetMain(QWidget):
    def __init__(self, parent):
        self.setupComar()

        QWidget.__init__(self, parent)
        self.setupForm()

        self.nrCards = 0
        self.nrMonitors = 0
        self.cards = []
        self.monitors = {}
            
        for i in "0",  "1":
            self.link.Xorg.Display.screenInfo(screenNumber=i, id=SCREEN_INFO)
        self.link.Xorg.Display.listCards(id=LIST_CARDS)

    def setupComar(self):
        link = comar.Link()
        link.localize()
        self.link = link

        self.link.can_access("Xorg.Display.listCards")
        try:
            reply = self.link.read_cmd()
        except comar.LinkClosed:
            print "Connection closed by COMAR"
            sys.exit(1)

        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)

    def setupForm(self):
        vb = QVBoxLayout(self, 6, 6, "mainLayout")

        label = QLabel(i18n("Desktop setup:"), self)
        desktopSetup = QComboBox(self)
        #desktopSetup.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        desktopSetupButton = QToolButton(self)
        desktopSetupButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        desktopSetupButton.setIconSet(getIconSet("configure.png"))

        hb = QHBoxLayout(vb, 3, "topLayout")
        hb.addWidget(label)
        hb.addWidget(desktopSetup)
        hb.addWidget(desktopSetupButton)

        self.tab = QTabWidget(self)
        scr1 = ScreenWidget(self)
        scr2 = ScreenWidget(self)
        self.tab.addTab(scr1, i18n("Screen &1"))
        self.tab.addTab(scr2, i18n("Screen &2"))
        self.tab.setTabEnabled(scr1, False)
        self.tab.setTabEnabled(scr2, False)
        self.tab.setCurrentPage(0)
        vb.addWidget(self.tab)

        menuButton = QPushButton(i18n("&Menu"), self)
        #okButton = QPushButton(i18n("&OK"), self)
        applyButton = QPushButton(i18n("&Apply"), self)
        #cancelButton = QPushButton(i18n("&Cancel"), self)

        hb = QHBoxLayout(vb, 3, "bottomLayout")
        hb.addWidget(menuButton)
        hb.addItem(QSpacerItem(200, 20))
        #hb.addWidget(okButton)
        hb.addWidget(applyButton)
        #hb.addWidget(cancelButton)
        
        self.connect(scr1.cardList, SIGNAL("activated(int)"), self.slotCardSelected)
        self.connect(scr2.cardList, SIGNAL("activated(int)"), self.slotCardSelected)
        self.connect(scr1.monitorList, SIGNAL("activated(int)"), self.slotMonitorSelected)
        self.connect(scr2.monitorList, SIGNAL("activated(int)"), self.slotMonitorSelected)
        
        self.connect(applyButton, SIGNAL("clicked()"), self.slotApply)
        
    def populatePage(self, scr):
        #self.tab.setTabEnabled(scr, True)
        
        scr.cardList.clear()
        for card in self.cards:
            scr.cardList.insertItem(card.name)
            
        idlist = [x.id for x in self.cards]
        cur = idlist.index(scr.curCard)
        
        scr.cardList.setCurrentItem(cur)
        self.slotCardSelected(cur, scr)
        
        for m in scr.monitors:
            if m.id == scr.curMonitor:
                index = scr.monitors.index(m)
                scr.monitorList.setCurrentItem(index)
                self.slotMonitorSelected(index, scr)
                break
        
        index = scr.res.index(scr.curRes)
        scr.resList.setCurrentItem(index)

        for d in scr.depths:
            if d == "16":
                scr.depthList.insertItem(i18n("High color (16 bit)"))
            else:
                scr.depthList.insertItem(i18n("True color (24 bit)"))
                
        index = scr.depths.index(scr.curDepth)
        scr.depthList.setCurrentItem(index)

        
    def slotCardSelected(self, index, page=None):
        if page:
            scr = page
        else:
            scr = self.tab.currentPage()
        
        card = self.cards[index]
        scr.monitors = card.monitors
        
        scr.monitorList.clear()
        for mon in card.monitors:
            scr.monitorList.insertItem(mon.name)
            
    def slotMonitorSelected(self, index, page=None):
        if page:
            scr = page
        else:
            scr = self.tab.currentPage()
        
        mon = scr.monitors[index]
        scr.res = mon.res

        scr.resList.clear()
        for res in scr.res:
            scr.resList.insertItem(res)

    def slotComar(self, sock):
        reply = self.link.read_cmd()

        if reply.command ==  "result":
            if reply.id == LIST_CARDS:
                cards = reply.data.splitlines()
                for card in cards:
                    cardId, name = card.split(" ", 1)
                    c = Card(cardId, name)
                    self.cards.append(c)
                    scr = self.tab.currentPage()
                    scr.card = c
                    #if cardId == scr.curCard:
                    #    scr.cardList.setCurrentItem(len(self.cards) - 1)
                    self.link.Xorg.Display.cardInfo(cardId=cardId, id=CARD_INFO)
                    
            elif reply.id == CARD_INFO:
                #lines = reply.data.strip().splitlines()
                #cardInfo = dict(x.split("=", 1) for x in lines)
                cardInfo = pairs2dict(reply.data)
                
                card = ""
                for c in self.cards:
                    if c.id == cardInfo["id"]:
                        card = c
                
                self.nrCards += 1
                monitors = cardInfo["monitors"].split(",")
                if not monitors[0]:
                    return
                
                for mon in monitors:
                    #if mon == scr.curMonitor:
                    #    scr.monitor = self.monitors[mon]

                    if self.monitors.has_key(mon):
                        card.monitors.append(self.monitors[mon])
                        continue
                    
                    m = Monitor(mon)
                    card.monitors.append(m)
                    self.monitors[mon] = m

                    self.link.Xorg.Display.monitorInfo(monitorId=mon, id=MONITOR_INFO)
                    
            elif reply.id == MONITOR_INFO:
                #lines = reply.data.strip().splitlines()
                #monInfo = dict(x.split("=", 1) for x in lines)
                monInfo = pairs2dict(reply.data)
                monId = monInfo["id"]
                self.nrMonitors += 1
                
                mon = None
                for card in self.cards:
                    for m in card.monitors:
                        if m.id == monId:
                            mon = m
                            break

                if not mon:
                    return
                
                mon.name = monInfo["modelName"]
                mon.res = monInfo["resolutions"].split(",")
                
                if self.nrMonitors == len(self.monitors):
                    for i in 0, 1:
                        scr = self.tab.page(i)
                        if self.tab.isTabEnabled(scr):
                            self.populatePage(scr)
                
            elif reply.id == SCREEN_INFO:
                if not reply.data:
                    return
                
                #lines = reply.data.strip().splitlines()
                #scrInfo = dict(x.split("=", 1) for x in lines)
                scrInfo = pairs2dict(reply.data)
                scrNum = scrInfo["number"]
                index = int(scrNum)
                
                scr = self.tab.page(index)
                scr.curCard = scrInfo["card"]
                scr.curMonitor = scrInfo["monitor"]
                scr.curRes = scrInfo["resolution"]
                scr.curDepth = scrInfo["depth"]
                
                self.tab.setTabEnabled(scr, True)
            
            elif reply.id == SET_SCREEN:
                pass
                #QMessageBox.information(self,
                #    i18n("Display Configuration"),
                #    i18n("""Your configuration has been saved."""))

                
        elif reply.command == "fail":
            print reply.data
            if reply.id == SCREEN_INFO:
                print reply.data
        
    def slotApply(self):
        for i in 0, 1:
            scr = self.tab.page(i)
            if not self.tab.isTabEnabled(scr):
                continue
            
            card = self.cards[scr.cardList.currentItem()]
            monitor = scr.monitors[scr.monitorList.currentItem()]
            res = scr.res[scr.resList.currentItem()]
            depth = scr.depths[scr.depthList.currentItem()]
            mode = "%s-%s" % (res, depth)
            
            self.link.Xorg.Display.setScreen(screenNumber=str(i),
                                             cardId=card.id,
                                             monitorId=monitor.id,
                                             mode=mode,
                                             id=SET_SCREEN)

    def slotHelp(self):
        help = HelpDialog('display-manager', i18n('Help'), self.parent())
        help.show()
