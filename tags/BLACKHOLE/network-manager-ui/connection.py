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

from settingsWindow import SettingsWindow

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

class Settings(SettingsWindow):
    def __init__(self, parent, conn, link=None, new_conn=None):
        SettingsWindow.__init__(self, parent)

        if not link:
            link = comlink.links[conn.script]

        self.connect(self.applyBut, SIGNAL("clicked()"), self.useValues)
        self.connect(self.cancelBut, SIGNAL("clicked()"), self.slotCancel)

        self.scanpop = None
        self.link = link
        self.conn = conn
        self.new_conn = new_conn
        self.channel = None
        self.auth_dict = {"TLS":[], "TTLS":["PAP","MSCHAPV2"], "PEAP":["MSCHAPV2", "MD5"]}
        self.apmac = ''
        self.auth_client_cert = ""
        self.auth_ca_cert = ""
        self.auth_private_key = ""
        self.auth_private_key_pass = ""

        self.fillLabels()

        self.devices = QPopupMenu()
        self.connect(self.devices, SIGNAL("activated(int)"), self.slotDeviceSelect)
        self.devices_but.setPopup(self.devices)

        self.address.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.address))
        self.netmask.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.netmask))
        self.gateway.setValidator(QRegExpValidator(QRegExp("[0123456789.:]*"), self.gateway))

        if "remote" in link.modes:
            if "scan" in link.modes:
                self.scanpop = Scanner(self)
                comlink.remote_hook.append(self.scanpop.slotRemotes)
                self.scanBut.setPopup(self.scanpop)
            else:
                self.scanBut.hide()

            if "devicemode" in link.modes:
                for dev_mode in link.device_modes:
                    self.selected_device_mode.insertItem(dev_mode)
            else:
                self.selected_device_mode.hide()
        else:
            self.scanBut.hide()
            self.remote.hide()
            self.selected_device_mode.hide()
            self.ssidLabel.hide()

        if "auth" in link.modes:
            self.security_mode_combo.insertItem(i18n("No authentication"))

            for mode in self.link.auth_modes:
                self.security_mode_combo.insertItem(mode.name)
            for enc in self.auth_dict:
                self.auth_mode_combo.insertItem(enc)

            self.connect(self.security_mode_combo, SIGNAL("activated(int)"), self.slotSecurityToggle)
            self.connect(self.auth_passphrase_line, SIGNAL("textChanged(const QString &)"), self.slotPasswordCheck)
            self.connect(self.auth_mode_combo, SIGNAL("activated(int)"), self.slotAuthToggle)
            self.connect(self.auth_ca_cert_but, SIGNAL("clicked()"), self.getCaCert)
            self.connect(self.auth_client_cert_but, SIGNAL("clicked()"), self.getClientCert)
            self.connect(self.auth_private_key_but, SIGNAL("clicked()"), self.getPrivateKey)

            self.slotSecurityToggle()
        else:
            self.authenticationGroupBox.hide()

        if "net" in link.modes:
            self.connect(self.dhcpButtonGroup, SIGNAL("clicked(int)"), self.slotNetToggle)
            if not self.conn:
                self.connect(self.address, SIGNAL("textChanged(const QString &)"), self.slotAddr)

            self.connect(self.auto_addr, SIGNAL("clicked()"), self.slotFields)

            for msk in ["255.0.0.0", "255.255.0.0", "255.255.255.0"]:
                self.netmask.insertItem(msk)

            self.connect(self.auto_gate, SIGNAL("clicked()"), self.slotFields)
            self.connect(self.dns_group, SIGNAL("clicked(int)"), self.slotNetToggle)
        else:
            self.addressGroupBox.hide()
            self.dnsGroupBox.hide()

        self.setValues()
        self.slotPasswordCheck()
        self.adjustSize()

        comlink.device_hook.append(self.slotDevices)
        comlink.queryDevices(link.script)

        self.show()

    def fillLabels(self):
        self.setCaption(i18n("Configure network connection"))
        self.connectionGroupBox.setTitle(i18n("Connection"))
        self.addressGroupBox.setTitle(i18n("Address Settings"))
        self.dnsGroupBox.setTitle(i18n("Name Server Settings"))
        self.nameLabel.setText(i18n("Name"))
        self.deviceLabel.setText(i18n("Device"))
        self.devices_but.setText(i18n("Select"))
        self.ssidLabel.setText(unicode(self.link.remote_name))
        self.r1.setText(i18n("Automatic query (DHCP)"))
        self.r2.setText(i18n("Manual"))
        self.addressLabel.setText(i18n("Address :"))
        self.auto_addr.setText(i18n("Custom"))
        self.netmaskLabel.setText(i18n("Net mask :"))
        self.gatewayLabel.setText(i18n("Gateway :"))
        self.auto_gate.setText(i18n("Custom"))
        self.dns1.setText(i18n("Default"))
        self.dns2.setText(i18n("Automatic"))
        self.dns3.setText(i18n("Custom"))
        self.security_mode_label.setText(i18n("Security"))
        self.auth_private_key_label.setText(i18n("Private Key File :"))
        self.auth_private_key_pass_label.setText(i18n("Private Key Password :"))
        self.auth_ca_cert_label.setText(i18n("CA Certificate :"))
        self.auth_client_cert_label.setText(i18n("Client Certificate :"))
        self.auth_passphrase_label.setText(i18n("Password :"))
        self.auth_user_label.setText(i18n("User/Identity :"))
        self.auth_anon_id_label.setText(i18n("Anonymous User :"))
        self.auth_inner_label.setText(i18n("Inner Authentication"))
        self.auth_mode_label.setText(i18n("Authentication"))
        self.auth_client_cert_but.setText(i18n("browse"))
        self.auth_client_cert_but.setIconSet(getIconSet("file", KIcon.Small))
        self.auth_ca_cert_but.setText(i18n("browse"))
        self.auth_ca_cert_but.setIconSet(getIconSet("file", KIcon.Small))
        self.auth_private_key_but.setText(i18n("browse"))
        self.auth_private_key_but.setIconSet(getIconSet("file", KIcon.Small))
        self.applyBut.setIconSet(getIconSet("apply", KIcon.Small))
        self.applyBut.setText(i18n("Apply"))
        self.cancelBut.setIconSet(getIconSet("cancel", KIcon.Small))
        self.cancelBut.setText(i18n("Cancel"))

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
            self.adjustSize()
            return

        if sec != None and auth == None:
            if sec == 0:
                self.setAuthVisible(False)
            else:
                self.setAuthVisible(True)
                self.auth_mode_combo.setCurrentItem(0)
                self.updateStack(self.security_mode_combo.currentItem(), 0)

        if sec != None and auth != None:
            if sec == 0:
                self.setAuthVisible(False)

            elif self.link.auth_modes[sec-1].type == "pass":
                self.setAuthVisible(False)
                self.auth_passphrase_label.show()
                self.auth_passphrase_line.show()

            elif self.link.auth_modes[sec-1].type == "login":
                self.setAuthVisible(False)
                self.auth_passphrase_line.show()
                self.auth_passphrase_label.show()
                self.auth_user_line.show()
                self.auth_user_label.show()

            elif self.link.auth_modes[sec-1].type == "certificate":
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

        self.adjustSize()

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

    def slotPasswordCheck(self, pword=None):
        pword = self.auth_passphrase_line.text()

        self.auth_passphrase_line.setPaletteBackgroundColor(QColor(208, 255, 192))

        if pword.isEmpty():
            self.auth_passphrase_line.setPaletteBackgroundColor(QColor(255, 192, 192))
        # wep
        elif self.security_mode_combo.currentText() == "WEP":
            pass
            # hex key

    def slotSecurityToggle(self, i=None):
        # security mode changed, like wep, wpa-psk ..
        if i != None:
            self.updateStack(i, self.auth_mode_combo.currentItem())
        else:
            self.updateStack(self.security_mode_combo.currentItem())
        self.slotPasswordCheck()

    def slotAuthToggle(self, i):
        self.updateStack(self.security_mode_combo.currentItem(), i)

    def setValues(self):
        conn = self.conn
        self.device_items = []
        if conn:
            self.nameLineEdit.setText(unicode(conn.name))
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
                if conn.auth_mode != "none":
                    i = 1
                    for mode in self.link.auth_modes:
                        if mode.id == conn.auth_mode:
                            if mode.type == "pass":
                                self.auth_passphrase_line.setText(unicode(conn.auth_pass))
                                self.security_mode_combo.setCurrentItem(i)
                                self.slotSecurityToggle(i)
                                if mode.id == "wep":
                                    pass
                            elif mode.type == "login":
                                self.auth_user_line.setText(unicode(conn.auth_user))
                                self.auth_passphrase_line.setText(unicode(conn.auth_pass))
                                self.security_mode_combo.setCurrentItem(i)
                                self.slotSecurityToggle(i)
                            elif mode.type == "certificate":
                                if mode.id == conn.auth_mode:
                                    self.security_mode_combo.setCurrentItem(i)
                                    self.slotSecurityToggle(i)

                                self.auth_client_cert = conn.auth_client_cert
                                self.auth_ca_cert = conn.auth_ca_cert
                                self.auth_private_key = conn.auth_private_key
                                self.auth_user_line.setText(unicode(conn.auth_user))
                                self.auth_passphrase_line.setText(unicode(conn.auth_pass))
                                self.auth_anon_id_line.setText(unicode(conn.auth_anon))
                                if conn.auth_ca_cert:
                                    self.auth_ca_cert_but.setText(unicode(conn.auth_ca_cert).split('/')[-1])
                                if conn.auth_client_cert:
                                    self.auth_client_cert_but.setText(unicode(conn.auth_client_cert).split('/')[-1])
                                if conn.auth_private_key:
                                    self.auth_private_key_but.setText(unicode(conn.auth_private_key).split('/')[-1])
                                self.auth_private_key_pass_line.setText(unicode(conn.auth_private_key_pass))
                                for j in self.auth_dict:
                                    if conn.auth_auth == j:
                                        self.auth_mode_combo.setCurrentItem(self.auth_dict.keys().index(j))
                                        self.slotAuthToggle(self.auth_dict.keys().index(j))
                                        if j != "TLS":
                                            self.auth_inner_combo.setCurrentItem(self.auth_dict[j].index(conn.auth_inner))
                            break
                        i += 1
        else:
            self.nameLineEdit.setText(unicode(comlink.uniqueName()))
            self.device_uid = self.new_conn[0]
            self.device.setText(self.new_conn[1])
            if "net" in self.link.modes:
                self.r1.setChecked(True)
                self.dns1.setChecked(True)
        if "net" in self.link.modes:
            self.slotFields()

    def useValues(self):
        name = str(self.nameLineEdit.text())
        conn = self.conn

        def saveConnection(set_conn):
            if set_conn:
                # create connection / update device
                comlink.call(self.link.script, "Net.Link", "setConnection", name, self.device_uid)
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
                comlink.call(self.link.script, "Net.Link", "setAddress", name, mode, address, netmask, gateway)
                # set name servers
                nameserver = ""
                if self.dns1.isChecked():
                    namemode = "default"
                elif self.dns2.isChecked():
                    namemode = "auto"
                elif self.dns3.isChecked():
                    namemode = "custom"
                    nameserver = str(self.dns_text.text())
                comlink.call(self.link.script, "Net.Link", "setNameService", name, namemode, nameserver)
            if "devicemode" in self.link.modes:
                selected_device_mode = str(self.selected_device_mode.currentText())
                comlink.call(self.link.script, "Net.Link", "setConnectionMode", name, selected_device_mode)
            if "remote" in self.link.modes:
                # set remote address
                remote = str(self.remote.text())
                comlink.call(self.link.script, "Net.Link", "setRemote", name, remote, self.apmac)
                if self.channel != None:
                    comlink.call(self.link.script, "Net.Link", "setChannel", name, self.channel)
            if "auth" in self.link.modes:
                i = self.security_mode_combo.currentItem()
                if i == 0:
                    comlink.call(self.link.script, "Net.Link", "setAuthentication", name, "none", "", "", "", "", "", "", "", "", "")
                else:
                    mode = self.link.auth_modes[i-1]
                    if mode.type == "pass":
                        pw = unicode(self.auth_passphrase_line.text())
                        comlink.call(self.link.script, "Net.Link", "setAuthentication", name, mode.id, "", pw, "", "", "", "", "", "", "")
                    elif mode.type == "login":
                        u = unicode(self.auth_user_line.text())
                        pw = unicode(self.auth_passphrase_line.text())
                        comlink.call(self.link.script, "Net.Link", "setAuthentication", name, mode.id, u, pw, "", "", "", "", "", "", "")
                    elif mode.type == "certificate":
                        if mode.id == "802.1x":
                            u = unicode(self.auth_user_line.text())
                            pw = unicode(self.auth_passphrase_line.text())
                            an = unicode(self.auth_anon_id_line.text())
                            au = unicode(self.auth_mode_combo.currentText())
                            p2 = unicode(self.auth_inner_combo.currentText())
                            comlink.call(self.link.script, "Net.Link", "setAuthentication", name, mode.id, u, pw, au, an, p2,\
                                str(self.auth_client_cert), str(self.auth_ca_cert), str(self.auth_private_key), str(self.auth_private_key_pass_line.text()))
                        else:
                            u = unicode(self.auth_user_line.text())
                            pw = unicode(self.auth_passphrase_line.text())
                            comlink.call(self.link.script, "Net.Link", "setAuthentication", name, mode.id, u, pw, "", "", "", "", "", "", "")
            # close dialog
            self.parent().setEnabled(True)
            self.cleanup()
            self.close()

        def error(exception):
            self.parent().setEnabled(True)

        def cancel():
            self.parent().setEnabled(True)

        self.parent().setEnabled(False)
        if conn and conn.name != name:
            ch = comlink.callHandler(self.link.script, "Net.Link", "deleteConnection", "tr.org.pardus.comar.net.link.set")
            ch.registerDone(saveConnection, True)
            ch.registerCancel(cancel)
            ch.registerError(error)
            ch.registerDBusError(error)
            ch.registerAuthError(error)
            ch.call(conn.name)
        else:
            ch = comlink.callHandler(self.link.script, "Net.Link", "setConnection", "tr.org.pardus.comar.net.link.set")
            ch.registerDone(saveConnection, False)
            ch.registerCancel(cancel)
            ch.registerError(error)
            ch.registerDBusError(error)
            ch.registerAuthError(error)
            ch.call(name, self.device_uid)

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
        auto = self.dhcpButtonGroup.selectedId()
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
            m = unicode(mask.currentText())
            if not self.maskOK(m):
                return
            if cl > 0 and cl < 127:
                mask.setCurrentText("255.0.0.0")
            elif cl > 127 and cl < 192:
                mask.setCurrentText("255.255.0.0")
            elif cl > 191 and cl < 224:
                mask.setCurrentText("255.255.255.0")

    def slotCancel(self):
        self.cleanup()
        self.close()

