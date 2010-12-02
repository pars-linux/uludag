#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
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
import locale

# QT & KDE Modules
from qt import *
from kdecore import *
from kdeui import *
import kdedesigner
from khtml import *

# UI
import firewall
import dialog
import editdialog

# DBus
import comar
import dbus
import dbus.mainloop.qt3


# Rules
import rules

def I18N_NOOP(str):
    return str

description = I18N_NOOP('Pardus Firewall Graphical User Interface')
version = '2.0.7'

def AboutData():
    global version, description

    about_data = KAboutData('firewall-config',
                            'Firewall Configuration',
                            version,
                            description,
                            KAboutData.License_GPL,
                            '(C) 2006 UEKAE/TÜBİTAK',
                            None, None,
                            'bahadir@pardus.org.tr')

    about_data.addAuthor('Bahadır Kandemir', None, 'bahadir@pardus.org.tr')
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

class FWListViewItem(QListViewItem):
    def __init__(self, parent, after=None, label='', ports='', isDefault=False, isRunning=False):
        QListViewItem.__init__(self, parent, after, label)
        self.ports = ports
        self.isDefault = isDefault
        self.isRunning = isRunning

    def paintCell(self, p, cg, column, width, align):
        cg = QColorGroup(cg)
        if self.isDefault:
            pp = p.font()
            pp.setWeight(QFont.Bold)
            p.setFont(pp)
            QListViewItem.paintCell(self, p, cg, column, width,align)
        else:
            QListViewItem.paintCell(self, p, cg, column, width,align)

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        lang = locale.setlocale(locale.LC_MESSAGES)
        if "_" in lang:
            lang = lang.split("_", 1)[0]
        url = locate("data", "%s/help/%s/main_help.html" % (name, lang))
        if not os.path.exists(url):
            url = locate("data", "%s/help/en/main_help.html" % name)
        self.htmlPart.openURL(KURL(url))

def checkPortFormat(ports):
    '''Check multiport format'''
    if ports.count(',') + ports.count('-') > 15:
        return False
    for port in ports.split(','):
        grp = port.split('-')
        if len(grp) > 2:
            return False
        for p in grp:
            if not p.isdigit() or p.startswith("0") or 0 > int(p) or int(p) > 65535:
                return False
    return True

class dialogRule(dialog.dialogRule):
    def __init__(self, parent=None, name=None, caption=i18n("Firewall Configuration"), ports=''):
        dialog.dialogRule.__init__(self, parent, name)

        self.connect(self.pushCancel, SIGNAL('clicked()'), self, SLOT('reject()'))
        self.connect(self.pushOK, SIGNAL('clicked()'), SLOT('accept()'))

        # Load icons for buttons
        self.pushCancel.setIconSet(loadIconSet('cancel', group=KIcon.Small))
        self.pushOK.setIconSet(loadIconSet('ok', group=KIcon.Small))

        self.linePorts.setText(ports.replace(':', '-'))
        self.setCaption(caption)

    def accept(self):
        if checkPortFormat(str(self.linePorts.text())):
            dialog.dialogRule.accept(self)
        else:
            KMessageBox.sorry(self, i18n('Invalid port range.'), i18n('Error'))

    def exec_loop(self):
        if dialog.dialogRule.exec_loop(self):
            ports = self.linePorts.text().replace('-', ':')
            ports = ports.replace(' ', '')

            return ports
        else:
            return False

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

        mainwidget = firewall.MainWindow(self)
        toplayout = QVBoxLayout(self, 0, KDialog.spacingHint())
        toplayout.addWidget(mainwidget)

        self.aboutus = KAboutApplication(self)

        # Initial conditions
        self.state = 'off'
        mainwidget.pushStatus.setEnabled(False)

        if not standalone:
            mainwidget.groupButtons.hide()

        # Icons
        self.setIcon(loadIcon('firewall_config', size=48))
        mainwidget.pixmapFW.setPixmap(loadIcon('firewall_config', size=48))
        mainwidget.pixmapIncoming.setPixmap(loadIcon('server.png', size=48))
        mainwidget.pixmapAdvanced.setPixmap(loadIcon('gear.png', size=48))
        mainwidget.pushNewRule.setPixmap(loadIcon('add.png', size=32))
        mainwidget.deleteRule.setPixmap(loadIcon('cancel.png', size=32))
        mainwidget.editRule.setPixmap(loadIcon('configure.png', size=32))
        mainwidget.startStop.setPixmap(loadIcon('player_play.png', size=32))

        mainwidget.pushOk.setIconSet(loadIconSet('ok', group=KIcon.Small))
        mainwidget.pushCancel.setIconSet(loadIconSet('cancel', group=KIcon.Small))
        mainwidget.pushHelp.setIconSet(loadIconSet('help', group=KIcon.Small))
        mainwidget.pushApply.setIconSet(loadIconSet('apply', group=KIcon.Small))

        # COMAR
        self.link = comar.Link()
        self.link.setLocale()
        self.link.listenSignals("Network.Firewall", self.handleSignals)
        self.link.listenSignals("System.Service", self.handleSignals)

        # Signals
        self.connect(mainwidget.pushStatus, SIGNAL('clicked()'), self.slotStatus)
        self.connect(mainwidget.pushCancel, SIGNAL('clicked()'), self, SLOT('close()'))
        self.connect(mainwidget.pushOk, SIGNAL('clicked()'), self.slotOk)
        self.connect(mainwidget.pushApply, SIGNAL('clicked()'), self.slotApply)
        self.connect(mainwidget.pushNewRule, SIGNAL('clicked()'), self.slotDialog)
        self.connect(mainwidget.deleteRule, SIGNAL('clicked()'), self.slotDelete)
        self.connect(mainwidget.editRule, SIGNAL('clicked()'), self.slotEdit)
        self.connect(mainwidget.startStop, SIGNAL('clicked()'), self.slotStartStop)
        self.connect(mainwidget.pushHelp, SIGNAL('clicked()'), self.slotHelp)
        self.connect(mainwidget.outgoingRuleList, SIGNAL('selectionChanged()'), self.slotUpdateRuleListState)
        self.connect(mainwidget.incomingRuleList, SIGNAL('selectionChanged()'), self.slotUpdateRuleListState)

        # Init
        self.getState()

        # List initialization
        mainwidget.outgoingRuleList.header().hide()
        mainwidget.outgoingRuleList.setSorting(-1)
        mainwidget.incomingRuleList.header().hide()
        mainwidget.incomingRuleList.setSorting(-1)

    def handleSignals(self, package, signal, args):
        pass

    def slotChanged(self):
        if not standalone:
            self.changed()
        return

    def getState(self):
        def handleState(package, exception, args):
            _state = args[0]
            self.state = "off"
            mainwidget.pushStatus.setEnabled(True)
            if _state  == "on":
                self.state = "on"
                self.getRules()
            self.setState(self.state)
        self.link.Network.Firewall["iptables"].getState(async=handleState)

    def handleList(self, list, ports):
        """
        Takes a qlistview and a port list. Firstly, adds defualt ports to the given list. Then iterates over 
        the port list and if a port value in the list belongs a default service port, which is defined by firewall-config,
        sets its running status and icon. Otherwise, adds a qlistviewitem for that port to the given qlistview.
        """
        list.clear()
        runningList = {}
        for _key, (_name, _ports) in rules.filter.iteritems():
            msg = i18n(_name) + " [ " + unicode(i18n("Ports: %s")) % _ports + " ]"
            lvi = FWListViewItem(list, None, msg, _ports, True)
            lvi.setPixmap(0, loadIcon('applications-other.png', size=24));
            runningList[_key] = lvi
        for port in ports:
            key = self.checkDefault(port)
            if not key == '':
                # this is default item, just edit
                lvi = runningList[key]
                if not lvi.isRunning:
                    lvi.setPixmap(0, loadIcon('gear.png', size=24))
                    lvi.isRunning = True
            else:
                # add custom item to end of the list
                self.addItemToRuleList(list, port)


    def getRules(self):
        # Note: If the firewall is running at the start this function executes two times.
        # So that in the handleList method, list is cleared at first.
        def handleIncoming(package, exception, args):
            if exception:
                return
            ports = args[0].get("port_exceptions", "").split()
            self.handleList(mainwidget.incomingRuleList, ports)
        self.link.Network.Firewall["iptables"].getModuleParameters("block_incoming", async=handleIncoming)

        def handleOutgoing(package, exception, args):
            if exception:
                return
            ports = args[0].get("port_exceptions", "").split() 
            self.handleList(mainwidget.outgoingRuleList, ports)
        self.link.Network.Firewall["iptables"].getModuleParameters("block_outgoing", async=handleOutgoing)

    def addItemToRuleList(self, list, port):
        """
        Adds a list view item to end of the given list with port value
        """
        if list == mainwidget.incomingRuleList:
            msg = i18n('Allow all incoming connection through port(s) %s')
        else:
            msg = i18n('Reject all outgoing connection through port(s) %s')
        msg = msg.replace('%s', port.replace(':', '-'))
        lvi = FWListViewItem(list, list.lastItem(), msg, port)
        lvi.setPixmap(0, loadIcon('gear.png', size=24));

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
            mainwidget.pushStatus.setText(i18n('&Stop Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(41, 182, 31))
            mainwidget.textStatus2.setText(i18n('Click here to stop the firewall and allow all incoming and outgoing connections.'))

            # Load FW rules
            self.getRules()
        else:
            mainwidget.pushStatus.setText(i18n('&Start Firewall'))
            mainwidget.textStatus.setText(i18n('<b><font size=\'+1\'>Firewall is not running</font></b>'))
            mainwidget.textStatus.setPaletteForegroundColor(QColor(182, 41, 31))
            mainwidget.textStatus2.setText(i18n('Click here to start the firewall and allow connections only to specified services.'))
        self.updateRules()

    def updateRules(self):
        if self.state == 'on':
            mainwidget.outgoingRuleList.setEnabled(True)
            mainwidget.pushNewRule.setEnabled(True)
            mainwidget.deleteRule.setEnabled(False)
            mainwidget.editRule.setEnabled(False)
            mainwidget.startStop.setEnabled(False)
            mainwidget.incomingRuleList.setEnabled(True)
        else:
            mainwidget.outgoingRuleList.setEnabled(False)
            mainwidget.outgoingRuleList.clear()
            mainwidget.pushNewRule.setEnabled(False)
            mainwidget.deleteRule.setEnabled(False)
            mainwidget.editRule.setEnabled(False)
            mainwidget.startStop.setEnabled(False)
            mainwidget.incomingRuleList.setEnabled(False)
            mainwidget.incomingRuleList.clear()

    def slotStatus(self):
        mainwidget.pushStatus.setEnabled(False)
        if self.state == 'on':
            def handleState(package, exception, args):
                if exception:
                    self.setState("on")
                    mainwidget.pushStatus.setEnabled(True)
                else:
                    self.setState("off")
                    mainwidget.pushStatus.setEnabled(True)
                    self.link.Network.Firewall["iptables"].setModuleState("block_incoming", "off")
                    self.link.Network.Firewall["iptables"].setModuleState("block_outgoing", "off")

            self.link.Network.Firewall["iptables"].setState("off", async=handleState)
        else:
            def handleState(package, exception, args):
                if exception:
                    self.setState("off")
                    mainwidget.pushStatus.setEnabled(True)
                else:
                    self.setState("on")
                    mainwidget.pushStatus.setEnabled(True)
                    self.link.Network.Firewall["iptables"].setModuleState("block_incoming", "on")
                    self.link.Network.Firewall["iptables"].setModuleState("block_outgoing", "on")

            self.link.Network.Firewall["iptables"].setState("on", async=handleState)

    def slotOk(self):
        self.saveAll()
        self.close()

    def slotApply(self):
        self.saveAll()

    def slotEdit(self):
        """
        Executes when an edit button clicked. Firstly decides which list will be used and shows an
        edit dialog to the user. Stores the changed value in the list if the user changes something.
        """
        if mainwidget.tabWidget.currentPageIndex() == 0:
            list = mainwidget.incomingRuleList
        else:
            list = mainwidget.outgoingRuleList
        item = list.selectedItem()
        if item:
            dialog = dialogRule(mainwidget, caption=i18n("Edit Rule"), ports=item.ports)
            ports = dialog.exec_loop()
            if ports: # if the user clicks cancel loop returns boolean-false
                item.ports = str(ports)
                if list == mainwidget.incomingRuleList:
                    msg = i18n('Allow all incoming connection through port(s) %s')
                else:
                    msg = i18n('Reject all outgoing connection through port(s) %s')
                msg = msg.replace('%s', ports.replace(':', '-'))
                item.setText(0, msg)
                KMessageBox.information(self, i18n("Changes are written but will not be saved until you aplly them."))
                if not standalone:
                    self.changed()

    def slotDialog(self):
        dialog = dialogRule(mainwidget, caption=i18n("New Rule"), ports='')
        ports = dialog.exec_loop()
        if ports:
            ports = str(ports)
            if mainwidget.tabWidget.currentPageIndex() == 0:
                list = mainwidget.incomingRuleList
            else:
                list = mainwidget.outgoingRuleList
            item = self.checkExistence(list, ports)
            if not item:
                self.addItemToRuleList(list, ports)
                if not standalone:
                    self.changed()
            else:
                list.setSelected(item, True)
                KMessageBox.sorry(self, i18n('Port is already in list.'), i18n('Error'))

    def checkExistence(self, list, ports):
        """
        Checks wheter the given port is in the given list.
        """
        it = QListViewItemIterator(list)
        item = it.current()
        while item:
            if item.ports == ports:
                return item
            it += 1
            item = it.current()
        return None

    def slotDelete(self):
        """
        Removes the selected item from the list. List is determined from the sender widget.
        """
        if mainwidget.tabWidget.currentPageIndex() == 0:
            list = mainwidget.incomingRuleList
        else:
            list = mainwidget.outgoingRuleList
        item = list.selectedItem()
        if item:
            list.takeItem(item)
            KMessageBox.information(self, i18n("Changes are written but will not be saved until you aplly them."))
            if not standalone:
                self.changed()

    def slotStartStop(self):
        """
        Gets the selected default port from the list and starts or stops them according to their running status.
        """
        if mainwidget.tabWidget.currentPageIndex() == 0:
            list = mainwidget.incomingRuleList
        else:
            list = mainwidget.outgoingRuleList
        item = list.selectedItem()
        if not item.isRunning:
            item.isRunning = True
            mainwidget.startStop.setPixmap(loadIcon('player_stop.png', size=32))
            item.setPixmap(0, loadIcon('gear.png', size=24));
        else:
            item.isRunning = False
            mainwidget.startStop.setPixmap(loadIcon('player_play.png', size=32))
            item.setPixmap(0, loadIcon('applications-other.png', size=24));
        if not standalone:
            self.changed()
        KMessageBox.information(self, i18n("Changes are written but will not be saved until you aplly them."))

    def slotUpdateRuleListState(self):
        """
        Triggered when outgoing rule list's selection changed. Determines the buttons' status wheter they are enabled.
        Default ports can't be edited or deleted but they can be started or stopped. Custom ports can be
        edited or removed.
        """
        if mainwidget.tabWidget.currentPageIndex() == 0:
            item = mainwidget.incomingRuleList.selectedItem()
        else:
            item = mainwidget.outgoingRuleList.selectedItem()
        if item:
            if item.isDefault:
                mainwidget.deleteRule.setEnabled(False)
                mainwidget.editRule.setEnabled(False)
                mainwidget.startStop.setEnabled(True)
                if item.isRunning:
                    mainwidget.startStop.setPixmap(loadIcon('player_stop.png', size=32))
                else:
                    mainwidget.startStop.setPixmap(loadIcon('player_play.png', size=32))
            else:
                mainwidget.deleteRule.setEnabled(True)
                mainwidget.editRule.setEnabled(True)
                mainwidget.startStop.setEnabled(False)
        else:
            mainwidget.deleteRule.setEnabled(False)
            mainwidget.editRule.setEnabled(False)
            mainwidget.startStop.setEnabled(False)

    def slotHelp(self):
        help = HelpDialog("firewall-config", i18n("Firewall Manager Help"), self)
        help.show()

    def setRule(self, table, rule):
        rule = '-t %s %s' % (table, rule)
        self.link.Net.Filter["iptables"].setRule(rule)

    def listPorts(self, list):
        """
        Stores the port values of the qlistitems in a python list for the given qlistview and returns this python port list.
        """
        ports = []
        it = QListViewItemIterator(list)
        item = it.current()
        while item:
            if item.isDefault:
                if item.isRunning:
                    ports.append(item.ports)
            else:
                ports.append(item.ports)
            it += 1
            item = it.current()
        return ports

    def saveAll(self):
        try:
            # Tab 1 - Incoming Connections
            ports = self.listPorts(mainwidget.incomingRuleList)
            self.link.Network.Firewall["iptables"].setModuleParameters("block_incoming", {"port_exceptions": " ".join(ports)})

            # Tab 2 - Advanced
            ports = self.listPorts(mainwidget.outgoingRuleList)
            self.link.Network.Firewall["iptables"].setModuleParameters("block_outgoing", {"port_exceptions": " ".join(ports)})
        except:
            pass

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
