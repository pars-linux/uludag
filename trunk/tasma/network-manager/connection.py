#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *

import widgets
from icons import getIconSet
from comariface import comlink


class AuthTab(QWidget):
    #remains
    def __init__(self, parent, modes):
        QWidget.__init__(self, parent)
        self.modes = modes
        
        g = QGridLayout(self, 5, 3, 6, 6)
        
        group = QButtonGroup()
        self.group = group
        group.setExclusive(True)
        self.connect(group, SIGNAL("clicked(int)"), self.slotClicked)
        
        r1 = QRadioButton(i18n("No authentication"), self)
        self.r1 = r1
        g.addMultiCellWidget(r1, 0, 0, 0, 2)
        group.insert(r1, 0)
        
        r2 = QRadioButton(i18n("Passphrase:"), self)
        self.r2 = r2
        g.addWidget(r2, 1, 0)
        group.insert(r2, 1)
        
        self.phrase = widgets.Edit(self, True)
        g.addMultiCellWidget(self.phrase, 1, 1, 1, 2)
        
        r3 = QRadioButton(i18n("Login"), self)
        self.r3 = r3
        g.addWidget(r3, 2, 0)
        group.insert(r3, 2)
        
        lab1 = QLabel(i18n("Name:"), self)
        g.addWidget(lab1, 2, 1, Qt.AlignRight)
        
        self.name = widgets.Edit(self)
        g.addWidget(self.name, 2, 2)
        
        lab = QLabel("", self)
        lab.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        g.addWidget(lab, 3, 0)
        
        lab2 = QLabel(i18n("Password:"), self)
        g.addWidget(lab2, 3, 1, Qt.AlignRight)
        
        self.password = widgets.Edit(self, True)
        g.addWidget(self.password, 3, 2)
        
        r4 = QRadioButton(i18n("Key"), self)
        self.r4 = r4
        g.addMultiCellWidget(r4, 4, 4, 0, 2)
        group.insert(r4, 3)
        
        if not "passauth" in modes:
            r2.setEnabled(False)
        if not "loginauth" in modes:
            r3.setEnabled(False)
            lab1.setEnabled(False)
            lab2.setEnabled(False)
        if not "keyauth" in modes:
            r4.setEnabled(False)
        
        self.slotSwitch(0)
    
    def slotClicked(self, id):
        if id == 0:
            self.phrase.setEnabled(False)
            self.name.setEnabled(False)
            self.password.setEnabled(False)
        elif id == 1:
            self.phrase.setEnabled(True)
            self.name.setEnabled(False)
            self.password.setEnabled(False)
        elif id == 2:
            self.phrase.setEnabled(False)
            self.name.setEnabled(True)
            self.password.setEnabled(True)
    
    def slotSwitch(self, id):
        if id == 0:
            self.r1.setChecked(True)
        elif id == 1:
            self.r2.setChecked(True)
        elif id == 2:
            self.r3.setChecked(True)
        elif id == 3:
            self.r4.setChecked(True)
        self.slotClicked(id)


class Settings(QWidget):
    def __init__(self, parent, link, conn, new_conn=None):
        QWidget.__init__(self, parent)
        
        self.link = link
        self.conn = conn
        self.new_conn = new_conn
        
        grid = QGridLayout(self, 2, 2, 6)
        row = 0
        
        # Identification
        lab = QLabel(i18n("Name:"), self)
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        self.name = widgets.Edit(self)
        grid.addWidget(self.name, row, 1)
        row += 1
        
        # Connection
        lab = QLabel(i18n("Device:"), self)
        grid.addWidget(lab, row, 0, Qt.AlignRight)
        hb = QHBox(self)
        hb.setSpacing(3)
        self.device = KActiveLabel("", hb)
        self.devices_but = QPushButton("Select", hb)
        self.devices_but.setEnabled(False)
        self.devices = QPopupMenu()
        self.connect(self.devices, SIGNAL("activated(int)"), self.slotDeviceSelect)
        self.devices_but.setPopup(self.devices)
        grid.addWidget(hb, row, 1)
        row += 1
        
        if "remote" in link.modes:
            lab = QLabel(unicode(link.remote_name), self)
            grid.addWidget(lab, row, 0, Qt.AlignRight)
            if "scan" in link.modes:
                hb = QHBox(self)
                hb.setSpacing(3)
                self.remote = QLineEdit(hb)
                but = QPushButton(getIconSet("find.png", KIcon.Small), i18n("Scan"), hb)
                self.scanpop = self.initScan()
                but.setPopup(self.scanpop)
                grid.addWidget(hb, row, 1)
            else:
                self.remote = QLineEdit(self)
                grid.addWidget(self.remote, row, 1)
            row += 1
        
        # Authentication
        #if "passauth" in link.modes or "loginauth" in link.modes or "keyauth" in link.modes:
        #    line = widgets.HLine(i18n("Authentication"), self)
        #    grid.addMultiCellWidget(line, row, row, 0, 1)
        #    row += 1
        
        # Communication
        if "net" in link.modes:
            row = self.initNet(grid, row)
        
        self.setValues()
        
        comlink.device_hook.append(self.slotDevices)
        comlink.remote_hook.append(self.slotRemotes)
        comlink.queryDevices(link.script)
    
    def cleanup(self):
        comlink.remote_hook.remove(self.slotRemotes)
        comlink.device_hook.remove(self.slotDevices)
    
    def initScan(self):
        pop = QPopupMenu()
        self.connect(pop, SIGNAL("aboutToShow()"), self.slotScan)
        pop.insertItem(QLabel("Scan results:", pop))
        box = QListBox(pop)
        box.setMinimumSize(240, 100)
        pop.insertItem(box)
        self.scan_box = box
        pop.insertItem(i18n("Scan again"))
        pop.insertItem(i18n("Use remote"))
        return pop
    
    def slotScan(self):
        comlink.queryRemotes(self.link.script, self.device_uid)
    
    def slotRemotes(self, script, remotes):
        if self.link.script != script:
            return
        self.scan_box.clear()
        for remote in remotes.split("\n"):
            self.scan_box.insertItem(remote)
    
    def initNet(self, grid, row):
        line = widgets.HLine(i18n("Network"), self)
        grid.addMultiCellWidget(line, row, row, 0, 1)
        row += 1
        
        self.group = QButtonGroup()
        self.connect(self.group, SIGNAL("clicked(int)"), self.slotNetToggle)
        self.r1 = QRadioButton(i18n("Automatic query (DHCP)"), self)
        self.group.insert(self.r1, 1)
        grid.addMultiCellWidget(self.r1, row, row, 0, 1)
        row += 1
        
        self.r2 = QRadioButton(i18n("Manual"), self)
        grid.addWidget(self.r2, row, 0, Qt.AlignTop)
        self.group.insert(self.r2, 0)
        
        box = QWidget(self)
        grid.addWidget(box, row, 1)
        grid2 = QGridLayout(box, 3, 3, 6)
        row += 1
        
        lab = QLabel(i18n("Address:"), box)
        grid2.addWidget(lab, 0, 0, Qt.AlignRight)
        self.address = QLineEdit(box)
        self.connect(self.address, SIGNAL("textChanged(const QString &)"), self.slotAddr)
        grid2.addWidget(self.address, 0, 1)
        self.auto_addr = QCheckBox(i18n("Custom"), box)
        self.connect(self.auto_addr, SIGNAL("clicked()"), self.slotFields)
        grid2.addWidget(self.auto_addr, 0, 2)
        
        lab = QLabel(i18n("Net mask:"), box)
        grid2.addWidget(lab, 1, 0, Qt.AlignRight)
        self.netmask = QLineEdit(box)
        grid2.addWidget(self.netmask, 1, 1)
        
        lab = QLabel(i18n("Gateway:"), box)
        grid2.addWidget(lab, 2, 0, Qt.AlignRight)
        self.gateway = QLineEdit(box)
        grid2.addWidget(self.gateway, 2, 1)
        self.auto_gate = QCheckBox(i18n("Custom"), box)
        self.connect(self.auto_gate, SIGNAL("clicked()"), self.slotFields)
        grid2.addWidget(self.auto_gate, 2, 2)
        
        line = widgets.HLine(i18n("Name servers"), self)
        grid.addMultiCellWidget(line, row, row, 0, 1)
        row += 1
        
        hb = QHBox(self)
        grid.addMultiCellWidget(hb, row, row, 0, 1)
        row += 1
        self.dns_group = QButtonGroup()
        self.dns1 = QRadioButton(i18n("Default"), hb)
        self.dns_group.insert(self.dns1, 0)
        self.dns2 = QRadioButton(i18n("From query"), hb)
        self.dns_group.insert(self.dns2, 1)
        self.dns3 = QRadioButton(i18n("Custom"), hb)
        self.dns_group.insert(self.dns3, 2)
        
        return row
    
    def setValues(self):
        conn = self.conn
        self.device_items = []
        if conn:
            self.name.edit.setText(unicode(conn.name))
            self.device.setText(conn.devname)
            self.device_uid = self.conn.devid
            if "remote" in self.link.modes:
                self.remote.setText(conn.remote)
            if conn.net_mode == "auto":
                self.r1.setChecked(True)
            else:
                self.r2.setChecked(True)
                self.address.setText(conn.net_addr)
                self.netmask.setText(conn.net_mask)
                self.gateway.setText(conn.net_gate)
        else:
            self.name.edit.setText(unicode(comlink.uniqueName()))
            self.device_uid = self.new_conn[0]
            self.device.setText(self.new_conn[1])
            self.r1.setChecked(True)
        self.slotFields()
    
    def useValues(self):
        name = str(self.name.edit.text())
        address = self.address.text()
        netmask = self.netmask.text()
        gateway = self.gateway.text()
        if self.r1.isChecked():
            mode = "auto"
            address = ""
            netmask = ""
            gateway = ""
        else:
            mode = "manual"
        
        conn = self.conn
        script = self.link.script
        
        if conn and conn.name != name:
            comlink.com.Net.Link[script].deleteConnection(name=conn.name)
        
        comlink.com.Net.Link[script].setAddress(name=name, mode=mode, address=address, mask=netmask, gateway=gateway)
        
        if conn == None or self.device_uid != conn.devid:
            comlink.com.Net.Link[script].setConnection(name=name, device=self.device_uid)
        
        if "remote" in self.link.modes:
            remote = self.remote.text()
            if conn == None or remote != self.conn.remote:
                comlink.com.Net.Link[script].setRemote(name=name, remote=remote)
        
        return
        #FIXME: remains
        if "passauth" in self.modes or "loginauth" in self.modes or "keyauth" in self.modes:
            r = self.auth.group.selectedId()
            if r == 0:
                self.comar.call_package("Net.Link.setAuthentication", self.link_name, [
                    "name", name, "user", "", "password", "", "key", "" ], id)
            elif r == 1:
                u1 = unicode(self.auth.phrase.edit.text())
                self.comar.call_package("Net.Link.setAuthentication", self.link_name, [
                    "name", name, "user", "", "password", u1, "key", "" ], id)
            elif r == 2:
                u1 = unicode(self.auth.name.edit.text())
                u2 = unicode(self.auth.password.edit.text())
                self.comar.call_package("Net.Link.setAuthentication", self.link_name, [
                    "name", name, "user", u1, "password", u2, "key", "" ], id)
            elif r == 3:
                # FIXME: key
                pass
    
    def slotDevices(self, script, devices):
        if script != self.link.script:
            return
        self.devices.clear()
        self.device_items = []
        id = 0
        for item in devices.split("\n"):
            uid, info = item.split(" ", 1)
            self.device_items.append((uid, info))
            self.devices.insertItem(info, id)
            id += 1
        if id > 1:
            self.devices_but.setEnabled(True)
    
    def slotDeviceSelect(self, id):
        item = self.device_items[id]
        self.device_uid = item[0]
        self.device.setText(item[1])
    
    def slotFields(self):
        auto = self.group.selectedId()
        addr = self.auto_addr.isChecked()
        gate = self.auto_gate.isChecked()
        self.address.setEnabled(not auto or (auto and addr))
        self.netmask.setEnabled(not auto or (auto and addr))
        self.gateway.setEnabled(not auto or (auto and gate))
        self.auto_addr.setEnabled(auto)
        self.auto_gate.setEnabled(auto)
    
    def slotNetToggle(self, id):
        self.slotFields()
    
    def maskOK(self, mask):
        if mask == "":
            return True
        m = mask.split(".")
        if len(m) != 4:
            return False
        if m[0] != "255":
            return False
        if m[1] != "255" and m[1] != "0":
            return False
        if m[2] != "255" and m[2] != "0":
            return False
        if m[3] != "255" and m[3] != "0":
            return False
        return True
    
    def slotAddr(self, addr):
        addr = unicode(addr)
        mask = self.netmask
        if "." in addr:
            try:
                cl = int(addr.split(".", 1)[0])
            except:
                cl = 0
            m = unicode(mask.text())
            if not self.maskOK(m):
                return
            if cl > 0 and cl < 127:
                mask.setText("255.0.0.0")
            elif cl > 127 and cl < 192:
                mask.setText("255.255.0.0")
            elif cl > 191 and cl < 224:
                mask.setText("255.255.255.0")


class Window(QMainWindow):
    def __init__(self, parent, conn, link=None, new_conn=None):
        QMainWindow.__init__(self, parent)
        
        self.setCaption(i18n("Configure network connection"))
        #self.setMinimumSize(580, 380)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(12)
        self.setCentralWidget(vb)
        
        if not link:
            link = comlink.links[conn.script]
        self.settings = Settings(vb, link, conn, new_conn)
        
        hb = QHBox(vb)
        hb.setSpacing(12)
        lab = QLabel("", hb)
        but = QPushButton(getIconSet("apply.png", KIcon.Small), i18n("Apply"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAccept)
        but = QPushButton(getIconSet("cancel.png", KIcon.Small), i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotCancel)
        
        self.show()
    
    def slotScan(self):
        # FIXME:
        if self.device:
            self.comar.call_package("Net.Link.scanRemote", self.link_name, [ "device", self.device ], id=6)
    
    def slotAccept(self):
        self.settings.useValues()
        self.settings.cleanup()
        self.close(True)
    
    def slotCancel(self):
        self.settings.cleanup()
        self.close(True)
    
    def slotComar(self, sock):
        # remains
        if reply[0] == self.comar.RESULT:
                name, type = reply[2].split("\n", 1)
                if type == "none":
                    self.auth.slotSwitch(0)
                else:
                    type, rest = type.split("\n", 1)
                    if type == "passauth":
                        self.auth.slotSwitch(1)
                        self.auth.phrase.edit.setText(rest)
                    elif type == "loginauth":
                        user, password = rest.split("\n", 1)
                        self.auth.slotSwitch(2)
                        self.auth.name.edit.setText(user)
                        self.auth.password.edit.setText(password)
