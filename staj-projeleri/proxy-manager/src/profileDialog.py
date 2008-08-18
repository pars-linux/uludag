# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileDialog.ui'
#
# Created: Cts Eki 13 15:10:22 2007
#      by: The PyQt User Interface Compiler (pyuic) 3-snapshot-20070613
#
# WARNING! All changes made in this file will be lost!


from qt import *
from kdecore import *
from kdeui import *



class profileDialog(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("Form1")


        Form1Layout = QGridLayout(self,1,1,8,2,"Form1Layout")

        layout6 = QGridLayout(None,1,1,4,4,"layout6")
        spacer4 = QSpacerItem(61,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout6.addItem(spacer4,0,0)

        self.cancel_but = QPushButton(self,"cancel_but")
        self.cancel_but.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.cancel_but.sizePolicy().hasHeightForWidth()))

        layout6.addWidget(self.cancel_but,0,2)

        self.apply_but = QPushButton(self,"apply_but")
        self.apply_but.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.apply_but.sizePolicy().hasHeightForWidth()))

        layout6.addWidget(self.apply_but,0,1)

        Form1Layout.addLayout(layout6,2,0)

        self.buttonGroup2 = QButtonGroup(self,"buttonGroup2")
        self.buttonGroup2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding,0,0,self.buttonGroup2.sizePolicy().hasHeightForWidth()))
        self.buttonGroup2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup2.layout().setSpacing(3)
        self.buttonGroup2.layout().setMargin(8)
        buttonGroup2Layout = QGridLayout(self.buttonGroup2.layout())
        buttonGroup2Layout.setAlignment(Qt.AlignTop)
        spacer1 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer1,3,0)
        spacer2_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2_2,5,0)
        spacer2_2_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2_2_2,1,0)

        self.textLabel6 = QLabel(self.buttonGroup2,"textLabel6")

        buttonGroup2Layout.addWidget(self.textLabel6,5,1)

        self.textLabel6_2 = QLabel(self.buttonGroup2,"textLabel6_2")

        buttonGroup2Layout.addMultiCellWidget(self.textLabel6_2,1,1,1,2)

        self.auto_url = QLineEdit(self.buttonGroup2,"auto_url")
        self.auto_url.setEnabled(0)

        buttonGroup2Layout.addMultiCellWidget(self.auto_url,5,5,2,6)

        self.details1 = QPushButton(self.buttonGroup2,"details1")
        self.details1.setMaximumSize(QSize(70,32767))

        buttonGroup2Layout.addWidget(self.details1,1,6)

        self.rd2 = QRadioButton(self.buttonGroup2,"rd2")

        buttonGroup2Layout.addMultiCellWidget(self.rd2,2,2,0,5)

        self.rd1 = QRadioButton(self.buttonGroup2,"rd1")

        buttonGroup2Layout.addMultiCellWidget(self.rd1,0,0,0,5)

        self.rd3 = QRadioButton(self.buttonGroup2,"rd3")

        buttonGroup2Layout.addMultiCellWidget(self.rd3,4,4,0,5)

        self.globl_host = QLineEdit(self.buttonGroup2,"globl_host")
        self.globl_host.setEnabled(0)
        self.globl_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.globl_host.sizePolicy().hasHeightForWidth()))

        buttonGroup2Layout.addWidget(self.globl_host,1,3)

        self.textLabel5_6 = QLabel(self.buttonGroup2,"textLabel5_6")
        self.textLabel5_6.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_6.sizePolicy().hasHeightForWidth()))

        buttonGroup2Layout.addWidget(self.textLabel5_6,1,4)

        self.globl_port = QLineEdit(self.buttonGroup2,"globl_port")
        self.globl_port.setEnabled(0)
        self.globl_port.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.globl_port.sizePolicy().hasHeightForWidth()))
        self.globl_port.setMaximumSize(QSize(60,32767))

        buttonGroup2Layout.addWidget(self.globl_port,1,5)

        layout5 = QGridLayout(None,1,1,0,2,"layout5")

        self.http_host = QLineEdit(self.buttonGroup2,"http_host")
        self.http_host.setEnabled(0)
        self.http_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.http_host.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.http_host,0,1)

        self.textLabel5_5 = QLabel(self.buttonGroup2,"textLabel5_5")
        self.textLabel5_5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_5.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.textLabel5_5,3,2)

        self.ch5 = QCheckBox(self.buttonGroup2,"ch5")
        self.ch5.setEnabled(0)
        self.ch5.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch5.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.ch5,3,0)
        spacer7 = QSpacerItem(16,99,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout5.addMultiCell(spacer7,1,3,4,4)

        self.ssl_host = QLineEdit(self.buttonGroup2,"ssl_host")
        self.ssl_host.setEnabled(0)
        self.ssl_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.ssl_host.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.ssl_host,2,1)

        self.ftp_host = QLineEdit(self.buttonGroup2,"ftp_host")
        self.ftp_host.setEnabled(0)
        self.ftp_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.ftp_host.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.ftp_host,1,1)

        self.details2 = QPushButton(self.buttonGroup2,"details2")
        self.details2.setMaximumSize(QSize(70,32767))

        layout5.addWidget(self.details2,0,4)

        self.socks_host = QLineEdit(self.buttonGroup2,"socks_host")
        self.socks_host.setEnabled(0)
        self.socks_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.socks_host.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.socks_host,3,1)

        self.ch1 = QCheckBox(self.buttonGroup2,"ch1")
        self.ch1.setEnabled(0)
        self.ch1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch1.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.ch1,0,0)

        self.textLabel5_4 = QLabel(self.buttonGroup2,"textLabel5_4")
        self.textLabel5_4.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_4.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.textLabel5_4,2,2)

        self.ssl_port = QLineEdit(self.buttonGroup2,"ssl_port")
        self.ssl_port.setEnabled(0)
        self.ssl_port.setMaximumSize(QSize(60,32767))

        layout5.addWidget(self.ssl_port,2,3)

        self.ch4 = QCheckBox(self.buttonGroup2,"ch4")
        self.ch4.setEnabled(0)
        self.ch4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch4.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.ch4,2,0)

        self.ftp_port = QLineEdit(self.buttonGroup2,"ftp_port")
        self.ftp_port.setEnabled(0)
        self.ftp_port.setMaximumSize(QSize(60,32767))

        layout5.addWidget(self.ftp_port,1,3)

        self.ch2 = QCheckBox(self.buttonGroup2,"ch2")
        self.ch2.setEnabled(0)
        self.ch2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch2.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.ch2,1,0)

        self.textLabel5 = QLabel(self.buttonGroup2,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.textLabel5,0,2)

        self.socks_port = QLineEdit(self.buttonGroup2,"socks_port")
        self.socks_port.setEnabled(0)
        self.socks_port.setMaximumSize(QSize(60,32767))

        layout5.addWidget(self.socks_port,3,3)

        self.textLabel5_2 = QLabel(self.buttonGroup2,"textLabel5_2")
        self.textLabel5_2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_2.sizePolicy().hasHeightForWidth()))

        layout5.addWidget(self.textLabel5_2,1,2)

        self.http_port = QLineEdit(self.buttonGroup2,"http_port")
        self.http_port.setEnabled(0)
        self.http_port.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.http_port.sizePolicy().hasHeightForWidth()))
        self.http_port.setMaximumSize(QSize(60,32767))

        layout5.addWidget(self.http_port,0,3)

        buttonGroup2Layout.addMultiCellLayout(layout5,3,3,1,6)

        Form1Layout.addWidget(self.buttonGroup2,1,0)

        layout4 = QGridLayout(None,1,1,0,2,"layout4")

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        layout4.addWidget(self.textLabel1,0,0)

        self.name_edit = QLineEdit(self,"name_edit")
        self.name_edit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum,0,0,self.name_edit.sizePolicy().hasHeightForWidth()))

        layout4.addWidget(self.name_edit,0,1)

        self.warning = QLabel(self,"warning")
        self.warning.setPaletteForegroundColor(QColor(255,0,0))
        self.warning.setAlignment(QLabel.AlignCenter)

        layout4.addMultiCellWidget(self.warning,1,1,0,1)

        Form1Layout.addLayout(layout4,0,0)

        self.languageChange()

        self.resize(QSize(410,396).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.name_edit,self.rd1)
        self.setTabOrder(self.rd1,self.rd2)
        self.setTabOrder(self.rd2,self.rd3)
        self.setTabOrder(self.rd3,self.ch1)
        self.setTabOrder(self.ch1,self.http_host)
        self.setTabOrder(self.http_host,self.http_port)
        self.setTabOrder(self.http_port,self.ch2)
        self.setTabOrder(self.ch2,self.ftp_host)
        self.setTabOrder(self.ftp_host,self.ftp_port)
        self.setTabOrder(self.ftp_port,self.ch4)
        self.setTabOrder(self.ch4,self.ssl_host)
        self.setTabOrder(self.ssl_host,self.ssl_port)
        self.setTabOrder(self.ssl_port,self.ch5)
        self.setTabOrder(self.ch5,self.socks_host)
        self.setTabOrder(self.socks_host,self.socks_port)
        self.setTabOrder(self.socks_port,self.auto_url)
        self.setTabOrder(self.auto_url,self.apply_but)
        self.setTabOrder(self.apply_but,self.cancel_but)


    def languageChange(self):
        self.setCaption(i18n("Proxy Settings"))
        self.cancel_but.setText(QString.null)
        self.apply_but.setText(QString.null)
        self.buttonGroup2.setTitle(i18n("Options"))
        self.textLabel6.setText(i18n("URL"))
        self.textLabel6_2.setText(i18n("Host"))
        self.details1.setText(i18n("Details"))
        self.rd2.setText(i18n("Use proxy server"))
        self.rd1.setText(i18n("Use a general proxy"))
        self.rd3.setText(i18n("Automatic settings"))
        self.textLabel5_6.setText(i18n("Port"))
        self.textLabel5_5.setText(i18n("Port"))
        self.ch5.setText(i18n("SOCKS"))
        self.details2.setText(i18n("Details"))
        self.ch1.setText(i18n("Http"))
        self.textLabel5_4.setText(i18n("Port"))
        self.ch4.setText(i18n("SSL"))
        self.ch2.setText(i18n("Ftp"))
        self.textLabel5.setText(i18n("Port"))
        self.textLabel5_2.setText(i18n("Port"))
        self.textLabel1.setText(i18n("Profile name:"))
        self.warning.setText(QString.null)

