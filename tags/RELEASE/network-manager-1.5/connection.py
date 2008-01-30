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
        self.name.edit.setMaxLength(48)
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
        if "auth" in link.modes:
            line = widgets.HLine(i18n("Authentication"), self)
            grid.addMultiCellWidget(line, row, row, 0, 1)
            row += 1
            
            lab = QLabel(i18n("Mode:"), self)
            grid.addWidget(lab, row, 0, Qt.AlignRight)
            
            grid2 = QGridLayout(grid, 2, 1, 12)
            row += 1
            
            self.auth_mode = QComboBox(False, self)
            self.connect(self.auth_mode, SIGNAL("activated(int)"), self.slotAuthToggle)
            grid2.addWidget(self.auth_mode, 0, 0)
            grid2.setColStretch(1, 2)
            
            self.auth_mode.insertItem(i18n("No authentication"))
            flag = 0
            for mode in link.auth_modes:
                self.auth_mode.insertItem(mode.name)
                if mode.type == "login":
                    flag = 1
            
            self.auth_stack = QWidgetStack(self)
            grid2.addWidget(self.auth_stack, 0, 1)
            
            lab = QLabel("", self)
            self.auth_stack.addWidget(lab, 0)
            
            hb = QHBox(self)
            hb.setSpacing(6)
            QLabel(i18n("Password:"), hb)
            self.auth_passphrase = QLineEdit(hb)
            self.auth_passphrase.setEchoMode(QLineEdit.Password)
            self.auth_stack.addWidget(hb, 1)
            
            if flag == 1:
                w = QWidget(self)
                grid3 = QGridLayout(w, 2, 2, 6)
                grid3.addWidget(QLabel(i18n("User name:"), w), 0, 0, Qt.AlignRight)
                self.auth_user = QLineEdit(w)
                grid3.addWidget(self.auth_user, 0, 1)
                grid3.addWidget(QLabel(i18n("Password:"), w), 1, 0, Qt.AlignRight)
                self.auth_password = QLineEdit(w)
                self.auth_password.setEchoMode(QLineEdit.Password)
                grid3.addWidget(self.auth_password, 1, 1)
                self.auth_stack.addWidget(w, 2)
        
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
        vb = QVBox(pop)
        pop.insertItem(vb)
        vb.setMargin(3)
        vb.setSpacing(3)
        lab = QLabel(i18n("Scan results:"), vb)
        box = QListBox(vb)
        box.connect(box, SIGNAL("selectionChanged()"), self.slotScanSelect)
        box.connect(box, SIGNAL("selected(QListBoxItem *)"), self.slotScanDouble)
        box.setMinimumSize(260, 110)
        self.scan_box = box
        hb = QHBox(vb)
        hb.setSpacing(6)
        but = QPushButton(getIconSet("reload.png", KIcon.Small), i18n("Scan again"), hb)
        self.connect(but, SIGNAL("clicked()"), self.slotScan)
        but = QPushButton(getIconSet("key_enter.png", KIcon.Small), i18n("Use"), hb)
        self.scan_use_but = but
        self.connect(but, SIGNAL("clicked()"), self.slotScanUse)
        return pop
    
    def slotAuthToggle(self, i):
        if i == 0:
            self.auth_stack.raiseWidget(0)
        elif self.link.auth_modes[i-1].type == "pass":
            self.auth_stack.raiseWidget(1)
        elif self.link.auth_modes[i-1].type == "login":
            self.auth_stack.raiseWidget(2)
    
    def slotScanDouble(self, item):
        self.remote.setText(item.text())
        self.scanpop.hide()
    
    def slotScanSelect(self):
        item = self.scan_box.selectedItem()
        self.scan_use_but.setEnabled(item != None)
    
    def slotScanUse(self):
        item = self.scan_box.selectedItem()
        if item:
            self.remote.setText(item.text())
            self.scanpop.hide()
    
    def slotScan(self):
        self.scan_use_but.setEnabled(False)
        self.scan_box.clear()
        comlink.queryRemotes(self.link.script, self.device_uid)
    
    def slotRemotes(self, script, remotes):
        if self.link.script != script:
            return
        for remote in remotes.split("\n"):
            self.scan_box.insertItem(remote)
    
    def initNet(self, grid, row):
        line = widgets.HLine(i18n("Network settings"), self)
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
        self.address.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.address))
        self.connect(self.address, SIGNAL("textChanged(const QString &)"), self.slotAddr)
        grid2.addWidget(self.address, 0, 1)
        self.auto_addr = QCheckBox(i18n("Custom"), box)
        self.connect(self.auto_addr, SIGNAL("clicked()"), self.slotFields)
        grid2.addWidget(self.auto_addr, 0, 2)
        
        lab = QLabel(i18n("Net mask:"), box)
        grid2.addWidget(lab, 1, 0, Qt.AlignRight)
        self.netmask = QLineEdit(box)
        self.netmask.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.netmask))
        grid2.addWidget(self.netmask, 1, 1)
        
        lab = QLabel(i18n("Gateway:"), box)
        grid2.addWidget(lab, 2, 0, Qt.AlignRight)
        self.gateway = QLineEdit(box)
        self.gateway.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.gateway))
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
        self.connect(self.dns_group, SIGNAL("clicked(int)"), self.slotNetToggle)
        
        self.dns_text = QLineEdit(hb)
        
        return row
    
    def setValues(self):
        conn = self.conn
        self.device_items = []
        if conn:
            self.name.edit.setText(unicode(conn.name))
            self.device.setText(conn.devname)
            self.device_uid = self.conn.devid
            if "remote" in self.link.modes:
                if conn.remote:
                    self.remote.setText(conn.remote)
            if "net" in self.link.modes:
                if conn.net_mode == "auto":
                    self.r1.setChecked(True)
                else:
                    self.r2.setChecked(True)
                    if conn.net_addr:
                        self.address.setText(conn.net_addr)
                    if conn.net_mask:
                        self.netmask.setText(conn.net_mask)
                    if conn.net_gate:
                        self.gateway.setText(conn.net_gate)
                if conn.dns_mode == "default":
                    self.dns1.setChecked(True)
                elif conn.dns_mode == "auto":
                    self.dns2.setChecked(True)
                else:
                    self.dns3.setChecked(True)
                    if conn.dns_server:
                        self.dns_text.setText(conn.dns_server)
            if "auth" in self.link.modes:
                self.auth_mode.setCurrentItem(0)
                if conn.auth_mode != "none":
                    i = 1
                    for mode in self.link.auth_modes:
                        if mode.id == conn.auth_mode:
                            if mode.type == "pass":
                                self.auth_passphrase.setText(unicode(conn.auth_pass))
                            elif mode.type == "login":
                                self.auth_user.setText(unicode(conn.auth_user))
                                self.auth_password.setText(unicode(conn.auth_pass))
                            self.auth_mode.setCurrentItem(i)
                            self.slotAuthToggle(i)
                            break
                        i += 1
        else:
            self.name.edit.setText(unicode(comlink.uniqueName()))
            self.device_uid = self.new_conn[0]
            self.device.setText(self.new_conn[1])
            if "net" in self.link.modes:
                self.r1.setChecked(True)
        if "net" in self.link.modes:
            self.slotFields()
    
    def useValues(self):
        name = str(self.name.edit.text())
        
        if "net" in self.link.modes:
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
        script_object = comlink.com.Net.Link[self.link.script]
        flag = False
        
        if conn and conn.name != name:
            script_object.deleteConnection(name=conn.name)
            flag = True
        
        if flag or conn == None or self.device_uid != conn.devid:
            script_object.setConnection(name=name, device=self.device_uid)
        
        if "net" in self.link.modes:
            script_object.setAddress(name=name, mode=mode, address=address, mask=netmask, gateway=gateway)
            nameserver = ""
            if self.dns1.isChecked():
                namemode = "default"
            elif self.dns2.isChecked():
                namemode = "auto"
            elif self.dns3.isChecked():
                namemode = "custom"
                nameserver = self.dns_text.text()
            script_object.setNameService(name=name, namemode=namemode, nameserver=nameserver)
        
        if "remote" in self.link.modes:
            remote = self.remote.text()
            if conn == None or remote != self.conn.remote:
                script_object.setRemote(name=name, remote=remote)
        
        if "auth" in self.link.modes:
            i = self.auth_mode.currentItem()
            if i == 0:
                script_object.setAuthentication(name=name, authmode="none", user="", password="")
            else:
                mode = self.link.auth_modes[i-1]
                if mode.type == "pass":
                    pw = unicode(self.auth_passphrase.text())
                    script_object.setAuthentication(name=name, authmode=mode.id, user="", password=pw)
                elif mode.type == "login":
                    u = unicode(self.auth_user.text())
                    pw = unicode(self.auth_password.text())
                    script_object.setAuthentication(name=name, authmode=mode.id, user=u, password=pw)
    
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
        self.dns2.setEnabled(auto)
        self.dns_text.setEnabled(self.dns_group.selectedId() == 2)
    
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
    
    def slotAccept(self):
        self.settings.useValues()
        self.settings.cleanup()
        self.close(True)
    
    def slotCancel(self):
        self.settings.cleanup()
        self.close(True)
