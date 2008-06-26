# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connsharing.ui'
#
# Created: Prş Haz 26 11:27:35 2008
#      by: The PyQt User Interface Compiler (pyuic) 3.17.4
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
from kdecore import KCmdLineArgs, KApplication
from kdeui import *
from comariface import comlink

i18n = lambda x:x

class connShare(QDialog):
    def __init__(self, parent = None):
        QDialog.__init__(self,parent,None,0,0)

        self.setName("connShare")

        connShareLayout = QGridLayout(self,1,1,11,6,"connShareLayout")

        self.sharecheckBox = QCheckBox(self,"sharecheckBox")

        connShareLayout.addWidget(self.sharecheckBox,0,0)

        self.groupBox1 = QGroupBox(self,"")
        self.groupBox1.setColumnLayout(0,Qt.Vertical)
        self.groupBox1.layout().setSpacing(6)
        self.groupBox1.layout().setMargin(11)
        groupBox1Layout = QGridLayout(self.groupBox1.layout())
        groupBox1Layout.setAlignment(Qt.AlignTop)

        self.textLabel1 = QLabel(self.groupBox1,"textLabel1")

        groupBox1Layout.addWidget(self.textLabel1,0,0)

        self.intcombo = QComboBox(0,self.groupBox1,"intcombo")

        groupBox1Layout.addWidget(self.intcombo,0,1)

        self.sharecombo = QComboBox(0,self.groupBox1,"sharecombo")

        groupBox1Layout.addWidget(self.sharecombo,1,1)

        self.textLabel2 = QLabel(self.groupBox1,"textLabel2")

        groupBox1Layout.addWidget(self.textLabel2,1,0)

        connShareLayout.addWidget(self.groupBox1,1,0)

        self.buttonGroup2 = QButtonGroup(self,"buttonGroup2")
        self.buttonGroup2.setColumnLayout(0,Qt.Vertical)
        self.buttonGroup2.layout().setSpacing(6)
        self.buttonGroup2.layout().setMargin(11)
        buttonGroup2Layout = QHBoxLayout(self.buttonGroup2.layout())
        buttonGroup2Layout.setAlignment(Qt.AlignTop)
        spacer2 = QSpacerItem(200,30,QSizePolicy.Expanding,QSizePolicy.Minimum)
        buttonGroup2Layout.addItem(spacer2)

        self.applyBut = QPushButton(self.buttonGroup2,"applyBut")
        buttonGroup2Layout.addWidget(self.applyBut)

        self.cancelBut = QPushButton(self.buttonGroup2,"cancelBut")
        buttonGroup2Layout.addWidget(self.cancelBut)

        connShareLayout.addWidget(self.buttonGroup2,2,0)

        self.languageChange()

        self.resize(QSize(411,196).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.textLabel1.setBuddy(self.intcombo)
        self.textLabel2.setBuddy(self.sharecombo)
        self.connect(self.sharecheckBox, SIGNAL("stateChanged(int)"), self.slotCheckBox)
        self.connect(self.applyBut, SIGNAL("clicked()"), self.shareConnection)
        self.connect(self.cancelBut, SIGNAL("clicked()"), self.close)


    def languageChange(self):
        self.setCaption(i18n("Internet Connection Sharing"))
        self.sharecheckBox.setText(i18n("Share Internet Connection"))
        self.groupBox1.setTitle(i18n(""))
        self.textLabel1.setText(i18n("Interface that goes to internet"))
        self.textLabel2.setText(i18n("Interface that will share connection"))
        self.buttonGroup2.setTitle(QString.null)
        self.applyBut.setText(i18n("Apply"))
        self.cancelBut.setText(i18n("Cancel"))
    def slotCheckBox(self):
        if not self.sharecheckBox.isOn():
            self.groupBox1.setEnabled(False)
            self.buttonGroup2.setEnabled(False)
        else:
            self.groupBox1.setEnabled(True)
            self.buttonGroup2.setEnabled(True)

    def shareConnection(self):
        int_if = str(self.intcombo.currentText()).split("-")[0]
        shr_if = str(self.intcombo.currentText()).split("-")[0]
        print int_if, shr_if
if __name__ == "__main__":
    appname     = ""
    description = ""
    version     = ""

    KCmdLineArgs.init (sys.argv, appname, description, version)
    a = KApplication ()

    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = connShare()
    a.setMainWidget(w)
    w.show()
    a.exec_loop()
