# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'profileDialog.ui'
#
# Created: Pzt Tem 9 14:40:35 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17
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


        Form1Layout = QGridLayout(self,1,1,11,2,"Form1Layout")

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

        layout15 = QGridLayout(None,1,1,0,0,"layout15")

        self.name_edit = QLineEdit(self,"name_edit")
        self.name_edit.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum,0,0,self.name_edit.sizePolicy().hasHeightForWidth()))

        layout15.addWidget(self.name_edit,0,1)

        self.warning = QLabel(self,"warning")
        self.warning.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum,0,0,self.warning.sizePolicy().hasHeightForWidth()))
        self.warning.setPaletteForegroundColor(QColor(255,0,0))
        self.warning.setAlignment(QLabel.AlignCenter)

        layout15.addWidget(self.warning,1,1)

        self.textLabel1 = QLabel(self,"textLabel1")
        self.textLabel1.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Minimum,0,0,self.textLabel1.sizePolicy().hasHeightForWidth()))

        layout15.addWidget(self.textLabel1,0,0)
        spacer5 = QSpacerItem(100,20,QSizePolicy.Minimum,QSizePolicy.Minimum)
        layout15.addItem(spacer5,1,0)

        Form1Layout.addLayout(layout15,0,0)

        self.buttonGroup2 = QButtonGroup(self,"buttonGroup2")
        self.buttonGroup2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Expanding,0,0,self.buttonGroup2.sizePolicy().hasHeightForWidth()))
        self.buttonGroup2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup2.layout().setSpacing(2)
        self.buttonGroup2.layout().setMargin(11)
        buttonGroup2Layout = QGridLayout(self.buttonGroup2.layout())
        buttonGroup2Layout.setAlignment(Qt.AlignTop)
        spacer1 = QSpacerItem(40,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addMultiCell(spacer1,3,3,0,1)
        spacer2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2,2,0)
        spacer2_2 = QSpacerItem(20,20,QSizePolicy.Fixed,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2_2,5,0)

        self.auto_url = QLineEdit(self.buttonGroup2,"auto_url")
        self.auto_url.setEnabled(0)

        buttonGroup2Layout.addWidget(self.auto_url,5,3)

        self.rd1 = QRadioButton(self.buttonGroup2,"rd1")

        buttonGroup2Layout.addMultiCellWidget(self.rd1,0,0,0,3)

        self.rd3 = QRadioButton(self.buttonGroup2,"rd3")

        buttonGroup2Layout.addMultiCellWidget(self.rd3,4,4,0,3)

        self.textLabel6 = QLabel(self.buttonGroup2,"textLabel6")

        buttonGroup2Layout.addMultiCellWidget(self.textLabel6,5,5,1,2)

        self.ch0 = QCheckBox(self.buttonGroup2,"ch0")

        buttonGroup2Layout.addMultiCellWidget(self.ch0,2,2,1,3)

        layout18 = QGridLayout(None,1,1,0,2,"layout18")

        self.ch5 = QCheckBox(self.buttonGroup2,"ch5")
        self.ch5.setEnabled(0)
        self.ch5.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch5.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ch5,4,0)

        self.textLabel5_3 = QLabel(self.buttonGroup2,"textLabel5_3")
        self.textLabel5_3.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_3.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.textLabel5_3,2,2)

        self.ch2 = QCheckBox(self.buttonGroup2,"ch2")
        self.ch2.setEnabled(0)
        self.ch2.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch2.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ch2,1,0)

        self.textLabel5_2 = QLabel(self.buttonGroup2,"textLabel5_2")
        self.textLabel5_2.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_2.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.textLabel5_2,1,2)

        self.ch4 = QCheckBox(self.buttonGroup2,"ch4")
        self.ch4.setEnabled(0)
        self.ch4.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch4.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ch4,3,0)

        self.socks_host = QLineEdit(self.buttonGroup2,"socks_host")
        self.socks_host.setEnabled(0)
        self.socks_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.socks_host.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.socks_host,4,1)

        self.textLabel5 = QLabel(self.buttonGroup2,"textLabel5")
        self.textLabel5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.textLabel5,0,2)

        self.socks_port = QLineEdit(self.buttonGroup2,"socks_port")
        self.socks_port.setEnabled(0)
        self.socks_port.setMaximumSize(QSize(60,32767))

        layout18.addWidget(self.socks_port,4,3)

        self.ssl_host = QLineEdit(self.buttonGroup2,"ssl_host")
        self.ssl_host.setEnabled(0)
        self.ssl_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.ssl_host.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ssl_host,3,1)

        self.ch3 = QCheckBox(self.buttonGroup2,"ch3")
        self.ch3.setEnabled(0)
        self.ch3.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch3.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ch3,2,0)

        self.gopher_host = QLineEdit(self.buttonGroup2,"gopher_host")
        self.gopher_host.setEnabled(0)
        self.gopher_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.gopher_host.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.gopher_host,2,1)

        self.gopher_port = QLineEdit(self.buttonGroup2,"gopher_port")
        self.gopher_port.setEnabled(0)
        self.gopher_port.setMaximumSize(QSize(60,32767))

        layout18.addWidget(self.gopher_port,2,3)

        self.ch1 = QCheckBox(self.buttonGroup2,"ch1")
        self.ch1.setEnabled(0)
        self.ch1.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.ch1.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ch1,0,0)

        self.ftp_host = QLineEdit(self.buttonGroup2,"ftp_host")
        self.ftp_host.setEnabled(0)
        self.ftp_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.ftp_host.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.ftp_host,1,1)

        self.textLabel5_5 = QLabel(self.buttonGroup2,"textLabel5_5")
        self.textLabel5_5.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_5.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.textLabel5_5,4,2)

        self.textLabel5_4 = QLabel(self.buttonGroup2,"textLabel5_4")
        self.textLabel5_4.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Preferred,0,0,self.textLabel5_4.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.textLabel5_4,3,2)

        self.ftp_port = QLineEdit(self.buttonGroup2,"ftp_port")
        self.ftp_port.setEnabled(0)
        self.ftp_port.setMaximumSize(QSize(60,32767))

        layout18.addWidget(self.ftp_port,1,3)

        self.ssl_port = QLineEdit(self.buttonGroup2,"ssl_port")
        self.ssl_port.setEnabled(0)
        self.ssl_port.setMaximumSize(QSize(60,32767))

        layout18.addWidget(self.ssl_port,3,3)

        self.http_port = QLineEdit(self.buttonGroup2,"http_port")
        self.http_port.setEnabled(0)
        self.http_port.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.http_port.sizePolicy().hasHeightForWidth()))
        self.http_port.setMaximumSize(QSize(60,32767))

        layout18.addWidget(self.http_port,0,3)

        self.http_host = QLineEdit(self.buttonGroup2,"http_host")
        self.http_host.setEnabled(0)
        self.http_host.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Fixed,0,0,self.http_host.sizePolicy().hasHeightForWidth()))

        layout18.addWidget(self.http_host,0,1)

        buttonGroup2Layout.addMultiCellLayout(layout18,3,3,2,3)

        self.rd2 = QRadioButton(self.buttonGroup2,"rd2")

        buttonGroup2Layout.addMultiCellWidget(self.rd2,1,1,0,3)

        Form1Layout.addWidget(self.buttonGroup2,1,0)

        self.languageChange()

        self.resize(QSize(398,432).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.setTabOrder(self.name_edit,self.rd1)
        self.setTabOrder(self.rd1,self.rd2)
        self.setTabOrder(self.rd2,self.rd3)
        self.setTabOrder(self.rd3,self.ch0)
        self.setTabOrder(self.ch0,self.ch1)
        self.setTabOrder(self.ch1,self.http_host)
        self.setTabOrder(self.http_host,self.http_port)
        self.setTabOrder(self.http_port,self.ch2)
        self.setTabOrder(self.ch2,self.ftp_host)
        self.setTabOrder(self.ftp_host,self.ftp_port)
        self.setTabOrder(self.ftp_port,self.ch3)
        self.setTabOrder(self.ch3,self.gopher_host)
        self.setTabOrder(self.gopher_host,self.gopher_port)
        self.setTabOrder(self.gopher_port,self.ch4)
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
        self.warning.setText(QString.null)
        self.textLabel1.setText(i18n("Profile name:"))
        self.buttonGroup2.setTitle(i18n("Options"))
        self.rd1.setText(i18n("Direct connection"))
        self.rd3.setText(i18n("Automatic settings"))
        self.textLabel6.setText(i18n("URL"))
        self.ch0.setText(i18n("Use a general proxy"))
        self.ch5.setText(i18n("SOCKS"))
        self.textLabel5_3.setText(i18n("Port"))
        self.ch2.setText(i18n("Ftp"))
        self.textLabel5_2.setText(i18n("Port"))
        self.ch4.setText(i18n("SSL"))
        self.textLabel5.setText(i18n("Port"))
        self.ch3.setText(i18n("Gopher"))
        self.ch1.setText(i18n("Http"))
        self.textLabel5_5.setText(i18n("Port"))
        self.textLabel5_4.setText(i18n("Port"))
        self.rd2.setText(i18n("Use proxy server"))

