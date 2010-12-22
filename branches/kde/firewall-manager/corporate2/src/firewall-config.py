#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

# Python Modules
import os
import re
import sys
import time

# QT & KDE Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner

# UI
#import firewall

# DBus
import comar
import dbus
import dbus.mainloop.qt3

from handler import CallHandler
from utils import *

# Rules
import rules

def I18N_NOOP(str):
    return str

description = I18N_NOOP('Pardus Firewall Graphical User Interface')
version = '2.1.0'

def AboutData():
    global version, description

    about_data = KAboutData('firewall-config',
                            'Firewall Configuration',
                            version,
                            description,
                            KAboutData.License_GPL,
                            '(C) 2006-2010 UEKAE/TÜBİTAK',
                            None, None,
                            'info@pardus.org.tr')

    about_data.addAuthor('Bahadır Kandemir', None, 'bahadir@pardus.org.tr')
    about_data.addAuthor('Mehmet Özdemir', None, 'mehmet@pardus.org.tr')
    about_data.addCredit('Görkem Çetin', I18N_NOOP('GUI Design & Usability'), 'gorkem@pardus.org.tr')
    about_data.addCredit('İsmail Dönmez', I18N_NOOP('Help with IPTables'), 'ismail@pardus.org.tr')
    about_data.addCredit('Gürer Özen', I18N_NOOP('Help with KDE stuff'), 'gurer@pardus.org.tr')

    return about_data

def loadIcon(name, group=KIcon.Desktop, size=16):
    return KGlobal.iconLoader().loadIcon(name, group, size)

def loadIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group, 0, False)

# Are we running as a separate standalone application or in KControl?
standalone = __name__ == '__main__'

if standalone:
    programbase = QDialog
else:
    programbase = KCModule

class MainApplication(programbase):
    def __init__(self, parent=None, name=None):
        global standalone
        global mainwidget
        global logwin

        if standalone:
            QDialog.__init__(self,parent,name)
            self.setCaption(i18n('Firewall Configuration'))
        else:
            KCModule.__init__(self,parent,name)
            KGlobal.locale().insertCatalogue('firewall_config')
            # Create a configuration object.
            self.config = KConfig('firewall_config')
            self.aboutdata = AboutData()
            self.setButtons(KCModule.Help | KCModule.Apply)

        # The appdir needs to be explicitly otherwise we won't be able to
        # load our icons and images.
        KGlobal.iconLoader().addAppDir('firewall_config')

        #mainwidget = firewall.MainWindow(self)
        mainLayout = QGridLayout(self, 4, 4, 4, 4)
        #toplayout = QVBoxLayout(firewall.MainWindow(self), 0, KDialog.spacingHint())
        #toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)

        # Tab 1 - Incoming Connections
        self.incoming = []
        #mainwidget.frameIncoming.setColumnLayout(0, Qt.Vertical)
        #frameIncomingLayout = QVBoxLayout(mainwidget.frameIncoming.layout())
        #frameIncomingLayout.setAlignment(Qt.AlignTop)

        # Tab 2 - Advanced
        self.advanced = []
        #mainwidget.frameAdvanced.setColumnLayout(0, Qt.Vertical)
        #mainwidget.frameAdvanced = EntryView(mainwidget.tabWidget)
        #mainwidget.frameAdvancedLayout = QVBoxLayout(mainwidget.frameAdvanced.layout())
        #mainwidget.frameAdvancedLayout.setAlignment(Qt.AlignTop)

        self.headGroup = QGroupBox(self, "headgroup")
        self.headGroup.setColumnLayout(0,Qt.Vertical)
        self.headGroup.layout().setSpacing(6)
        self.headGroup.layout().setMargin(11)
        self.headGroup.setFrameShape(QButtonGroup.NoFrame)

        self.sl = QHBoxLayout(self.headGroup.layout())
        self.sl.setAlignment(Qt.AlignTop)

        self.headlayout = QHBoxLayout(None, 0, 6, "qhbox")
        mainLayout.addMultiCellWidget(self.headGroup, 0, 0, 0, 3)

        self.sl.addLayout(self.headlayout)

        self.pixmapFW = QLabel(self.headGroup, "pixmapFW")
        self.headlayout.addWidget(self.pixmapFW)

        vLay = QVBoxLayout(None,0,6,"layout6")

        self.textStatus = QLabel(self.headGroup, "textStatus")
        font = self.textStatus.font()
        font.setPointSize(14)
        self.textStatus.setFont(font)
        vLay.addWidget(self.textStatus)

        self.txinfo = QLabel(self.headGroup, "txinfo")
        vLay.addWidget(self.txinfo)

        self.headlayout.addLayout(vLay)

        spacer = QSpacerItem(100, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.headlayout.addItem(spacer)

        self.pushStatus = QPushButton(self.headGroup, "pushStatus")
        self.headlayout.addWidget(self.pushStatus)
        self.pushStatus.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Preferred,0,0,self.pushStatus.sizePolicy().hasHeightForWidth()))

        self.hrline = QFrame(self,"hrline")
        self.hrline.setFrameShape(QFrame.HLine)
        self.hrline.setFrameShadow(QFrame.Sunken)
        self.hrline.setFrameShape(QFrame.HLine)
        mainLayout.addMultiCellWidget(self.hrline, 1, 1, 0, 3)

        self.toplayout = QHBoxLayout(None, 0, 6, "qtbox")
        mainLayout.addMultiCell(self.toplayout, 2, 2, 0, 3)

        self.rulePopup = QPopupMenu(self)
        self.rulePopup.insertItem(i18n("Incoming Rule"), self.slotAddIncoming)
        self.rulePopup.insertItem(i18n("Outgoing Rule"), self.slotAddOutgoing)

        self.newRule = QPushButton(self, "NewRuleButton")
        self.newRule.setText(i18n("New Rule"))
        self.newRule.setPopup(self.rulePopup)
        self.toplayout.addWidget(self.newRule)

        spacer = QSpacerItem(100, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.toplayout.addItem(spacer)

        self.filterCombo = QComboBox(self)
        self.filterCombo.insertItem(i18n("Incoming Connections"))
        self.filterCombo.insertItem(i18n("Outgoing Connections"))
        self.toplayout.addWidget(self.filterCombo)

        self.inev = EntryView(self)
        self.inev.setEnabled(True)
        mainLayout.addMultiCellWidget(self.inev, 3, 3, 0, 3)

        self.bottomlayout = QHBoxLayout(None, 0, 6, "qtbox")
        mainLayout.addMultiCell(self.bottomlayout, 4, 4, 0, 3)

        self.pushHelp = QPushButton(self, "pushHelp")
        self.bottomlayout.addWidget(self.pushHelp)

        spacer = QSpacerItem(100, 1, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bottomlayout.addItem(spacer)

        # Initial conditions
        self.state = 'off'
        self.pushStatus.setEnabled(False)

        # Icons
        self.setIcon(loadIcon('firewall_config', size=48))

        self.pushHelp.setIconSet(loadIconSet('help', group=KIcon.Small))

        # COMAR
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("Network.Firewall", self.handleSignals)
        self.link.listenSignals("System.Service", self.handleSignals)

        # Signals
        self.connect(self.pushStatus, SIGNAL('clicked()'), self.slotStatus)
        self.connect(self.pushHelp, SIGNAL('clicked()'), self.slotHelp)
        self.connect(self.filterCombo, SIGNAL("activated(int)"), self.slotFilterChanged)

        # Init
        self.getState()

        if standalone:
            self.pushClose = QPushButton(self, "pushClose")
            self.pushClose.setText(i18n("Close"))
            self.bottomlayout.addWidget(self.pushClose)
            self.pushClose.setIconSet(loadIconSet('cancel', group=KIcon.Small))
            self.connect(self.pushClose, SIGNAL('clicked()'), self, SLOT('close()'))

    def handleSignals(self, package, signal, args):
        pass

    def slotChanged(self):
        if not standalone:
            self.changed()
        return

    def slotAddIncoming(self):
        if self.filterCombo.currentItem() == 1:
            self.filterCombo.setCurrentItem(0)
            self.getIncomingRules()
        ports = self.askPorts(unicode(i18n("Write ports or port ranges that you want to ALLOW for incoming connections.")))
        if ports:
            if not self.inev.checkItem(ports):
                item = self.inev.add("", ports, -1, False, True, True, "")
                try:
                    self.saveAll()
                    self.refreshView()
                except:
                    self.inev.delete(item)
            else:
                KMessageBox.information(self, unicode(i18n("%s already in list!")) % ports)

    def slotAddOutgoing(self):
        if self.filterCombo.currentItem() == 0:
            self.filterCombo.setCurrentItem(1)
            self.getOutgoingRules()
        ports = self.askPorts(unicode(i18n("Write ports or port ranges that you want to BLOCK for outgoing connections.")))
        if ports:
            if not self.inev.checkItem(ports):
                item = self.inev.add("", ports, -1, False, True, False, "")
                try:
                    self.saveAll()
                    self.refreshView()
                except:
                    self.inev.delete(item)
            else:
                KMessageBox.information(self, unicode(i18n("%s already in list!")) % ports)

    def listIncomingRules(self):
        pass

    def listOutgoingRules(self):
        pass

    def slotFilterChanged(self, index):
        if index < 0:
            return
        if index == 0:
            self.getIncomingRules()
        else:
            self.getOutgoingRules()

    def slotHelp(self):
        if 1:
            return
        help = HelpDialog("firewall-config", i18n("Firewall Manager Help"), self)
        help.show()

    def getState(self):
        """
        Executes only at init
        """
        def handleState(package, exception, args):
            _state = args[0]
            self.state = "off"
            self.pushStatus.setEnabled(True)
            if _state  == "on":
                self.state = "on"
                self.getIncomingRules()
            self.setState(self.state)
        self.link.Network.Firewall["iptables"].getState(async=handleState)

    def handleList(self, ports, isIncoming):
        self.inev.clear()
        runningList = {}
        index = 0
        for _key, (_name, _ports) in rules.filter.iteritems():
            item = self.inev.add("", _ports, index, True, False, isIncoming, _name)
            runningList[_key] = item
            index = index + 1
        for port in ports:
            key = self.checkDefault(port)
            if not key == '':
                # this is default item, just edit
                item = runningList[key]
                item.setIsRunning(True)
            else:
                item = self.inev.add("", port, index, False, True, isIncoming, "")
            index = index + 1

    def getIncomingRules(self):
        def handleIncoming(package, exception, args):
            if exception:
                return
            ports = args[0].get("port_exceptions", "").split()
            self.handleList(ports, True)
        self.link.Network.Firewall["iptables"].getModuleParameters("block_incoming", async=handleIncoming)

    def getOutgoingRules(self):
        def handleOutgoing(package, exception, args):
            if exception:
                return
            ports = args[0].get("port_exceptions", "").split()
            self.handleList(ports, False)
        self.link.Network.Firewall["iptables"].getModuleParameters("block_outgoing", async=handleOutgoing)

    def checkDefault(self, ports):
        """
        Checks the given ports if they are default or not.
        If finds a default port returns the key name of it such as 'inMail'
        """
        for _key, (_name, _ports) in rules.filter.iteritems():
            if _key.startswith('in') and not _ports.find(ports) == -1:
                return _key
        return ''

    def setState(self, state):
        self.state = state
        if self.state == 'on': #and self.profile == rules.profile:
            self.pushStatus.setText(i18n('&Stop'))
            self.pixmapFW.setPixmap(loadIcon('fw-locked', size=48))
            self.textStatus.setText(i18n('Firewall is running'))
            self.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            self.txinfo.setText(i18n('Click here to stop the firewall and allow all incoming and outgoing connections.'))

            # Load FW rules
            #self.getRules()
        else:
            self.pushStatus.setText(i18n('&Start'))
            self.pixmapFW.setPixmap(loadIcon('fw-unlocked', size=48))
            self.textStatus.setText(i18n('Firewall is not running'))
            self.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            self.txinfo.setText(i18n('Click here to start the firewall and allow connections only to specified services.'))
        self.updateRules()

    def updateRules(self):
        if self.state == 'on':
            self.inev.setEnabled(True)
            self.newRule.setEnabled(True)
            self.filterCombo.setEnabled(True)
        else:
            self.inev.setEnabled(False)
            self.newRule.setEnabled(False)
            self.filterCombo.setEnabled(False)

    def slotStatus(self):
        self.pushStatus.setEnabled(False)
        if self.state == 'on':
            def handleState(package, exception, args):
                if exception:
                    self.setState("on")
                    self.pushStatus.setEnabled(True)
                else:
                    self.setState("off")
                    self.pushStatus.setEnabled(True)
                    self.link.Network.Firewall["iptables"].setModuleState("block_incoming", "off")
                    self.link.Network.Firewall["iptables"].setModuleState("block_outgoing", "off")

            self.link.Network.Firewall["iptables"].setState("off", async=handleState)
        else:
            def handleState(package, exception, args):
                if exception:
                    self.setState("off")
                    self.pushStatus.setEnabled(True)
                else:
                    self.refreshView()
                    self.setState("on")
                    self.pushStatus.setEnabled(True)
                    self.link.Network.Firewall["iptables"].setModuleState("block_incoming", "on")
                    self.link.Network.Firewall["iptables"].setModuleState("block_outgoing", "on")

            self.link.Network.Firewall["iptables"].setState("on", async=handleState)

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def askPorts(self, description):
        dialog = dialogRule(self, title=i18n("New Rule"), description=description)
        ports = dialog.exec_loop()
        if ports:
            ports = str(ports)
            if not standalone:
                self.changed()
            ports = ports.replace(',', ' ')
            return ports
        return None

    def setRule(self, table, rule):
        rule = '-t %s %s' % (table, rule)
        self.link.Net.Filter["iptables"].setRule(rule)

    def refreshView(self):
        if self.filterCombo.currentItem() == 0:
            self.getIncomingRules()
        else:
            self.getOutgoingRules()

    def saveAll(self):
        if self.filterCombo.currentItem() == 0:
            ports = self.inev.getPorts()
            try:
                self.link.Network.Firewall["iptables"].setModuleParameters("block_incoming", {"port_exceptions": " ".join(ports)})
            except:
                raise

        if self.filterCombo.currentItem() == 1:
            ports = self.inev.getPorts()
            try:
                self.link.Network.Firewall["iptables"].setModuleParameters("block_outgoing", {"port_exceptions": " ".join(ports)})
            except:
                raise

    def __del__(self):
        pass

    def exec_loop(self):
        global programbase
        programbase.exec_loop(self)

    # KControl virtual void methods
    def load(self):
        pass

    def save(self):
        self.saveAll()

    def defaults(self):
        pass

    def sysdefaults(self):
        pass

    def aboutData(self):
        # Return the KAboutData object which we created during initialisation.
        return self.aboutdata

# This is the entry point used when running this module outside of kcontrol.
def main():
    global kapp

    dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)

    about_data = AboutData()
    KCmdLineArgs.init(sys.argv, about_data)

    if not KUniqueApplication.start():
        print i18n('Pardus Firewall Interface is already running!')
        return

    kapp = KUniqueApplication(True, True, True)
    myapp = MainApplication()
    myapp.resize(QSize(600, 500).expandedTo(myapp.minimumSizeHint()))
    kapp.setMainWidget(myapp)
    sys.exit(myapp.exec_loop())

# Factory function for KControl
def create_firewall_config(parent,name):
    global kapp

    kapp = KApplication.kApplication()
    if not dbus.get_default_main_loop():
        dbus.mainloop.qt3.DBusQtMainLoop(set_as_default=True)
    return MainApplication(parent, name)

if standalone:
    main()
