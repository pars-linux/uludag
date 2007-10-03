# -*- coding: utf-8 -*-

import sys
from qt import *
from kdecore import *
from kdeui import *
from kfile import *
import sane
from scanner import *
import pickle

version = '0.1'
description = "Scanner Interface"

def loadIcon(name, group=KIcon.Desktop):
    return KGlobal.iconLoader().loadIcon(name, group)

def loadIconSet(name, group=KIcon.Desktop):
        return KGlobal.iconLoader().loadIconSet(name, group)

def AboutData():
   about_data = KAboutData(
        'scanner',
        'Scanner',
        version,
        description,
        KAboutData.License_GPL,
        '(C) 2007 UEKAE/TÜBİTAK',
        None,
        None,
        'bugzilla@pardus.org.tr')
   about_data.addAuthor("Barış Can Daylık", "Main Developer", None)
   about_data.addAuthor("Aslı Okur", "Developer and Current Maintainer", "asliokur@yahoo.com")
   return about_data

class Main(KDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        KDialog.__init__(self,parent,name,modal,fl)
	self.connect(kapp, SIGNAL("shutDown()"), self.slotQuit)
	self.setIcon(loadIcon("scanner"))

        if not name:
            self.setName("Main")

        sane.init()
        
        self.devices = sane.get_devices()
        
        try:
            f = open("defaultdevice","r")
        except:
            f = None
            
        try:
            if f != None:
                device = pickle.load(f)
        except:
            f = None
            
        if f == None or not device in self.devices:
        
            MainLayout = QVBoxLayout(self,11,6,"MainLayout")
    
            self.devicesGroup = QButtonGroup(self,"devices")
            self.devicesGroup.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.devicesGroup.sizePolicy().hasHeightForWidth()))
            self.devicesGroup.setColumnLayout(0,Qt.Vertical)
            self.devicesGroup.layout().setSpacing(6)
            self.devicesGroup.layout().setMargin(11)
            devicesLayout = QVBoxLayout(self.devicesGroup.layout())
            devicesLayout.setAlignment(Qt.AlignTop)
    
            for device in self.devices:
                print device
                radio = QRadioButton(self.devicesGroup,"device")
                radio.setText(device[1] + " " + device[2])
                devicesLayout.addWidget(radio)
                
            try:
                radio.setOn(True)
            except:
                pass
            
            MainLayout.addWidget(self.devicesGroup)
    
            layout1 = QHBoxLayout(None,0,6,"layout1")
            spacer = QSpacerItem(91,21,QSizePolicy.Expanding,QSizePolicy.Minimum)
            layout1.addItem(spacer)
    
            self.setDefault = QCheckBox(self,"setDefault")
            MainLayout.addWidget(self.setDefault)
    
            self.OKButton = QPushButton(self,"OKButton")
            layout1.addWidget(self.OKButton)
    
            self.connect(self.OKButton,SIGNAL("released()"),self.openDevice)
    
            self.cancelButton = QPushButton(self,"cancelButton")
            layout1.addWidget(self.cancelButton)
            MainLayout.addLayout(layout1)
            
            self.connect(self.cancelButton,SIGNAL("released()"),self.reject)
    
            self.languageChange()
    
            self.resize(self.minimumSizeHint())
            self.clearWState(Qt.WState_Polished)
    
            self.scanWindow = ScanWindow()
            self.scanWindow.hide()
            
            self.connect(self.scanWindow.options,PYSIGNAL("newDeviceSelected"),self.showScanWindow)
        
            self.show()
        else:
            MainLayout = QVBoxLayout(self,11,6,"MainLayout")
            label = QLabel("Loading...",self,"label")
            MainLayout.addWidget(label)
            self.scanWindow = ScanWindow()
            self.scanWindow.hide()
            self.connect(self.scanWindow.options,PYSIGNAL("newDeviceSelected"),self.showScanWindow)
            self.openDevice(device)
            
        

    def slotQuit(self):
	#sane.exit()
	self.deleteLater()
        kapp.quit()

    def languageChange(self):
        self.setCaption(self.__tr("Please Select a Device"))
        self.devicesGroup.setTitle(self.__tr("Select Device"))
        self.setDefault.setText("Use as default.")
        self.OKButton.setText(self.__tr("OK"))
        self.cancelButton.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("Main",s,c)

    def quit(self):
        sane.exit()
	#self.queryExit()
        
    def openDevice(self,device = None):
        if device == None:
            if self.setDefault.isChecked():
                f=open('defaultdevice','w')
                pickle.dump(self.devices[self.devicesGroup.selectedId()],f)
            self.hide()
            self.scanWindow.options.deviceSelect.setCurrentItem(self.devicesGroup.selectedId()+1)
            self.scanWindow.options.deviceSelected(self.devicesGroup.selectedId()+1)
        else:
            self.hide()
            index = self.devices.index(device)
            self.scanWindow.options.deviceSelect.setCurrentItem(index+1)
            self.scanWindow.options.deviceSelected(index+1)

    def showScanWindow(self):
        self.scanWindow.show()
        

if __name__ == "__main__":
    global kapp
    #a = KApplication(sys.argv,"")
    about_data = AboutData()
    KCmdLineArgs.init(sys.argv,about_data)
    kapp = KUniqueApplication(True, True, True)
    #QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    mainForm = Main()
    kapp.setMainWidget(mainForm)
    #QObject.connect(a, SIGNAL("aboutToQuit()"), mainForm.quit)
    #QObject.connect(a, SIGNAL("aboutToQuit()"), a, SLOT("quit()"))
    #QObject.connect(a, SIGNAL("lastWindowClosed()"),mainForm.quit)
    #a.exec_loop()
    sys.exit(kapp.exec_loop())
    
    #a = QApplication(sys.argv)
    #QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    #mainForm = Main()
    #a.setMainWidget(mainForm)
    #QObject.connect(a,SIGNAL("lastWindowClosed()"),mainForm.quit)
    #a.exec_loop()


