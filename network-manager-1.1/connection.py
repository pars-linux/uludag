#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import i18n
from links import links
import widgets
import comar
import csapi


class AuthTab(QWidget):
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


class Address(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        
        widgets.HLine(i18n("Network:"), self)
        
        box = QWidget(self)
        g = QGridLayout(box, 4, 2, 6)
        
        group = QButtonGroup()
        self.group = group
        group.setExclusive(True)
        self.connect(group, SIGNAL("clicked(int)"), self.slotClicked)
        
        self.r1 = QRadioButton(i18n("Automatic query (DHCP)"), box)
        g.addMultiCellWidget(self.r1, 0, 0, 0, 2)
        group.insert(self.r1, 0)
        
        self.r2 = QRadioButton(i18n("Manual"), box)
        g.addWidget(self.r2, 1, 0)
        group.insert(self.r2, 1)
        
        lab = QLabel(i18n("Address:"), box)
        g.addWidget(lab, 1, 1, Qt.AlignRight)
        self.address = widgets.Edit(box)
        self.connect(self.address.edit, SIGNAL("textChanged(const QString &)"), self.slotMask)
        g.addWidget(self.address, 1, 2)
        
        lab = QLabel(i18n("Net mask:"), box)
        g.addWidget(lab, 2, 1, Qt.AlignRight)
        self.netmask = widgets.Edit(box)
        g.addWidget(self.netmask, 2, 2)
        
        lab = QLabel(i18n("Gateway:"), box)
        g.addWidget(lab, 3, 1, Qt.AlignRight)
        self.gateway = widgets.Edit(box)
        g.addWidget(self.gateway, 3, 2)
        
        self.slotSwitch("auto")
    
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
    
    def slotMask(self, addr):
        addr = unicode(addr)
        mask = self.netmask.edit
        if "." in addr:
            cl = csapi.atoi(addr.split(".", 1)[0])
            m = unicode(mask.text())
            if not self.maskOK(m):
                return
            if cl > 0 and cl < 127:
                mask.setText("255.0.0.0")
            elif cl > 127 and cl < 192:
                mask.setText("255.255.0.0")
            elif cl > 191 and cl < 224:
                mask.setText("255.255.255.0")
    
    def slotClicked(self, id):
        if id == 0:
            self.address.setEnabled(False)
            self.gateway.setEnabled(False)
            self.netmask.setEnabled(False)
        elif id == 1:
            self.address.setEnabled(True)
            self.gateway.setEnabled(True)
            self.netmask.setEnabled(True)
    
    def slotSwitch(self, mode):
        if mode == "manual":
            self.r2.setChecked(True)
            self.slotClicked(1)
        else:
            self.r1.setChecked(True)
            self.slotClicked(0)


class Device(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        
        widgets.HLine(i18n("Device:"), self)
        
        box = QWidget(self)
        g = QGridLayout(box, 2, 2, 6)
        g.setColStretch(0, 1)
        g.setColStretch(1, 10)
        
        lab = QLabel(i18n("Device:"), box)
        lab.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        g.addWidget(lab, 0, 0)
        self.device = QComboBox(False, box)
        self.device.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        g.addWidget(self.device, 0, 1)
        
        self.remote_label = QLabel("", box)
        g.addWidget(self.remote_label, 1, 0)
        hb = QHBox(box)
        hb.setSpacing(3)
        hb.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        self.remote = QComboBox(True, hb)
        hb.setStretchFactor(self.remote, 4)
        self.remote_scan = QPushButton(i18n("Scan"), hb)
        hb.setStretchFactor(self.remote_scan, 1)
        g.addWidget(hb, 1, 1)


class BasicTab(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        self.my_parent = parent
        self.setMargin(6)
        self.setSpacing(6)

        hb = QHBox(self)
        hb.setSpacing(6)
        QLabel(i18n("Name:"), hb)
        self.name = widgets.Edit(hb)
        hb.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        self.device = Device(self)
        self.device.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        self.address = Address(self)
        self.address.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)


class Window(QMainWindow):
    def __init__(self, parent, name, link_name, is_new=0):
        QMainWindow.__init__(self, parent)
        self.name = name
        self.link_name = link_name
        
        self.setCaption(i18n("Configure network connection"))
        self.setMinimumSize(580, 380)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(6)
        self.setCentralWidget(vb)
        
        tab = QTabWidget(vb)
        self.tab = tab
        
        self.basic = BasicTab(tab)
        tab.addTab(self.basic, i18n("Basic"))
        
        hb = QHBox(vb)
        hb.setSpacing(12)
        but = QPushButton(i18n("Connect"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotConnect)
        but = QPushButton(i18n("Accept"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAccept)
        but = QPushButton(i18n("Cancel"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotCancel)
        
        self.w_name = self.basic.name.edit
        self.w_device = self.basic.device.device
        self.w_address = self.basic.address.address.edit
        self.w_gateway = self.basic.address.gateway.edit
        self.w_remote = self.basic.device.remote
        self.w_remote_label = self.basic.device.remote_label
        self.w_remote_scan = self.basic.device.remote_scan
        self.device_list = {}
        
        self.connect(self.w_remote_scan, SIGNAL("clicked()"), self.slotScan)
        
        lname = links.get_info(self.link_name).remote_name
        # what a hack! :)
        if lname == "Phone number":
            lname = i18n("Phone number")
        self.w_remote_label.setText(lname)
        self.show()
        
        self.w_name.setText(unicode(name))
        
        self.comar = comar.Link()
        self.comar.call_package("Net.Link.modes", link_name, id=3)
        if is_new:
            self.device = i18n("No device")
            self.comar.call_package("Net.Link.deviceList", link_name, id=1)
        else:
            self.comar.call_package("Net.Link.getAddress", link_name, [ "name", name ], id=2)
            self.comar.call_package("Net.Link.connectionInfo", link_name, [ "name", name ], id=4)
        
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def setData(self, id=0):
        name = self.w_name.text()
        if unicode(name) != unicode(self.name):
            self.comar.call_package("Net.Link.deleteConnection", self.link_name, [ "name", self.name ])
        self.name = name
        device = self.device_list[str(self.basic.device.device.currentText())]
        address = self.basic.address.address.edit.text()
        netmask = self.basic.address.netmask.edit.text()
        gateway = self.basic.address.gateway.edit.text()
        self.comar.call_package("Net.Link.setConnection", self.link_name, [ "name", name, "device", device ], id)
        if self.basic.address.r1.isChecked():
            self.comar.call_package("Net.Link.setAddress", self.link_name, [
                "name", name, "mode", "auto" ], id)
        else:
            self.comar.call_package("Net.Link.setAddress", self.link_name, [
                "name", name, "mode", "manual", "address", address, "mask", netmask, "gateway", gateway ], id)
        if "remote" in self.modes:
            remote = self.basic.device.remote.currentText()
            self.comar.call_package("Net.Link.setRemote", self.link_name, [
                "name", name, "remote", remote ], id)
        self.count = 3
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
            self.count += 1
    
    def slotScan(self):
        if self.device:
            self.comar.call_package("Net.Link.scanRemote", self.link_name, [ "device", self.device ], id=6)
    
    def slotConnect(self):
        self.setData(32)
        self.hide()
    
    def slotAccept(self):
        self.setData()
        self.close(True)
    
    def slotCancel(self):
        self.close(True)
    
    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        if reply[1] == 32:
            self.count -= 1
            if self.count == 0:
                self.comar.call_package("Net.Link.setState", self.link_name, [ "name", self.name, "state", "up" ])
                self.close(True)
        if reply[0] == self.comar.RESULT:
            if reply[1] == 1:
                for item in reply[2].split("\n"):
                    uid, info = item.split(" ", 1)
                    if uid != self.device:
                        self.w_device.insertItem(info)
                        self.device_list[info] = uid
            elif reply[1] == 2:
                name, mode, addr, gate = reply[2].split("\n", 3)
                mask = ""
                if "\n" in gate:
                    gate, mask = gate.split("\n", 1)
                self.basic.address.slotSwitch(mode)
                self.w_address.setText(addr)
                self.w_gateway.setText(gate)
                if mask:
                    self.basic.address.netmask.edit.setText(mask)
            elif reply[1] == 3:
                self.modes = reply[2].split(",")
                if not "remote" in self.modes:
                    self.basic.device.remote.hide()
                    self.basic.device.remote_label.hide()
                if not "auto" in self.modes:
                    self.basic.address.r2.setEnabled(False)
                if "remote" in self.modes:
                    self.comar.call_package("Net.Link.getRemote", self.link_name, [ "name", self.name ], id=5)
                if not "scan" in self.modes:
                    self.basic.device.remote_scan.hide()
                
                if "passauth" in self.modes or "loginauth" in self.modes or "keyauth" in self.modes:
                    self.auth = AuthTab(self.tab, self.modes)
                    self.tab.addTab(self.auth, i18n("Authentication"))
                    self.comar.call_package("Net.Link.getAuthentication", self.link_name, [ "name", self.name ], id=7)
                
                if not "net" in self.modes:
                    self.basic.address.setEnabled(False)
            elif reply[1] == 4:
                name, uid, info = reply[2].split("\n")
                self.device = uid
                self.w_device.insertItem(info)
                self.device_list[info] = uid
                self.comar.call_package("Net.Link.deviceList", self.link_name, id=1)
            elif reply[1] == 5:
                name, remote = reply[2].split("\n")
                self.w_remote.setCurrentText(remote)
            elif reply[1] == 6:
                old = self.w_remote.currentText()
                self.w_remote.clear()
                self.w_remote.insertItem(old)
                for item in reply[2].split("\n"):
                    self.w_remote.insertItem(item)
            elif reply[1] == 7:
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
