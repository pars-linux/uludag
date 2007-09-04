# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanresult.ui'
#
# Created: Sal Ağu 28 14:38:12 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


from qt import *


class ScanResult(QDialog):
    def __init__(self,image,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ScanResult")


        ScanResultLayout = QHBoxLayout(self,11,6,"ScanResultLayout")

        self.scrollView1 = QScrollView(self,"scrollView1")
        self.scrollView1.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.scrollView1.sizePolicy().hasHeightForWidth()))

        self.pixmapLabel1 = QLabel(self.scrollView1.viewport(),"pixmapLabel1")
#        self.pixmapLabel1.setGeometry(QRect(0,0,100,100))
        self.pixmapLabel1.setScaledContents(1)
        self.scrollView1.addChild(self.pixmapLabel1)
        ScanResultLayout.addWidget(self.scrollView1)

        self.pixmapLabel1.setPixmap(QPixmap(image))

        self.languageChange()

        self.resize(QSize(600,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(self.__tr("Scan Result"))


    def __tr(self,s,c = None):
        return qApp.translate("ScanResult",s,c)
