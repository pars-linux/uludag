# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settingsWindow.ui'
#
# Created: Prş Kas 6 13:03:51 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


from qt import *


class SettingsWindow(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("SettingsWindow")

        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.sizePolicy().hasHeightForWidth()))

        SettingsWindowLayout = QGridLayout(self,1,1,11,6,"SettingsWindowLayout")

        layout7 = QHBoxLayout(None,0,6,"layout7")
        spacer5 = QSpacerItem(518,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout7.addItem(spacer5)

        self.applyBut = QPushButton(self,"applyBut")
        self.applyBut.setFlat(1)
        layout7.addWidget(self.applyBut)

        self.cancelBut = QPushButton(self,"cancelBut")
        self.cancelBut.setFlat(1)
        layout7.addWidget(self.cancelBut)

        SettingsWindowLayout.addLayout(layout7,3,0)

        self.authenticationGroupBox = QGroupBox(self,"authenticationGroupBox")
        self.authenticationGroupBox.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.authenticationGroupBox.sizePolicy().hasHeightForWidth()))
        self.authenticationGroupBox.setFrameShape(QGroupBox.NoFrame)
        self.authenticationGroupBox.setFlat(0)
        self.authenticationGroupBox.setColumnLayout(0,Qt.Vertical)
        self.authenticationGroupBox.layout().setSpacing(3)
        self.authenticationGroupBox.layout().setMargin(6)
        authenticationGroupBoxLayout = QVBoxLayout(self.authenticationGroupBox.layout())
        authenticationGroupBoxLayout.setAlignment(Qt.AlignTop)

        layoutTop = QHBoxLayout(None,0,6,"layoutTop")

        self.security_mode_label = QLabel(self.authenticationGroupBox,"security_mode_label")
        layoutTop.addWidget(self.security_mode_label)

        self.security_mode_combo = QComboBox(0,self.authenticationGroupBox,"security_mode_combo")
        layoutTop.addWidget(self.security_mode_combo)
        spacer1 = QSpacerItem(380,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layoutTop.addItem(spacer1)
        authenticationGroupBoxLayout.addLayout(layoutTop)

        layout10 = QHBoxLayout(None,0,6,"layout10")

        layout8 = QGridLayout(None,1,1,0,6,"layout8")

        self.auth_key_type_label = QLabel(self.authenticationGroupBox,"auth_key_type_label")
        self.auth_key_type_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout8.addWidget(self.auth_key_type_label,1,0)

        self.auth_key_type_combo = QComboBox(0,self.authenticationGroupBox,"auth_key_type_combo")
        self.auth_key_type_combo.setDuplicatesEnabled(0)

        layout8.addWidget(self.auth_key_type_combo,1,1)

        self.auth_key_mode_label = QLabel(self.authenticationGroupBox,"auth_key_mode_label")
        self.auth_key_mode_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout8.addWidget(self.auth_key_mode_label,0,0)

        self.auth_inner_combo = QComboBox(0,self.authenticationGroupBox,"auth_inner_combo")
        self.auth_inner_combo.setDuplicatesEnabled(0)

        layout8.addWidget(self.auth_inner_combo,3,1)
        spacer9 = QSpacerItem(20,21,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout8.addItem(spacer9,4,1)

        self.auth_key_mode_combo = QComboBox(0,self.authenticationGroupBox,"auth_key_mode_combo")
        self.auth_key_mode_combo.setSizeLimit(2)
        self.auth_key_mode_combo.setMaxCount(2)
        self.auth_key_mode_combo.setInsertionPolicy(QComboBox.AtBottom)
        self.auth_key_mode_combo.setDuplicatesEnabled(0)

        layout8.addWidget(self.auth_key_mode_combo,0,1)

        self.auth_inner_label = QLabel(self.authenticationGroupBox,"auth_inner_label")
        self.auth_inner_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout8.addWidget(self.auth_inner_label,3,0)

        self.auth_mode_combo = QComboBox(0,self.authenticationGroupBox,"auth_mode_combo")
        self.auth_mode_combo.setDuplicatesEnabled(0)

        layout8.addWidget(self.auth_mode_combo,2,1)

        self.auth_mode_label = QLabel(self.authenticationGroupBox,"auth_mode_label")
        self.auth_mode_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout8.addWidget(self.auth_mode_label,2,0)
        layout10.addLayout(layout8)
        spacer8 = QSpacerItem(21,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        layout10.addItem(spacer8)

        layout11 = QGridLayout(None,1,1,0,6,"layout11")

        self.auth_private_key_label = QLabel(self.authenticationGroupBox,"auth_private_key_label")
        self.auth_private_key_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_private_key_label,5,0)

        self.auth_private_key_pass_line = QLineEdit(self.authenticationGroupBox,"auth_private_key_pass_line")
        self.auth_private_key_pass_line.setMinimumSize(QSize(210,0))
        self.auth_private_key_pass_line.setMaximumSize(QSize(232,32767))
        self.auth_private_key_pass_line.setFrameShape(QLineEdit.PopupPanel)
        self.auth_private_key_pass_line.setEchoMode(QLineEdit.Password)

        layout11.addWidget(self.auth_private_key_pass_line,6,1)

        self.auth_passphrase_label = QLabel(self.authenticationGroupBox,"auth_passphrase_label")
        self.auth_passphrase_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_passphrase_label,2,0)

        self.auth_private_key_but = QPushButton(self.authenticationGroupBox,"auth_private_key_but")
        self.auth_private_key_but.setMinimumSize(QSize(210,0))
        self.auth_private_key_but.setMaximumSize(QSize(232,32767))
        self.auth_private_key_but.setFlat(1)

        layout11.addWidget(self.auth_private_key_but,5,1)

        self.auth_client_cert_label = QLabel(self.authenticationGroupBox,"auth_client_cert_label")
        self.auth_client_cert_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_client_cert_label,3,0)

        self.auth_anon_id_label = QLabel(self.authenticationGroupBox,"auth_anon_id_label")
        self.auth_anon_id_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_anon_id_label,0,0)

        self.auth_user_line = QLineEdit(self.authenticationGroupBox,"auth_user_line")
        self.auth_user_line.setMinimumSize(QSize(210,0))
        self.auth_user_line.setMaximumSize(QSize(232,32767))
        self.auth_user_line.setFrameShape(QLineEdit.PopupPanel)

        layout11.addWidget(self.auth_user_line,1,1)

        self.auth_ca_cert_but = QPushButton(self.authenticationGroupBox,"auth_ca_cert_but")
        self.auth_ca_cert_but.setMinimumSize(QSize(210,0))
        self.auth_ca_cert_but.setMaximumSize(QSize(232,32767))
        self.auth_ca_cert_but.setFlat(1)

        layout11.addWidget(self.auth_ca_cert_but,4,1)

        self.auth_client_cert_but = QPushButton(self.authenticationGroupBox,"auth_client_cert_but")
        self.auth_client_cert_but.setMinimumSize(QSize(210,0))
        self.auth_client_cert_but.setMaximumSize(QSize(232,32767))
        self.auth_client_cert_but.setFlat(1)

        layout11.addWidget(self.auth_client_cert_but,3,1)

        self.auth_private_key_pass_label = QLabel(self.authenticationGroupBox,"auth_private_key_pass_label")
        self.auth_private_key_pass_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_private_key_pass_label,6,0)

        self.auth_anon_id_line = QLineEdit(self.authenticationGroupBox,"auth_anon_id_line")
        self.auth_anon_id_line.setMinimumSize(QSize(210,0))
        self.auth_anon_id_line.setMaximumSize(QSize(232,32767))
        self.auth_anon_id_line.setFrameShape(QLineEdit.PopupPanel)

        layout11.addWidget(self.auth_anon_id_line,0,1)

        self.auth_passphrase_line = QLineEdit(self.authenticationGroupBox,"auth_passphrase_line")
        self.auth_passphrase_line.setMinimumSize(QSize(210,0))
        self.auth_passphrase_line.setMaximumSize(QSize(232,32767))
        self.auth_passphrase_line.setPaletteBackgroundColor(QColor(255,192,192))
        self.auth_passphrase_line.setEchoMode(QLineEdit.Password)

        layout11.addWidget(self.auth_passphrase_line,2,1)

        self.auth_ca_cert_label = QLabel(self.authenticationGroupBox,"auth_ca_cert_label")
        self.auth_ca_cert_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_ca_cert_label,4,0)

        self.auth_user_label = QLabel(self.authenticationGroupBox,"auth_user_label")
        self.auth_user_label.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        layout11.addWidget(self.auth_user_label,1,0)
        spacer10 = QSpacerItem(20,34,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout11.addItem(spacer10,7,1)
        layout10.addLayout(layout11)
        spacer9_2 = QSpacerItem(20,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout10.addItem(spacer9_2)
        authenticationGroupBoxLayout.addLayout(layout10)

        SettingsWindowLayout.addWidget(self.authenticationGroupBox,1,0)

        layout6 = QHBoxLayout(None,0,6,"layout6")

        self.addressGroupBox = QGroupBox(self,"addressGroupBox")
        self.addressGroupBox.setFrameShape(QGroupBox.GroupBoxPanel)
        self.addressGroupBox.setFlat(0)
        self.addressGroupBox.setColumnLayout(0,Qt.Vertical)
        self.addressGroupBox.layout().setSpacing(3)
        self.addressGroupBox.layout().setMargin(10)
        addressGroupBoxLayout = QGridLayout(self.addressGroupBox.layout())
        addressGroupBoxLayout.setAlignment(Qt.AlignTop)

        self.auto_addr = QCheckBox(self.addressGroupBox,"auto_addr")

        addressGroupBoxLayout.addWidget(self.auto_addr,1,2)

        self.gatewayLabel = QLabel(self.addressGroupBox,"gatewayLabel")
        self.gatewayLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        addressGroupBoxLayout.addWidget(self.gatewayLabel,2,0)

        self.auto_gate = QCheckBox(self.addressGroupBox,"auto_gate")

        addressGroupBoxLayout.addWidget(self.auto_gate,2,2)

        self.netmask = QComboBox(0,self.addressGroupBox,"netmask")
        self.netmask.setMinimumSize(QSize(140,0))
        self.netmask.setMaximumSize(QSize(140,32767))
        self.netmask.setEditable(1)
        self.netmask.setMaxCount(5)
        self.netmask.setDuplicatesEnabled(0)

        addressGroupBoxLayout.addWidget(self.netmask,3,1)

        self.gateway = QLineEdit(self.addressGroupBox,"gateway")
        self.gateway.setMinimumSize(QSize(140,0))
        self.gateway.setMaximumSize(QSize(140,32767))
        self.gateway.setFrameShape(QLineEdit.PopupPanel)

        addressGroupBoxLayout.addWidget(self.gateway,2,1)

        self.address = QLineEdit(self.addressGroupBox,"address")
        self.address.setMinimumSize(QSize(140,0))
        self.address.setMaximumSize(QSize(140,32767))
        self.address.setFrameShape(QLineEdit.PopupPanel)

        addressGroupBoxLayout.addWidget(self.address,1,1)

        self.netmaskLabel = QLabel(self.addressGroupBox,"netmaskLabel")
        self.netmaskLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        addressGroupBoxLayout.addWidget(self.netmaskLabel,3,0)

        self.addressLabel = QLabel(self.addressGroupBox,"addressLabel")
        self.addressLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        addressGroupBoxLayout.addWidget(self.addressLabel,1,0)

        self.dhcpButtonGroup = QButtonGroup(self.addressGroupBox,"dhcpButtonGroup")
        self.dhcpButtonGroup.setFrameShape(QButtonGroup.NoFrame)
        self.dhcpButtonGroup.setFlat(0)
        self.dhcpButtonGroup.setColumnLayout(0,Qt.Vertical)
        self.dhcpButtonGroup.layout().setSpacing(6)
        self.dhcpButtonGroup.layout().setMargin(11)
        dhcpButtonGroupLayout = QGridLayout(self.dhcpButtonGroup.layout())
        dhcpButtonGroupLayout.setAlignment(Qt.AlignTop)

        self.r2 = QRadioButton(self.dhcpButtonGroup,"r2")

        dhcpButtonGroupLayout.addWidget(self.r2,0,1)

        self.r1 = QRadioButton(self.dhcpButtonGroup,"r1")

        dhcpButtonGroupLayout.addWidget(self.r1,0,0)

        addressGroupBoxLayout.addMultiCellWidget(self.dhcpButtonGroup,0,0,0,2)
        layout6.addWidget(self.addressGroupBox)

        self.dnsGroupBox = QGroupBox(self,"dnsGroupBox")
        self.dnsGroupBox.setFrameShape(QGroupBox.GroupBoxPanel)
        self.dnsGroupBox.setFlat(0)
        self.dnsGroupBox.setColumnLayout(0,Qt.Vertical)
        self.dnsGroupBox.layout().setSpacing(3)
        self.dnsGroupBox.layout().setMargin(10)
        dnsGroupBoxLayout = QGridLayout(self.dnsGroupBox.layout())
        dnsGroupBoxLayout.setAlignment(Qt.AlignTop)

        self.dns_text = QLineEdit(self.dnsGroupBox,"dns_text")
        self.dns_text.setFrameShape(QLineEdit.PopupPanel)

        dnsGroupBoxLayout.addWidget(self.dns_text,1,0)

        self.dns_group = QButtonGroup(self.dnsGroupBox,"dns_group")
        self.dns_group.setFrameShape(QButtonGroup.NoFrame)
        self.dns_group.setColumnLayout(0,Qt.Vertical)
        self.dns_group.layout().setSpacing(6)
        self.dns_group.layout().setMargin(11)
        dns_groupLayout = QGridLayout(self.dns_group.layout())
        dns_groupLayout.setAlignment(Qt.AlignTop)

        self.dns1 = QRadioButton(self.dns_group,"dns1")

        dns_groupLayout.addWidget(self.dns1,0,0)

        self.dns2 = QRadioButton(self.dns_group,"dns2")

        dns_groupLayout.addWidget(self.dns2,0,1)

        self.dns3 = QRadioButton(self.dns_group,"dns3")

        dns_groupLayout.addWidget(self.dns3,0,2)

        dnsGroupBoxLayout.addWidget(self.dns_group,0,0)
        layout6.addWidget(self.dnsGroupBox)

        SettingsWindowLayout.addLayout(layout6,2,0)

        self.connectionGroupBox = QGroupBox(self,"connectionGroupBox")
        self.connectionGroupBox.setFrameShape(QGroupBox.GroupBoxPanel)
        self.connectionGroupBox.setColumnLayout(0,Qt.Vertical)
        self.connectionGroupBox.layout().setSpacing(4)
        self.connectionGroupBox.layout().setMargin(10)
        connectionGroupBoxLayout = QGridLayout(self.connectionGroupBox.layout())
        connectionGroupBoxLayout.setAlignment(Qt.AlignTop)

        self.remote = QLineEdit(self.connectionGroupBox,"remote")
        self.remote.setFrameShape(QLineEdit.PopupPanel)

        connectionGroupBoxLayout.addWidget(self.remote,2,1)

        self.scanBut = QPushButton(self.connectionGroupBox,"scanBut")
        self.scanBut.setFlat(1)

        connectionGroupBoxLayout.addWidget(self.scanBut,2,3)

        self.selected_device_mode = QComboBox(0,self.connectionGroupBox,"selected_device_mode")

        connectionGroupBoxLayout.addWidget(self.selected_device_mode,2,2)

        self.devices_but = QPushButton(self.connectionGroupBox,"devices_but")
        self.devices_but.setFlat(1)

        connectionGroupBoxLayout.addWidget(self.devices_but,1,3)

        self.device = QLabel(self.connectionGroupBox,"device")

        connectionGroupBoxLayout.addMultiCellWidget(self.device,1,1,1,2)

        self.nameLineEdit = QLineEdit(self.connectionGroupBox,"nameLineEdit")
        self.nameLineEdit.setFrameShape(QLineEdit.PopupPanel)

        connectionGroupBoxLayout.addMultiCellWidget(self.nameLineEdit,0,0,1,3)

        self.nameLabel = QLabel(self.connectionGroupBox,"nameLabel")
        self.nameLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        connectionGroupBoxLayout.addWidget(self.nameLabel,0,0)

        self.deviceLabel = QLabel(self.connectionGroupBox,"deviceLabel")
        self.deviceLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        connectionGroupBoxLayout.addWidget(self.deviceLabel,1,0)

        self.ssidLabel = QLabel(self.connectionGroupBox,"ssidLabel")
        self.ssidLabel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)

        connectionGroupBoxLayout.addWidget(self.ssidLabel,2,0)

        SettingsWindowLayout.addWidget(self.connectionGroupBox,0,0)

        self.languageChange()

        self.resize(QSize(636,566).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.security_mode_label.setBuddy(self.security_mode_combo)
        self.auth_key_type_label.setBuddy(self.auth_key_type_combo)
        self.auth_key_mode_label.setBuddy(self.auth_key_mode_combo)
        self.auth_inner_label.setBuddy(self.auth_inner_combo)
        self.auth_mode_label.setBuddy(self.auth_mode_combo)
        self.auth_private_key_label.setBuddy(self.auth_private_key_but)
        self.auth_passphrase_label.setBuddy(self.auth_passphrase_line)
        self.auth_client_cert_label.setBuddy(self.auth_client_cert_but)
        self.auth_anon_id_label.setBuddy(self.auth_anon_id_line)
        self.auth_private_key_pass_label.setBuddy(self.auth_private_key_pass_line)
        self.auth_ca_cert_label.setBuddy(self.auth_ca_cert_but)
        self.auth_user_label.setBuddy(self.auth_user_line)
        self.gatewayLabel.setBuddy(self.gateway)
        self.netmaskLabel.setBuddy(self.netmask)
        self.addressLabel.setBuddy(self.address)
        self.device.setBuddy(self.auth_client_cert_but)


    def languageChange(self):
        self.setCaption(self.__tr("Network Settings"))
        self.applyBut.setText(self.__tr("Uygula"))
        self.cancelBut.setText(self.__trUtf8("\xc4\xb0\x70\x74\x61\x6c"))
        self.authenticationGroupBox.setTitle(QString.null)
        self.security_mode_label.setText(self.__trUtf8("\x47\xc3\xbc\x76\x65\x6e\x6c\x69\x6b"))
        self.auth_key_type_label.setText(self.__tr("Key Type"))
        self.auth_key_mode_label.setText(self.__tr("Mod"))
        self.auth_inner_label.setText(self.__trUtf8("\xc4\xb0\xc3\xa7\x20\x64\x6f\xc4\x9f\x72\x75\x6c\x61\x6d\x61"))
        self.auth_mode_label.setText(self.__trUtf8("\x4b\x69\x6d\x6c\x69\x6b\x20\x64\x6f\xc4\x9f\x72\x75\x6c\x61\x6d\x61"))
        self.auth_private_key_label.setText(self.__tr("Private Key File :"))
        self.auth_passphrase_label.setText(self.__tr("Parola :"))
        self.auth_private_key_but.setText(self.__tr("browse"))
        self.auth_client_cert_label.setText(self.__trUtf8("\xc4\xb0\x73\x74\x65\x6d\x63\x69\x20\x53\x65\x72\x74\x69\x66\x69\x6b\x61\x73\xc4\xb1\x20\x3a"))
        self.auth_anon_id_label.setText(self.__trUtf8("\x41\x6e\x6f\x6e\x69\x6d\x20\x4b\x75\x6c\x6c\x61\x6e\xc4\xb1\x63\xc4\xb1\x20\x3a"))
        self.auth_ca_cert_but.setText(self.__tr("browse"))
        self.auth_client_cert_but.setText(self.__tr("browse"))
        self.auth_private_key_pass_label.setText(self.__tr("Private Key Password :"))
        self.auth_ca_cert_label.setText(self.__trUtf8("\x43\x41\x20\x53\x65\x72\x74\x69\x66\x69\x6b\x61\x73\xc4\xb1\x20\x3a"))
        self.auth_user_label.setText(self.__trUtf8("\x4b\x75\x6c\x6c\x61\x6e\xc4\xb1\x63\xc4\xb1\x2f\x4b\x69\x6d\x6c\x69\x6b\x20\x3a"))
        self.addressGroupBox.setTitle(self.__trUtf8("\x41\x64\x72\x65\x73\x20\x41\x79\x61\x72\x6c\x61\x72\xc4\xb1"))
        self.auto_addr.setText(self.__trUtf8("\xc3\x96\x7a\x65\x6c"))
        self.gatewayLabel.setText(self.__trUtf8("\x41\xc4\x9f\x20\x47\x65\xc3\xa7\x69\x64\x69\x20\x3a"))
        self.auto_gate.setText(self.__trUtf8("\xc3\x96\x7a\x65\x6c"))
        self.netmask.clear()
        self.netmask.insertItem(QString.null)
        self.netmaskLabel.setText(self.__trUtf8("\x41\xc4\x9f\x20\x4d\x61\x73\x6b\x65\x73\x69\x20\x3a"))
        self.addressLabel.setText(self.__tr("Adres :"))
        self.dhcpButtonGroup.setTitle(QString.null)
        self.r2.setText(self.__tr("Elle Ayarla"))
        self.r1.setText(self.__tr("Otomatik Ayar (DHCP)"))
        self.dnsGroupBox.setTitle(self.__trUtf8("\xc4\xb0\x73\x69\x6d\x20\x53\x75\x6e\x75\x63\x75\x73\x75"))
        self.dns_group.setTitle(QString.null)
        self.dns1.setText(self.__trUtf8("\xc3\x96\x6e\x74\x61\x6e\xc4\xb1\x6d\x6c\xc4\xb1"))
        self.dns2.setText(self.__tr("Otomatik"))
        self.dns3.setText(self.__trUtf8("\xc3\x96\x7a\x65\x6c"))
        self.connectionGroupBox.setTitle(self.__trUtf8("\x42\x61\xc4\x9f\x6c\x61\x6e\x74\xc4\xb1"))
        self.scanBut.setText(self.__tr("Tara"))
        self.devices_but.setText(self.__trUtf8("\x41\x79\x67\xc4\xb1\x74\x20\x53\x65\xc3\xa7"))
        self.device.setText(self.__tr("Pro Wireless Hede Hot Intel Corporation Yooo (wlan0)"))
        self.nameLabel.setText(self.__trUtf8("\x41\x64\xc4\xb1\x20\x3a"))
        self.deviceLabel.setText(self.__trUtf8("\x41\x79\x67\xc4\xb1\x74\x20\x3a"))
        self.ssidLabel.setText(self.__tr("Ess ID :"))


    def __tr(self,s,c = None):
        return qApp.translate("SettingsWindow",s,c)

    def __trUtf8(self,s,c = None):
        return qApp.translate("SettingsWindow",s,c,QApplication.UnicodeUTF8)
