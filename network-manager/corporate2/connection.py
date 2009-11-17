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
from kfile import KFileDialog

import widgets
from icons import getIconSet, icons
from comariface import comlink

class WirelessTipper(QToolTip):
    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item and item.info:
            self.tip(self.list.itemRect(item),
                "<nobr>%s: %s</nobr><br><nobr>%s: %s</nobr><br><nobr>%s: %s</nobr>" %
                    (
                    i18n("Channel"), item.info["channel"],
                    i18n("Mode"), item.info["mode"],
                    i18n("Protocol"), item.info["protocol"]
                    )
            )

class ScanItem(QListViewItem):
    def __init__(self, parent, data):
        QListViewItem.__init__(self, parent)
        self.info = {}

        if not data:
            self.setPixmap(0, getIconSet("remove", KIcon.Small).pixmap(QIconSet.Automatic, QIconSet.Normal))
            self.setText(1, "")
            self.setText(2, i18n("No remotes found"))
            return

        for key, value in data.iteritems():
            self.info[key] = value

        enc = self.info.get("encryption", "none")
        if enc != "none":
            self.setPixmap(0, getIconSet("kgpg_key1", KIcon.Small).pixmap(QIconSet.Automatic, QIconSet.Normal))
        self.enc = enc

        qual = self.info.get("quality", "0")
        try:
            qual = int(qual)
        except:
            qual = 0
        self.setPixmap(1, self.signalIcon(qual))

        remote = self.info["remote"]
        if remote == "<hidden>" or remote == "":
            remote = i18n("<hidden>")
        self.remote = remote
        self.setText(3, remote)

        self.mac = self.info.get("mac", None)
        if self.mac:
            self.setText(4, self.mac)

        point_mode = self.info["mode"]

        if point_mode == "Ad-Hoc":
            self.setPixmap(2, getIconSet("attach", KIcon.Small).pixmap(QIconSet.Automatic, QIconSet.Normal))

    def signalIcon(self, signal):
        # FIXME: make this more pythonic
        num = 0
        if signal >= 80:
            num = 4
        elif signal >= 60:
            num = 3
        elif signal >= 40:
            num = 2
        elif signal >= 20:
            num = 1

        iconSet = getIconSet(locate("data", "network-manager/signal_%d.png" % num), KIcon.Small)
        return iconSet.pixmap(QIconSet.Automatic, QIconSet.Normal)


class Scanner(QPopupMenu):
    def __init__(self, parent):
        QPopupMenu.__init__(self)
        self.parent = parent
        self.connect(self, SIGNAL("aboutToShow()"), self.slotScan)
        vb = QVBox(self)
        self.insertItem(vb)
        vb.setMargin(3)
        vb.setSpacing(3)
        lab = QLabel(i18n("Scan results:"), vb)
        self.view = QListView(vb)
        self.view.connect(self.view, SIGNAL("selectionChanged()"), self.slotScanSelect)
        self.view.connect(self.view, SIGNAL("doubleClicked(QListViewItem *)"), self.slotScanDouble)
        self.view.setMinimumSize(300, 120)
        self.view.addColumn("")
        self.view.addColumn("")
        self.view.addColumn("")
        self.view.addColumn("")
        self.view.addColumn("")
        self.view.setColumnAlignment(4, Qt.AlignRight)
        self.view.setResizeMode(QListView.LastColumn)
        self.view.setAllColumnsShowFocus(True)
        self.view.setShowToolTips(True)
        self.view.header().hide()
        self.package_tipper = WirelessTipper(self.view.viewport())
        self.package_tipper.list = self.view
        hb = QHBox(vb)
        hb.setSpacing(6)
        but = QPushButton(getIconSet("reload", KIcon.Small), i18n("Scan again"), hb)
        but.setFlat(1)
        self.connect(but, SIGNAL("clicked()"), self.slotScan)
        but = QPushButton(getIconSet("key_enter", KIcon.Small), i18n("Use"), hb)
        but.setFlat(1)
        self.scan_use_but = but
        self.connect(but, SIGNAL("clicked()"), self.slotScanUse)

    def slotScanDouble(self, item):
        if not item.info:
            return

        parent = self.parent
        parent.remote.setText(item.remote)
        parent.apmac = item.mac
        parent.channel = item.info.get("channel")

        dev_mode = item.info["mode"]

        if dev_mode == "Master" or dev_mode == "Managed":
            parent.selected_device_mode.setCurrentText("Managed")
        else:
            parent.selected_device_mode.setCurrentText("Ad-Hoc")

        if item.enc == "none":
            i = 0
        else:
            i = 1
            for mode in parent.link.auth_modes:
                if mode.id == item.enc:
                    break
                i += 1
        auth_last = parent.link.auth_modes[parent.security_mode_combo.currentItem() - 1].id
        auth_now = item.enc
        if not (auth_last.startswith("wep") and auth_now.startswith("wep")):
            parent.security_mode_combo.setCurrentItem(i)
        parent.slotSecurityToggle(i)
        self.hide()

    def slotScanSelect(self):
        item = self.view.selectedItem()
        if item:
            if item.info:
                self.scan_use_but.setEnabled(True)

    def slotScanUse(self):
        item = self.view.selectedItem()
        if item:
            self.slotScanDouble(item)

    def slotScan(self):
        self.scan_use_but.setEnabled(False)
        comlink.queryRemotes(self.parent.link.script, self.parent.device_uid)

    def slotRemotes(self, script, remotes):
        if self.parent.link.script != script:
            return
        self.view.clear()
        if remotes:
            for remote in remotes:
                ScanItem(self.view, remote)
        else:
            ScanItem(self.view, None)


class Settings(QWidget):
    def __init__(self, parent, link, conn, new_conn=None):
        QWidget.__init__(self, parent)

        self.scanpop = None
        self.link = link
        self.conn = conn
        self.new_conn = new_conn
        self.channel = None
        self.auth_dict = {"TLS":[], "TTLS":["PAP","MSCHAPV2"], "PEAP":["MSCHAPV2", "MD5"]}

        self.apmac = ''
        lay = QVBoxLayout(self, 3, 3, "mainVertLayout")

        # Identification
        grid = QGridLayout(1, 2, 6)
        lay.addLayout(grid)
        lab = QLabel(i18n("Connection name:"), self)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.name = widgets.Edit(self)
        self.name.edit.setMaxLength(48)
        grid.addWidget(self.name, 0, 1)

        # Connection
        line = widgets.HLine(i18n("Connection"), self, "irkick")
        lay.addSpacing(6)
        lay.addWidget(line)

        grid = QGridLayout(None, 1, 1, 11, 6)

        lab = QLabel(i18n("Device:"), self)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.device = QLabel("", self)
        grid.addMultiCellWidget(self.device, 0, 0, 1, 2)

        self.devices_but = QPushButton(i18n("Select"), self)
        self.devices_but.setEnabled(False)
        self.devices_but.setFlat(1)
        grid.addWidget(self.devices_but, 0, 3)

        self.devices = QPopupMenu()
        self.connect(self.devices, SIGNAL("activated(int)"), self.slotDeviceSelect)
        self.devices_but.setPopup(self.devices)

        self.selected_device_mode = QComboBox(False, self)
        grid.addWidget(self.selected_device_mode, 1, 2)

        self.ssidLabel = QLabel(unicode(link.remote_name), self)
        grid.addWidget(self.ssidLabel, 1, 0, Qt.AlignRight)

        self.remote = QLineEdit(self)
        grid.addWidget(self.remote, 1, 1)

        self.scanBut = QPushButton(getIconSet("find", KIcon.Small), i18n("Scan"), self)
        self.scanBut.setFlat(1)
        grid.addWidget(self.scanBut, 1, 3)

        if "remote" in link.modes:
            if "remote_scan" in link.modes:
                self.scanpop = Scanner(self)
                comlink.remote_hook.append(self.scanpop.slotRemotes)
                self.scanBut.setPopup(self.scanpop)
            else:
                self.scanBut.hide()

            if "device_mode" in link.modes:
                for dev_mode in link.device_modes:
                    self.selected_device_mode.insertItem(dev_mode)
            else:
                self.selected_device_mode.hide()
        else:
            self.scanBut.hide()
            self.remote.hide()
            self.selected_device_mode.hide()
            self.ssidLabel.hide()

        lay.addLayout(grid)

        # Authentication
        if "auth" in link.modes:
            self.auth_client_cert = ""
            self.auth_ca_cert = ""
            self.auth_private_key = ""
            self.auth_private_key_pass = ""

            line = widgets.HLine(i18n("Authentication"), self, "kgpg_key1")
            lay.addSpacing(6)
            lay.addWidget(line)

            grid = QGridLayout(lay, 1, 1, 6, "mainAuthGrid")

            layoutLeft = QGridLayout(None, 1, 1, 0, 6, "layoutLeft")

            self.security_mode_label = QLabel(i18n("Security:"), self)
            self.security_mode_combo = QComboBox(0, self)
            self.security_mode_combo.setWFlags(Qt.WStyle_NoBorder)
            self.security_mode_combo.insertItem(i18n("No authentication"))
            layoutLeft.addWidget(self.security_mode_label, 0, 0, Qt.AlignRight)
            layoutLeft.addWidget(self.security_mode_combo, 0, 1)

            self.auth_mode_label = QLabel(i18n("Authentication:"), self)
            self.auth_mode_combo = QComboBox(0, self)
            self.auth_mode_combo.setWFlags(Qt.WStyle_NoBorder)
            layoutLeft.addWidget(self.auth_mode_label, 1, 0, Qt.AlignRight)
            layoutLeft.addWidget(self.auth_mode_combo, 1, 1)

            self.auth_inner_label = QLabel(i18n("Inner Authentication:"), self)
            self.auth_inner_combo = QComboBox(0, self)
            self.auth_inner_combo.setWFlags(Qt.WStyle_NoBorder)
            layoutLeft.addWidget(self.auth_inner_label, 2, 0, Qt.AlignRight)
            layoutLeft.addWidget(self.auth_inner_combo, 2, 1)

            grid.addLayout(layoutLeft, 0, 0)
            spacer1 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
            grid.addItem(spacer1, 1, 0)

            layoutRight = QGridLayout(None, 1, 1, 0, 6, "layoutRight")

            self.auth_anon_id_label = QLabel(i18n("Anonymous Identity:"), self)
            self.auth_anon_id_line = QLineEdit(self)
            layoutRight.addWidget(self.auth_anon_id_label, 0, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_anon_id_line, 0, 1)

            self.auth_user_label = QLabel(i18n("User/Identity"), self)
            self.auth_user_line = QLineEdit(self)
            layoutRight.addWidget(self.auth_user_label, 1, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_user_line, 1, 1)

            self.auth_passphrase_label = QLabel(i18n("Password:"), self)
            self.auth_passphrase_line = QLineEdit(self)
            self.auth_passphrase_line.setEchoMode(QLineEdit.Password)
            layoutRight.addWidget(self.auth_passphrase_label, 2, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_passphrase_line, 2, 1)

            self.auth_client_cert_label = QLabel(i18n("Client Certificate:"), self)
            self.auth_client_cert_but = QPushButton(getIconSet("file", KIcon.Small), i18n("browse"),  self)
            self.auth_client_cert_but.setFlat(1)
            layoutRight.addWidget(self.auth_client_cert_label, 3, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_client_cert_but, 3, 1)

            self.auth_ca_cert_label = QLabel(i18n("CA Certificate:"), self)
            self.auth_ca_cert_but = QPushButton(getIconSet("file", KIcon.Small), i18n("browse"), self)
            self.auth_ca_cert_but.setFlat(1)
            layoutRight.addWidget(self.auth_ca_cert_label, 4, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_ca_cert_but, 4, 1)

            self.auth_private_key_label = QLabel(i18n("Private Key File:"), self)
            self.auth_private_key_but = QPushButton(getIconSet("file", KIcon.Small), i18n("browse"), self)
            self.auth_private_key_but.setFlat(1)
            layoutRight.addWidget(self.auth_private_key_label, 5, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_private_key_but, 5, 1)

            self.auth_private_key_pass_label = QLabel(i18n("Private Key Password:"), self)
            self.auth_private_key_pass_line = QLineEdit(self)
            self.auth_private_key_pass_line.setEchoMode(QLineEdit.Password)
            layoutRight.addWidget(self.auth_private_key_pass_label, 6, 0, Qt.AlignRight)
            layoutRight.addWidget(self.auth_private_key_pass_line, 6, 1)

            grid.addMultiCellLayout(layoutRight, 0, 1, 1, 1)
            spacer2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
            grid.addItem(spacer2, 2, 1)

            for mode in self.link.auth_modes:
                self.security_mode_combo.insertItem(mode.name)
            for enc in self.auth_dict:
                self.auth_mode_combo.insertItem(enc)

            self.connect(self.security_mode_combo, SIGNAL("activated(int)"), self.slotSecurityToggle)
            self.connect(self.auth_mode_combo, SIGNAL("activated(int)"), self.slotAuthToggle)
            self.connect(self.auth_ca_cert_but, SIGNAL("clicked()"), self.getCaCert)
            self.connect(self.auth_client_cert_but, SIGNAL("clicked()"), self.getClientCert)
            self.connect(self.auth_private_key_but, SIGNAL("clicked()"), self.getPrivateKey)

            self.slotSecurityToggle()

        # Communication
        if "net" in link.modes:
            self.initNet(lay)

        self.setValues()

        comlink.device_hook.append(self.slotDevices)
        comlink.queryDevices(link.script)

    def getCaCert(self, parent=None):
        i = KFileDialog.getOpenFileName("", i18n("*|Certificates"), parent, i18n("Select CA Certificate File"))
        if i:
            self.auth_ca_cert = i
            self.auth_ca_cert_but.setText(self.auth_ca_cert.section('/', -1))

    def getClientCert(self, parent=None):
        i = KFileDialog.getOpenFileName("", i18n("*|Certificates"), parent, i18n("Select Client Certificate File"))
        if i:
            self.auth_client_cert = i
            self.auth_client_cert_but.setText(self.auth_client_cert.section('/', -1))

    def getPrivateKey(self, parent=None):
        i = KFileDialog.getOpenFileName("", i18n("*|Certificates"), parent, i18n("Select Private Key File"))
        if i:
            self.auth_private_key = i
            self.auth_private_key_but.setText(self.auth_private_key.section('/', -1))

    def cleanup(self):
        self.apmac = ''
        if self.scanpop:
            comlink.remote_hook.remove(self.scanpop.slotRemotes)
        comlink.device_hook.remove(self.slotDevices)

    def updateStack(self, sec=None, auth=None):
        """ if auth is given, clears the inner combobox and adds related inner auth methods.
            if sec is given, hides/shows related parts of authentication section.
            give both sec and auth, if you'll use this while editing ( not creating a new connection )
        """
        if auth != None and sec == None:
            self.auth_inner_combo.clear()
            for i in self.auth_dict:
                if self.auth_dict.keys().index(i) == auth:
                    self.auth_mode_combo.setCurrentItem(auth)
                    if len(self.auth_dict[i]) == 0:
                        self.auth_inner_combo.hide()
                        self.auth_inner_label.hide()
                    else:
                        self.auth_inner_label.show()
                        self.auth_inner_combo.show()
                        for j in self.auth_dict[i]:
                            self.auth_inner_combo.insertItem(j)
            return

        if sec != None and auth == None:
            if sec == 0:
                self.setAuthVisible(False)
            else:
                self.setAuthVisible(True)
                self.auth_mode_combo.setCurrentItem(0)
                self.slotAuthToggle(0)

        if sec != None and auth != None:
            if sec == 0:
                self.setAuthVisible(False)

            elif len(self.link.auth_modes[sec-1].paramters) == 1:
                self.setAuthVisible(False)
                self.auth_passphrase_label.show()
                self.auth_passphrase_line.show()

            elif len(self.link.auth_modes[sec-1].paramters) == 2:
                self.setAuthVisible(False)
                self.auth_passphrase_line.show()
                self.auth_passphrase_label.show()
                self.auth_user_line.show()
                self.auth_user_label.show()

            elif len(self.link.auth_modes[sec-1].paramters) > 2:
                self.setAuthVisible(True)
                self.updateStack(None, auth)

                if len(self.auth_dict[str(self.auth_mode_combo.currentText())]) == 0:
                    self.auth_inner_combo.hide()
                    self.auth_inner_label.hide()

                if self.auth_mode_combo.currentText() == "TLS":
                    self.auth_passphrase_line.hide()
                    self.auth_passphrase_label.hide()
                    self.auth_anon_id_line.hide()
                    self.auth_anon_id_label.hide()

                elif self.auth_mode_combo.currentText() in ["TTLS", "PEAP"]:
                    self.auth_client_cert_label.hide()
                    self.auth_client_cert_but.hide()
                    self.auth_private_key_but.hide()
                    self.auth_private_key_label.hide()
                    self.auth_private_key_pass_line.hide()
                    self.auth_private_key_pass_label.hide()

    def setAuthVisible(self, true):
        self.auth_mode_label.setShown(true)
        self.auth_mode_combo.setShown(true)
        self.auth_inner_label.setShown(true)
        self.auth_inner_combo.setShown(true)
        self.auth_anon_id_label.setShown(true)
        self.auth_anon_id_line.setShown(true)
        self.auth_user_label.setShown(true)
        self.auth_user_line.setShown(true)
        self.auth_passphrase_label.setShown(true)
        self.auth_passphrase_line.setShown(true)
        self.auth_client_cert_label.setShown(true)
        self.auth_client_cert_but.setShown(true)
        self.auth_ca_cert_label.setShown(true)
        self.auth_ca_cert_but.setShown(true)
        self.auth_private_key_label.setShown(true)
        self.auth_private_key_but.setShown(true)
        self.auth_private_key_pass_line.setShown(true)
        self.auth_private_key_pass_label.setShown(true)

    def slotSecurityToggle(self, i=None):
        if i != None:
            self.updateStack(i, self.auth_mode_combo.currentItem())
        else:
            self.updateStack(self.security_mode_combo.currentItem())

    def slotAuthToggle(self, i):
        self.updateStack(self.security_mode_combo.currentItem(), i)

    def initNet(self, lay):
        line = widgets.HLine(i18n("Network settings"), self, "network")
        lay.addSpacing(12)
        lay.addWidget(line)

        grid = QGridLayout(3, 4, 6)
        lay.addLayout(grid)
        row = 0

        self.group = QButtonGroup()
        self.connect(self.group, SIGNAL("clicked(int)"), self.slotNetToggle)
        self.r1 = QRadioButton(i18n("Automatic query (DHCP)"), self)
        self.group.insert(self.r1, 1)
        grid.addMultiCellWidget(self.r1, row, row, 0, 2)
        row += 1

        self.r2 = QRadioButton(i18n("Manual"), self)
        grid.addWidget(self.r2, row, 0, Qt.AlignTop)
        self.group.insert(self.r2, 0)

        lab = QLabel(i18n("Address:"), self)
        grid.addWidget(lab, row, 1, Qt.AlignRight)
        self.address = QLineEdit(self)
        self.address.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.address))
        if not self.conn:
            self.connect(self.address, SIGNAL("textChanged(const QString &)"), self.slotAddr)
        grid.addWidget(self.address, row, 2)
        self.auto_addr = QCheckBox(i18n("Custom"), self)
        self.connect(self.auto_addr, SIGNAL("clicked()"), self.slotFields)
        grid.addWidget(self.auto_addr, row, 3)
        row += 1

        lab = QLabel(i18n("Net mask:"), self)
        grid.addWidget(lab, row, 1, Qt.AlignRight)
        self.netmask = QComboBox(True, self)
        self.netmask.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.netmask))
        self.netmask.insertItem("255.0.0.0")
        self.netmask.insertItem("255.255.0.0")
        self.netmask.insertItem("255.255.255.0")
        self.netmask.setCurrentText("")
        grid.addWidget(self.netmask, row, 2)
        row += 1

        lab = QLabel(i18n("Gateway:"), self)
        grid.addWidget(lab, row, 1, Qt.AlignRight)
        self.gateway = QLineEdit(self)
        self.gateway.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.gateway))
        grid.addWidget(self.gateway, row, 2)
        self.auto_gate = QCheckBox(i18n("Custom"), self)
        self.connect(self.auto_gate, SIGNAL("clicked()"), self.slotFields)
        grid.addWidget(self.auto_gate, row, 3)

        line = widgets.HLine(i18n("Name servers"), self, "kaddressbook")
        lay.addSpacing(12)
        lay.addWidget(line)

        hb = QHBox(self)
        lay.addWidget(hb)
        self.dns_group = QButtonGroup()
        self.dns1 = QRadioButton(i18n("Default"), hb)
        self.dns_group.insert(self.dns1, 0)
        self.dns2 = QRadioButton(i18n("Automatic"), hb)
        self.dns_group.insert(self.dns2, 1)
        self.dns3 = QRadioButton(i18n("Custom"), hb)
        self.dns_group.insert(self.dns3, 2)
        self.connect(self.dns_group, SIGNAL("clicked(int)"), self.slotNetToggle)

        self.dns_text = QLineEdit(hb)

    def setValues(self):
        conn = self.conn
        self.device_items = []
        if conn:
            self.name.edit.setText(unicode(conn.name))
            if conn.devname:
                self.device.setText(conn.devname)
            self.device_uid = self.conn.devid
            if "devicemode" in self.link.modes:
                self.selected_device_mode.setCurrentText(conn.device_mode)
            if "remote" in self.link.modes:
                if conn.remote:
                    self.remote.setText(conn.remote)
                if conn.apmac:
                    self.apmac = conn.apmac
                else:
                    self.apmac = ''
            if "net" in self.link.modes:
                if conn.net_mode == "auto":
                    self.r1.setChecked(True)
                    if conn.net_addr:
                        self.auto_addr.setChecked(True)
                        self.address.setText(conn.net_addr)
                        if conn.net_mask:
                            self.netmask.setCurrentText(conn.net_mask)
                    if conn.net_gate:
                        self.auto_gate.setChecked(True)
                        self.gateway.setText(conn.net_gate)
                else:
                    self.r2.setChecked(True)
                    if conn.net_addr:
                        self.address.setText(conn.net_addr)
                    if conn.net_mask:
                        self.netmask.setCurrentText(conn.net_mask)
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
                self.security_mode_combo.setCurrentItem(0)
                auth_mode, auth_parameters = comlink.getAuth(self.link.script, conn.name)
                if auth_mode != "none":
                    i = 1
                    for mode in self.link.auth_modes:
                        if mode.id == auth_mode:
                            if len(mode.paramters) == 1:
                                self.auth_passphrase_line.setText(unicode(auth_parameters.get("password", "")))
                                self.security_mode_combo.setCurrentItem(i)
                                self.slotSecurityToggle(i)
                            if len(mode.paramters) == 2:
                                self.auth_user_line.setText(unicode(auth_parameters.get("username", "")))
                                self.auth_passphrase_line.setText(unicode(auth_parameters.get("password", "")))
                                self.security_mode_combo.setCurrentItem(i)
                                self.slotSecurityToggle(i)
                            elif len(mode.paramters) > 2:
                                pass
                                """
                                if mode.id == conn.auth_mode:
                                    self.security_mode_combo.setCurrentItem(i)
                                    self.slotSecurityToggle(i)

                                self.auth_client_cert = conn.auth_client_cert
                                self.auth_ca_cert = conn.auth_ca_cert
                                self.auth_private_key = conn.auth_private_key
                                self.auth_user_line.setText(unicode(conn.auth_user))
                                self.auth_passphrase_line.setText(unicode(conn.auth_pass))
                                self.auth_anon_id_line.setText(unicode(conn.auth_anon))
                                self.auth_ca_cert_but.setText(unicode(conn.auth_ca_cert).split('/')[-1])
                                self.auth_client_cert_but.setText(unicode(conn.auth_client_cert).split('/')[-1])
                                self.auth_private_key_but.setText(unicode(conn.auth_private_key).split('/')[-1])
                                self.auth_private_key_pass_line.setText(unicode(conn.auth_private_key_pass))
                                for j in self.auth_dict:
                                    if conn.auth_auth == j:
                                        self.auth_mode_combo.setCurrentItem(self.auth_dict.keys().index(j))
                                        self.slotAuthToggle(self.auth_dict.keys().index(j))
                                        if j != "TLS":
                                            self.auth_inner_combo.setCurrentItem(self.auth_dict[j].index(conn.auth_inner))
                                """
                            break
                        i += 1
        else:
            self.name.edit.setText(unicode(comlink.uniqueName()))
            self.device_uid = self.new_conn[0]
            self.device.setText(self.new_conn[1])
            if "net" in self.link.modes:
                self.r1.setChecked(True)
                self.dns1.setChecked(True)
        if "net" in self.link.modes:
            self.slotFields()

    def useValues(self):
        name = str(self.name.edit.text())
        conn = self.conn

        def saveConnection(package, exception, args):
            if exception:
                self.parent().setEnabled(True)
                return
            comlink.link.Network.Link[self.link.script].setDevice(name, self.device_uid)
            if "net" in self.link.modes:
                # set address
                address = str(self.address.text())
                netmask = str(self.netmask.currentText())
                gateway = str(self.gateway.text())
                if self.r1.isChecked():
                    mode = "auto"
                    if not self.auto_addr.isChecked():
                        address = ""
                        netmask = ""
                    if not self.auto_gate.isChecked():
                        gateway = ""
                else:
                    mode = "manual"
                comlink.link.Network.Link[self.link.script].setAddress(name, mode, address, netmask, gateway)
                # set name servers
                nameserver = ""
                if self.dns1.isChecked():
                    namemode = "default"
                elif self.dns2.isChecked():
                    namemode = "auto"
                elif self.dns3.isChecked():
                    namemode = "custom"
                    nameserver = str(self.dns_text.text())
                comlink.link.Network.Link[self.link.script].setNameService(name, namemode, nameserver)
            if "devicemode" in self.link.modes:
                selected_device_mode = str(self.selected_device_mode.currentText())
                comlink.link.Network.Link[self.link.script].setDeviceMode(name, selected_device_mode)
            if "remote" in self.link.modes:
                # set remote address
                remote = str(self.remote.text())
                comlink.link.Network.Link[self.link.script].setRemote(name, remote)
            if "auth" in self.link.modes:
                i = self.security_mode_combo.currentItem()
                if i == 0:
                    comlink.link.Network.Link[self.link.script].setAuthMethod(name, "none")
                else:
                    mode = self.link.auth_modes[i-1]
                    comlink.link.Network.Link[self.link.script].setAuthMethod(name, mode.id)
                    if len(mode.paramters)  == 1:
                        pw = unicode(self.auth_passphrase_line.text())
                        comlink.link.Network.Link[self.link.script].setAuthParameters(name, "password", pw)
                    elif len(mode.paramters)  == 2:
                        u = unicode(self.auth_user_line.text())
                        pw = unicode(self.auth_passphrase_line.text())
                        comlink.link.Network.Link[self.link.script].setAuthParameters(name, "username", u)
                        comlink.link.Network.Link[self.link.script].setAuthParameters(name, "password", pw)
                    elif len(mode.paramters) > 2:
                        u = unicode(self.auth_user_line.text())
                        pw = unicode(self.auth_passphrase_line.text())
                        an = unicode(self.auth_anon_id_line.text())
                        au = unicode(self.auth_mode_combo.currentText())
                        p2 = unicode(self.auth_inner_combo.currentText())
                        pass
            # close dialog
            self.parent().setEnabled(True)
            self.cleanup()
            self.parent().parent().close(True)

        self.parent().setEnabled(False)
        if conn and conn.name != name:
            comlink.link.Network.Link[self.link.script].deleteConnection(conn.name, async=saveConnection)
        else:
            comlink.link.Network.Link[self.link.script].setDevice(name, self.device_uid, async=saveConnection)

    def slotDevices(self, script, devices):
        if script != self.link.script:
            return
        self.devices.clear()
        self.device_items = []
        id = 0
        for uid, info in devices.iteritems():
            self.device_items.append((uid, info))
            self.devices.insertItem(info, id)
            id += 1
        if id > 1 or (self.conn and not self.conn.devname):
            self.devices_but.setEnabled(True)
        if id == 1 and self.conn and (self.conn.devid != self.device_items[0][0]):
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
        
        # Switching to manual mode causes dns mode left in automatic dns mode
        if not auto and self.dns2.isChecked():
            self.dns1.setChecked(True)

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
            m = unicode(mask.currentText())
            if not self.maskOK(m):
                return
            if cl > 0 and cl < 127:
                mask.setCurrentText("255.0.0.0")
            elif cl > 127 and cl < 192:
                mask.setCurrentText("255.255.0.0")
            elif cl > 191 and cl < 224:
                mask.setCurrentText("255.255.255.0")


class Window(QMainWindow):
    def __init__(self, parent, conn, link=None, new_conn=None):
        QMainWindow.__init__(self, parent, " ", Qt.WType_Dialog)
        
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
        but = QPushButton(getIconSet("apply", KIcon.Small), i18n("Apply"), hb)
        but.setFlat(1)
        self.connect(but, SIGNAL("clicked()"), self.slotAccept)
        but = QPushButton(getIconSet("cancel", KIcon.Small), i18n("Cancel"), hb)
        but.setFlat(1)
        self.connect(but, SIGNAL("clicked()"), self.slotCancel)
        
        self.show()
    
    def slotAccept(self):
        self.settings.useValues()
    
    def slotCancel(self):
        self.settings.cleanup()
        self.close(True)
