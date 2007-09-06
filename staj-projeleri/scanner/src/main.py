# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Prş Eyl 6 10:01:20 2007
#      by: The PyQt User Interface Compiler (pyuic) 3.17.3
#
# WARNING! All changes made in this file will be lost!


import sys
from qt import *
import sane
from scanner import *
import pickle

class Main(QDialog):
    def __init__(self,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

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
                
            radio.setOn(True)
            
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
            self.scanWindow.hide();
            
            self.connect(self.scanWindow.options,PYSIGNAL("newDeviceSelected"),self.showScanWindow)
        
            self.show()
        else:
            MainLayout = QVBoxLayout(self,11,6,"MainLayout")
            label = QLabel("Loading...",self,"label")
            MainLayout.addWidget(label)
            self.scanWindow = ScanWindow()
            self.scanWindow.hide();
            self.connect(self.scanWindow.options,PYSIGNAL("newDeviceSelected"),self.showScanWindow)
            self.openDevice(device)
            
        


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
    a = QApplication(sys.argv)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),a,SLOT("quit()"))
    w = Main()
    a.setMainWidget(w)
    QObject.connect(a,SIGNAL("lastWindowClosed()"),w.quit)
    a.exec_loop()


