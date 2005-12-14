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
import widgets
import comar


class AuthTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        g = QGridLayout(self, 4, 2, 6)
        
        group = QButtonGroup()
        self.group = group
        group.setExclusive(True)
        
        r1 = QRadioButton("No authentication", self)
        g.addMultiCellWidget(r1, 0, 0, 0, 1, g.AlignTop)
        group.insert(r1, 0)
        
        r2 = QRadioButton("Passphrase:", self)
        g.addWidget(r2, 1, 0, g.AlignTop)
        group.insert(r2, 1)
        
        self.phrase = widgets.Edit(self)
        g.addWidget(self.phrase, 1, 1, g.AlignTop)
        
        r3 = QRadioButton("Login", self)
        g.addWidget(r3, 2, 0, g.AlignTop)
        group.insert(r3, 2)
        
        g2 = QGridLayout(2, 2, 6)
        g.addLayout(g2, 2, 1)
        
        lab = QLabel("Name:", self)
        g2.addWidget(lab, 0, 0)
        
        self.name = widgets.Edit(self)
        g2.addWidget(self.name, 0, 1)
        
        lab = QLabel("Password:", self)
        g2.addWidget(lab, 1, 0)
        
        self.password = widgets.Edit(self)
        g2.addWidget(self.password, 1, 1)
        
        r4 = QRadioButton("Key", self)
        g.addMultiCellWidget(r4, 3, 3, 0, 1, g.AlignTop)
        group.insert(r4, 3)


class Address(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        
        widgets.HLine("Network:", self)
        
        box = QWidget(self)
        g = QGridLayout(box, 2, 2, 6)
        
        group = QButtonGroup()
        self.group = group
        group.setExclusive(True)
        self.connect(group, SIGNAL("clicked(int)"), self.slotClicked)
        
        self.r1 = QRadioButton("Automatic query (DHCP)", box)
        g.addMultiCellWidget(self.r1, 0, 0, 0, 1)
        group.insert(self.r1, 0)
        
        self.r2 = QRadioButton("Manual", box)
        g.addWidget(self.r2, 1, 0, g.AlignTop)
        group.insert(self.r2, 1)
        
        g2 = QGridLayout(2, 2, 6)
        g.addLayout(g2, 1, 1)
        
        lab = QLabel("Address:", box)
        g2.addWidget(lab, 0, 0)
        self.address = widgets.Edit(box)
        g2.addWidget(self.address, 0, 1)
        
        lab = QLabel("Gateway:", box)
        g2.addWidget(lab, 1, 0)
        self.gateway = widgets.Edit(box)
        g2.addWidget(self.gateway, 1, 1)
    
    def slotClicked(self, id):
        if id == 0:
            self.address.setEnabled(False)
            self.gateway.setEnabled(False)
        elif id == 1:
            self.address.setEnabled(True)
            self.gateway.setEnabled(True)


class Device(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        
        widgets.HLine("Device:", self)
        
        box = QWidget(self)
        g = QGridLayout(box, 2, 2, 6)
        
        lab = QLabel("Device:", box)
        g.addWidget(lab, 0, 0)
        self.device = QComboBox(False, box)
        
        g.addWidget(self.device, 0, 1)
        
        lab = QLabel("Essid:", box)
        g.addWidget(lab, 1, 0)
        self.remote = widgets.Edit(box)
        g.addWidget(self.remote, 1, 1)


class BasicTab(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        self.setMargin(6)
        self.setSpacing(6)

        hb = QHBox(self)
        QLabel("Name:", hb)
        self.name = widgets.Edit(hb)
        hb.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        self.device = Device(self)
        self.device.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        self.address = Address(self)
        self.address.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        
        #self.layout().insertStretch(-1)


class Window(QMainWindow):
    def __init__(self, parent, name, link_name, is_new=0):
        QMainWindow.__init__(self, parent)
        self.name = name
        self.link_name = link_name
        
        self.setCaption("Configure network connection")
        self.setMinimumSize(620, 420)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(6)
        self.setCentralWidget(vb)
        
        tab = QTabWidget(vb)
        
        self.basic = BasicTab(tab)
        tab.addTab(self.basic, "Basic")
        
        self.auth = AuthTab(tab)
        tab.addTab(self.auth, "Authentication")
        
        hb = QHBox(vb)
        but = QPushButton("Accept", hb)
        self.connect(but, SIGNAL("clicked()"), self.slotAccept)
        but = QPushButton("Cancel", hb)
        self.connect(but, SIGNAL("clicked()"), self.slotCancel)
        
        self.w_name = self.basic.name.edit
        self.w_device = self.basic.device.device
        self.w_address = self.basic.address.address.edit
        self.w_gateway = self.basic.address.gateway.edit
        self.w_remote = self.basic.device.remote.edit
        self.device_list = {}
        
        self.show()
        
        self.w_name.setText(unicode(name))
        
        self.comar = comar.Link()
        self.comar.call_package("Net.Link.modes", link_name, id=3)
        if is_new:
            self.device = "No device"
            self.comar.call_package("Net.Link.deviceList", link_name, id=1)
        else:
            self.comar.call_package("Net.Link.getAddress", link_name, [ "name", name ], id=2)
            self.comar.call_package("Net.Link.connectionInfo", link_name, [ "name", name ], id=4)
        
        self.notifier = QSocketNotifier(self.comar.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
    
    def slotAccept(self):
        name = self.w_name.text()
        if name != self.name:
            self.comar.call_package("Net.Link.deleteConnection", self.link_name, [ "name", self.name ])
        device = self.device_list[str(self.basic.device.device.currentText())]
        address = self.basic.address.address.edit.text()
        gateway = self.basic.address.gateway.edit.text()
        self.comar.call_package("Net.Link.setConnection", self.link_name, [ "name", name, "device", device ])
        self.comar.call_package("Net.Link.setAddress", self.link_name, [
            "name", name, "mode", "manual", "address", address, "gateway", gateway ])
        if "remote" in self.modes:
            remote = self.basic.device.remote.edit.text()
            self.comar.call_package("Net.Link.setRemote", self.link_name, [
                "name", name, "remote", remote ])
        self.close(True)
    
    def slotCancel(self):
        self.close(True)
    
    def slotComar(self, sock):
        reply = self.comar.read_cmd()
        if reply[0] == self.comar.RESULT:
            if reply[1] == 1:
                for item in reply[2].split("\n"):
                    uid, info = item.split(" ", 1)
                    if uid != self.device:
                        self.w_device.insertItem(info)
                        self.device_list[info] = uid
            elif reply[1] == 2:
                name, mode, addr, gate = reply[2].split("\n")
                self.w_address.setText(addr)
                self.w_gateway.setText(gate)
            elif reply[1] == 3:
                self.modes = reply[2].split(",")
                print self.modes
                if not "remote" in self.modes:
                    self.basic.device.remote.setEnabled(False)
                if not "auto" in self.modes:
                    self.basic.address.r2.setEnabled(False)
                if "remote" in self.modes:
                    self.comar.call_package("Net.Link.getRemote", self.link_name, [ "name", self.name ], id=5)
            elif reply[1] == 4:
                name, uid, info = reply[2].split("\n")
                self.device = uid
                self.w_device.insertItem(info)
                self.device_list[info] = uid
                self.comar.call_package("Net.Link.deviceList", self.link_name, id=1)
            elif reply[1] == 5:
                name, remote = reply[2].split("\n")
                self.w_remote.setText(remote)
