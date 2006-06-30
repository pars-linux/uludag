# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'firewall.ui'
#
# Created: Cum Haz 30 11:18:44 2006
#      by: The PyQt User Interface Compiler (pyuic) snapshot-20060407
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from kdecore import KCmdLineArgs, KApplication
from kdeui import *



class MainWindow(QWidget):
    def __init__(self,parent = None,name = None,fl = 0):
        QWidget.__init__(self,parent,name,fl)

        if not name:
            self.setName("widgetFW")


        widgetFWLayout = QGridLayout(self,1,1,KDialog.marginHint(),KDialog.spacingHint(),"widgetFWLayout")

        layout2 = QHBoxLayout(None,0,KDialog.spacingHint(),"layout2")

        self.pushHelp = QPushButton(self,"pushHelp")
        self.pushHelp.setMinimumSize(QSize(100,23))
        self.pushHelp.setAutoMask(0)
        layout2.addWidget(self.pushHelp)
        spacer10 = QSpacerItem(105,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout2.addItem(spacer10)

        self.pushApply = QPushButton(self,"pushApply")
        self.pushApply.setMinimumSize(QSize(100,23))
        self.pushApply.setAutoMask(0)
        layout2.addWidget(self.pushApply)

        self.pushOk = QPushButton(self,"pushOk")
        self.pushOk.setMinimumSize(QSize(100,23))
        self.pushOk.setAutoMask(0)
        layout2.addWidget(self.pushOk)

        self.pushCancel = QPushButton(self,"pushCancel")
        self.pushCancel.setMinimumSize(QSize(100,23))
        self.pushCancel.setAutoMask(0)
        layout2.addWidget(self.pushCancel)

        widgetFWLayout.addLayout(layout2,3,0)

        self.buttonGroup3_3 = QButtonGroup(self,"buttonGroup3_3")
        self.buttonGroup3_3.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.buttonGroup3_3.sizePolicy().hasHeightForWidth()))
        self.buttonGroup3_3.setMinimumSize(QSize(0,0))
        self.buttonGroup3_3.setPaletteBackgroundColor(QColor(231,231,255))
        self.buttonGroup3_3.setFrameShape(QButtonGroup.StyledPanel)
        self.buttonGroup3_3.setFrameShadow(QButtonGroup.Raised)
        self.buttonGroup3_3.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup3_3.layout().setSpacing(KDialog.spacingHint())
        self.buttonGroup3_3.layout().setMargin(KDialog.marginHint())
        buttonGroup3_3Layout = QGridLayout(self.buttonGroup3_3.layout())
        buttonGroup3_3Layout.setAlignment(Qt.AlignTop)

        self.textStatus2 = QLabel(self.buttonGroup3_3,"textStatus2")
        self.textStatus2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.textStatus2.sizePolicy().hasHeightForWidth()))
        self.textStatus2.setMinimumSize(QSize(0,0))
        self.textStatus2.setMaximumSize(QSize(32767,50))
        self.textStatus2.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter | QLabel.AlignLeft)

        buttonGroup3_3Layout.addMultiCellWidget(self.textStatus2,1,1,2,3)

        self.pushStatus = QPushButton(self.buttonGroup3_3,"pushStatus")
        self.pushStatus.setMaximumSize(QSize(180,32767))

        buttonGroup3_3Layout.addWidget(self.pushStatus,1,1)

        self.pixmapFW = QLabel(self.buttonGroup3_3,"pixmapFW")
        self.pixmapFW.setMaximumSize(QSize(48,48))
        self.pixmapFW.setMargin(5)
        self.pixmapFW.setScaledContents(1)

        buttonGroup3_3Layout.addMultiCellWidget(self.pixmapFW,0,1,0,0)

        self.textStatus = QLabel(self.buttonGroup3_3,"textStatus")
        self.textStatus.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.textStatus.sizePolicy().hasHeightForWidth()))
        self.textStatus.setMinimumSize(QSize(0,0))
        self.textStatus.setMaximumSize(QSize(32767,50))
        self.textStatus.setPaletteForegroundColor(QColor(41,182,31))
        self.textStatus.setPaletteBackgroundColor(QColor(231,231,255))
        self.textStatus.setBackgroundOrigin(QLabel.WidgetOrigin)
        self.textStatus.setAlignment(QLabel.AlignVCenter | QLabel.AlignLeft)

        buttonGroup3_3Layout.addMultiCellWidget(self.textStatus,0,0,1,2)

        widgetFWLayout.addWidget(self.buttonGroup3_3,0,0)
        spacer3 = QSpacerItem(16,16,QSizePolicy.Minimum,QSizePolicy.Fixed)
        widgetFWLayout.addItem(spacer3,1,0)

        self.tabWidget = QTabWidget(self,"tabWidget")

        self.tabConnections = QWidget(self.tabWidget,"tabConnections")
        tabConnectionsLayout = QGridLayout(self.tabConnections,1,1,KDialog.marginHint(),KDialog.spacingHint(),"tabConnectionsLayout")

        self.pixmapIncoming = QLabel(self.tabConnections,"pixmapIncoming")
        self.pixmapIncoming.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.pixmapIncoming.sizePolicy().hasHeightForWidth()))
        self.pixmapIncoming.setMinimumSize(QSize(48,48))
        self.pixmapIncoming.setScaledContents(1)

        tabConnectionsLayout.addWidget(self.pixmapIncoming,0,0)

        self.buttonGroup3_2 = QButtonGroup(self.tabConnections,"buttonGroup3_2")
        self.buttonGroup3_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Preferred,0,0,self.buttonGroup3_2.sizePolicy().hasHeightForWidth()))
        self.buttonGroup3_2.setPaletteBackgroundColor(QColor(231,231,255))
        self.buttonGroup3_2.setFrameShape(QButtonGroup.StyledPanel)
        self.buttonGroup3_2.setFrameShadow(QButtonGroup.Raised)
        self.buttonGroup3_2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup3_2.layout().setSpacing(KDialog.spacingHint())
        self.buttonGroup3_2.layout().setMargin(KDialog.marginHint())
        buttonGroup3_2Layout = QGridLayout(self.buttonGroup3_2.layout())
        buttonGroup3_2Layout.setAlignment(Qt.AlignTop)

        self.checkinMail = QCheckBox(self.buttonGroup3_2,"checkinMail")

        buttonGroup3_2Layout.addWidget(self.checkinMail,2,0)

        self.checkinDNS = QCheckBox(self.buttonGroup3_2,"checkinDNS")

        buttonGroup3_2Layout.addWidget(self.checkinDNS,0,0)

        self.checkinWeb = QCheckBox(self.buttonGroup3_2,"checkinWeb")

        buttonGroup3_2Layout.addWidget(self.checkinWeb,1,0)

        self.checkinRemote = QCheckBox(self.buttonGroup3_2,"checkinRemote")

        buttonGroup3_2Layout.addWidget(self.checkinRemote,3,0)

        self.checkinWFS = QCheckBox(self.buttonGroup3_2,"checkinWFS")

        buttonGroup3_2Layout.addWidget(self.checkinWFS,4,0)

        self.checkinIRC = QCheckBox(self.buttonGroup3_2,"checkinIRC")

        buttonGroup3_2Layout.addWidget(self.checkinIRC,5,0)

        self.checkinIM = QCheckBox(self.buttonGroup3_2,"checkinIM")

        buttonGroup3_2Layout.addWidget(self.checkinIM,6,0)

        self.checkinFS = QCheckBox(self.buttonGroup3_2,"checkinFS")

        buttonGroup3_2Layout.addWidget(self.checkinFS,7,0)

        self.checkinFTP = QCheckBox(self.buttonGroup3_2,"checkinFTP")

        buttonGroup3_2Layout.addWidget(self.checkinFTP,8,0)

        tabConnectionsLayout.addMultiCellWidget(self.buttonGroup3_2,2,2,0,1)

        self.textLabel3_2_2 = QLabel(self.tabConnections,"textLabel3_2_2")
        self.textLabel3_2_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.textLabel3_2_2.sizePolicy().hasHeightForWidth()))
        self.textLabel3_2_2.setMinimumSize(QSize(0,0))
        self.textLabel3_2_2.setAlignment(QLabel.AlignVCenter)

        tabConnectionsLayout.addWidget(self.textLabel3_2_2,0,1)

        self.textLabel3_2 = QLabel(self.tabConnections,"textLabel3_2")
        self.textLabel3_2.setSizePolicy(QSizePolicy(QSizePolicy.Preferred,QSizePolicy.Fixed,0,0,self.textLabel3_2.sizePolicy().hasHeightForWidth()))
        self.textLabel3_2.setMinimumSize(QSize(0,0))
        self.textLabel3_2.setAlignment(QLabel.AlignVCenter)

        tabConnectionsLayout.addMultiCellWidget(self.textLabel3_2,1,1,0,1)
        self.tabWidget.insertTab(self.tabConnections,QString.fromLatin1(""))

        self.TabPage = QWidget(self.tabWidget,"TabPage")
        TabPageLayout = QGridLayout(self.TabPage,1,1,KDialog.marginHint(),KDialog.spacingHint(),"TabPageLayout")

        self.groupBox1_3 = QGroupBox(self.TabPage,"groupBox1_3")
        self.groupBox1_3.setColumnLayout(0,Qt.Vertical)
        self.groupBox1_3.layout().setSpacing(KDialog.spacingHint())
        self.groupBox1_3.layout().setMargin(KDialog.marginHint())
        groupBox1_3Layout = QGridLayout(self.groupBox1_3.layout())
        groupBox1_3Layout.setAlignment(Qt.AlignTop)

        self.textLabel1_3 = QLabel(self.groupBox1_3,"textLabel1_3")

        groupBox1_3Layout.addWidget(self.textLabel1_3,0,0)

        self.textLabel1_3_2 = QLabel(self.groupBox1_3,"textLabel1_3_2")

        groupBox1_3Layout.addWidget(self.textLabel1_3_2,1,0)

        self.textLabel1_3_3 = QLabel(self.groupBox1_3,"textLabel1_3_3")

        groupBox1_3Layout.addWidget(self.textLabel1_3_3,2,0)

        self.comboDirection = QComboBox(0,self.groupBox1_3,"comboDirection")
        self.comboDirection.setMaximumSize(QSize(100,32767))

        groupBox1_3Layout.addWidget(self.comboDirection,2,1)

        self.textLabel1_3_3_2 = QLabel(self.groupBox1_3,"textLabel1_3_3_2")

        groupBox1_3Layout.addWidget(self.textLabel1_3_3_2,3,0)

        self.comboAction = QComboBox(0,self.groupBox1_3,"comboAction")
        self.comboAction.setMaximumSize(QSize(100,32767))

        groupBox1_3Layout.addWidget(self.comboAction,3,1)

        self.lineToPort = QLineEdit(self.groupBox1_3,"lineToPort")
        self.lineToPort.setMinimumSize(QSize(50,0))
        self.lineToPort.setMaximumSize(QSize(150,32767))

        groupBox1_3Layout.addMultiCellWidget(self.lineToPort,1,1,4,5)

        self.textLabel2 = QLabel(self.groupBox1_3,"textLabel2")
        self.textLabel2.setMinimumSize(QSize(10,0))
        self.textLabel2.setMaximumSize(QSize(10,32767))

        groupBox1_3Layout.addWidget(self.textLabel2,0,3)

        self.textLabel2_3 = QLabel(self.groupBox1_3,"textLabel2_3")
        self.textLabel2_3.setMinimumSize(QSize(10,0))
        self.textLabel2_3.setMaximumSize(QSize(10,32767))

        groupBox1_3Layout.addWidget(self.textLabel2_3,1,3)

        self.lineFromPort = QLineEdit(self.groupBox1_3,"lineFromPort")
        self.lineFromPort.setMinimumSize(QSize(50,0))
        self.lineFromPort.setMaximumSize(QSize(150,32767))

        groupBox1_3Layout.addMultiCellWidget(self.lineFromPort,0,0,4,5)

        self.lineFromIP = QLineEdit(self.groupBox1_3,"lineFromIP")
        self.lineFromIP.setMinimumSize(QSize(250,0))

        groupBox1_3Layout.addMultiCellWidget(self.lineFromIP,0,0,1,2)

        self.lineToIP = QLineEdit(self.groupBox1_3,"lineToIP")
        self.lineToIP.setMinimumSize(QSize(250,0))

        groupBox1_3Layout.addMultiCellWidget(self.lineToIP,1,1,1,2)
        spacer9 = QSpacerItem(230,16,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1_3Layout.addMultiCell(spacer9,3,3,2,4)

        self.pushAdd = QPushButton(self.groupBox1_3,"pushAdd")
        self.pushAdd.setMinimumSize(QSize(80,0))

        groupBox1_3Layout.addWidget(self.pushAdd,3,5)

        TabPageLayout.addWidget(self.groupBox1_3,0,0)

        self.groupBox4 = QGroupBox(self.TabPage,"groupBox4")
        self.groupBox4.setColumnLayout(0,Qt.Vertical)
        self.groupBox4.layout().setSpacing(KDialog.spacingHint())
        self.groupBox4.layout().setMargin(KDialog.marginHint())
        groupBox4Layout = QGridLayout(self.groupBox4.layout())
        groupBox4Layout.setAlignment(Qt.AlignTop)

        self.listAdvanced = QListView(self.groupBox4,"listAdvanced")
        self.listAdvanced.addColumn(self.__tr("Direction"))
        self.listAdvanced.addColumn(self.__tr("From"))
        self.listAdvanced.addColumn(self.__tr("To"))
        self.listAdvanced.addColumn(self.__tr("Action"))

        groupBox4Layout.addMultiCellWidget(self.listAdvanced,0,1,0,0)

        self.pushRemove = QPushButton(self.groupBox4,"pushRemove")
        self.pushRemove.setMinimumSize(QSize(80,0))

        groupBox4Layout.addWidget(self.pushRemove,0,1)
        spacer10_2 = QSpacerItem(26,56,QSizePolicy.Minimum,QSizePolicy.Expanding)
        groupBox4Layout.addItem(spacer10_2,1,1)

        TabPageLayout.addWidget(self.groupBox4,1,0)
        self.tabWidget.insertTab(self.TabPage,QString.fromLatin1(""))

        self.tabFeatures = QWidget(self.tabWidget,"tabFeatures")
        tabFeaturesLayout = QGridLayout(self.tabFeatures,1,1,KDialog.marginHint(),KDialog.spacingHint(),"tabFeaturesLayout")

        self.groupBox1 = QGroupBox(self.tabFeatures,"groupBox1")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(KDialog.spacingHint())
        self.groupBox1.layout().setMargin(KDialog.marginHint())
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.checkotherICMP = QCheckBox(self.groupBox1,"checkotherICMP")

        groupBox1Layout.addWidget(self.checkotherICMP,0,0)

        tabFeaturesLayout.addWidget(self.groupBox1,0,0)
        spacer2 = QSpacerItem(31,25,QSizePolicy.Minimum,QSizePolicy.Expanding)
        tabFeaturesLayout.addItem(spacer2,2,0)

        self.groupBox1_2 = QGroupBox(self.tabFeatures,"groupBox1_2")
        self.groupBox1_2.setColumnLayout(0,Qt.Vertical)
        self.groupBox1_2.layout().setSpacing(KDialog.spacingHint())
        self.groupBox1_2.layout().setMargin(KDialog.marginHint())
        groupBox1_2Layout = QGridLayout(self.groupBox1_2.layout())
        groupBox1_2Layout.setAlignment(Qt.AlignTop)

        self.textLabel1 = QLabel(self.groupBox1_2,"textLabel1")
        self.textLabel1.setAlignment(QLabel.WordBreak | QLabel.AlignVCenter)

        groupBox1_2Layout.addMultiCellWidget(self.textLabel1,0,0,0,1)

        self.pushLog = QPushButton(self.groupBox1_2,"pushLog")
        self.pushLog.setMaximumSize(QSize(100,32767))

        groupBox1_2Layout.addWidget(self.pushLog,1,0)
        spacer7 = QSpacerItem(171,11,QSizePolicy.Expanding,QSizePolicy.Minimum)
        groupBox1_2Layout.addItem(spacer7,1,1)

        tabFeaturesLayout.addWidget(self.groupBox1_2,1,0)
        self.tabWidget.insertTab(self.tabFeatures,QString.fromLatin1(""))

        widgetFWLayout.addWidget(self.tabWidget,2,0)

        self.languageChange()

        self.resize(QSize(566,622).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Firewall Configuration"))
        QWhatsThis.add(self,self.__tr("Enter the IP address of the "))
        self.pushHelp.setText(self.__tr("&Help"))
        self.pushHelp.setAccel(QKeySequence(self.__tr("Alt+H")))
        self.pushApply.setText(self.__tr("&Apply"))
        self.pushApply.setAccel(QKeySequence(self.__tr("Alt+A")))
        self.pushOk.setText(self.__tr("&Ok"))
        self.pushOk.setAccel(QKeySequence(self.__tr("Alt+O")))
        self.pushCancel.setText(self.__tr("&Cancel"))
        self.pushCancel.setAccel(QKeySequence(self.__tr("Alt+C")))
        self.buttonGroup3_3.setTitle(QString.null)
        self.textStatus2.setText(self.__tr("Click here to stop the firewall and allow all incoming connections."))
        self.pushStatus.setText(self.__tr("&Stop"))
        self.pushStatus.setAccel(QKeySequence(self.__tr("Alt+S")))
        self.textStatus.setText(self.__tr("<b><font size=\"+1\">Firewall is running</font></b>"))
        self.buttonGroup3_2.setTitle(QString.null)
        self.checkinMail.setText(self.__tr("E-mail Services"))
        self.checkinDNS.setText(self.__tr("Domain Name Service (DNS)"))
        self.checkinWeb.setText(self.__tr("Web Services"))
        self.checkinRemote.setText(self.__tr("Remote Login Services"))
        self.checkinWFS.setText(self.__tr("Windows File Sharing Services"))
        self.checkinIRC.setText(self.__tr("Internet Relay Chat Services"))
        self.checkinIM.setText(self.__tr("Instant Messaging Services"))
        self.checkinFS.setText(self.__tr("File Sharing (p2p) Services"))
        self.checkinFTP.setText(self.__tr("File Transfer Services"))
        self.textLabel3_2_2.setText(self.__tr("..."))
        self.textLabel3_2.setText(self.__tr("Allow other computers to access following services on this computer:"))
        self.tabWidget.changeTab(self.tabConnections,self.__tr("Incoming Connections"))
        self.groupBox1_3.setTitle(self.__tr("New Rule"))
        self.textLabel1_3.setText(self.__tr("From:"))
        self.textLabel1_3_2.setText(self.__tr("To:"))
        self.textLabel1_3_3.setText(self.__tr("Direction:"))
        self.comboDirection.clear()
        self.comboDirection.insertItem(self.__tr("In"))
        self.comboDirection.insertItem(self.__tr("Out"))
        self.textLabel1_3_3_2.setText(self.__tr("Action:"))
        self.comboAction.clear()
        self.comboAction.insertItem(self.__tr("Accept"))
        self.comboAction.insertItem(self.__tr("Reject"))
        QToolTip.add(self.comboAction,self.__tr("Accept: The packet is allowed. Reject: The packet is filtered out (i.e deleted)"))
        QToolTip.add(self.lineToPort,self.__tr("Enter the port number here"))
        self.textLabel2.setText(self.__tr(":"))
        self.textLabel2_3.setText(self.__tr(":"))
        QToolTip.add(self.lineFromPort,self.__tr("Enter the port number here"))
        QToolTip.add(self.lineFromIP,self.__tr("Enter the IP address of the host which the packet comes from"))
        QWhatsThis.add(self.lineFromIP,QString.null)
        QToolTip.add(self.lineToIP,self.__tr("Enter the IP address of the machine the packet heads to"))
        self.pushAdd.setText(self.__tr("&Add"))
        self.pushAdd.setAccel(QKeySequence(self.__tr("Alt+A")))
        self.groupBox4.setTitle(self.__tr("Rules"))
        self.listAdvanced.header().setLabel(0,self.__tr("Direction"))
        self.listAdvanced.header().setLabel(1,self.__tr("From"))
        self.listAdvanced.header().setLabel(2,self.__tr("To"))
        self.listAdvanced.header().setLabel(3,self.__tr("Action"))
        self.pushRemove.setText(self.__tr("&Remove"))
        self.pushRemove.setAccel(QKeySequence(self.__tr("Alt+R")))
        self.tabWidget.changeTab(self.TabPage,self.__tr("Advanced"))
        self.groupBox1.setTitle(self.__tr("ICMP"))
        self.checkotherICMP.setText(self.__tr("Block incoming PING (ICMP/8) requests."))
        self.groupBox1_2.setTitle(self.__tr("Firewall Logs"))
        self.textLabel1.setText(self.__tr("Firewall logs offer a visual way of understanding what happens. Click the button below to see firewall logs."))
        self.pushLog.setText(self.__tr("&View Logs"))
        self.pushLog.setAccel(QKeySequence(self.__tr("Alt+V")))
        self.tabWidget.changeTab(self.tabFeatures,self.__tr("Other Features"))


    def __tr(self,s,c = None):
        return qApp.translate("MainWindow",s,c)

if __name__ == "__main__":
    appname     = ""
    description = ""
    version     = ""

    KCmdLineArgs.init (sys.argv, appname, description, version)
    a = KApplication ()

    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = MainWindow()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
