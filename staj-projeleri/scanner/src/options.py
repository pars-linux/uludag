
from qt import *

import sane
from labeledline import *
from option import *
from optionsthread import *
from combobox import *


class Options(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,False))
        self.setMinimumSize(QSize(350,410))
        self.setMaximumSize(QSize(350,32767))
        self.hLayout = QHBoxLayout(self)
        
        self.tabWidget = QTabWidget(self,"tabWidget")
        self.tabWidget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.tabWidget.sizePolicy().hasHeightForWidth()))
        self.tabWidget.setMinimumSize(QSize(350,410))
        self.tabWidget.setMaximumSize(QSize(350,32767))
        self.hLayout.addWidget(self.tabWidget)

        self.basicTab = QScrollView(self.tabWidget,"basicTab")
        self.basicTabViewport = QWidget(self.basicTab.viewport(),"basicTab")
        self.basicTabViewport.setMinimumWidth(328);
        self.basicTab.viewport().setPaletteBackgroundColor(self.basicTabViewport.paletteBackgroundColor())
        self.basicTab.viewport().setPaletteForegroundColor(QColor(0,0,0))
        self.basicTabLayout = QVBoxLayout(self.basicTabViewport)
        
        self.basicTab.addChild(self.basicTabViewport)
        
        self.basicOptionsBox = QGroupBox(1,Qt.Horizontal,"Basic Options",self.basicTabViewport,"basicOptionsBox")
        self.basicOptionsBox.setFlat(True)
        self.basicTabLayout.addWidget(self.basicOptionsBox)
        
        self.scanMode = ComboBox("Scan Mode",False,self.basicOptionsBox,"combobox")
        
        self.resolution = ComboBox("Resolution",False,self.basicOptionsBox,"combobox")
        
        self.tabWidget.insertTab(self.basicTab,QString.fromLatin1(""))
        
        self.advancedTab = QScrollView(self.tabWidget,"scrollView")
        self.advancedTabViewport = QWidget(self.advancedTab.viewport(),"advancedTab")
        self.advancedTabViewport.setMinimumWidth(328);
        self.advancedTab.viewport().setPaletteBackgroundColor(self.advancedTabViewport.paletteBackgroundColor())
        self.advancedTab.viewport().setPaletteForegroundColor(QColor(0,0,0))
        self.advancedTabLayout = QVBoxLayout(self.advancedTabViewport)
        
        self.advancedTab.addChild(self.advancedTabViewport)
        
        self.devices = sane.get_devices()
        
        self.deviceSelectBox = QGroupBox(1,Qt.Horizontal,"Devices",self.advancedTabViewport,"deviceSelectBox")
        self.deviceSelectBox.setFlat(True)
        self.advancedTabLayout.addWidget(self.deviceSelectBox)
        
        self.deviceSelect = QComboBox(False,self.deviceSelectBox,"deviceSelect")
        
        self.deviceSelect.insertItem("None")
        
        for device in self.devices:
            self.deviceSelect.insertItem(device[1] + " " + device[2])
        
        self.connect(self.deviceSelect,SIGNAL("activated(int)"),self.deviceSelected)
        
        self.opt = None
        
        self.tabWidget.insertTab(self.advancedTab,QString.fromLatin1(""))

        self.languageChange()
        
        self.device = None

    def languageChange(self):
        self.tabWidget.changeTab(self.advancedTab,self.__tr("Advanced Settings"))
        self.tabWidget.changeTab(self.basicTab,self.__tr("Basic Settings"))
        
    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
    
    def updateOptions(self):
        print "updating options"
        for option in self.optionList:
            option.widget.updateState()
    
    def deviceSelected(self,no):
        self.clearOptions()
        if no > 0:
            self.opt = QWidget(self.advancedTabViewport)
            self.advancedTabLayout.addWidget(self.opt)
            self.optLayout = QVBoxLayout(self.opt)
            
            self.tmpVBox = QVBox(self.opt,"vbox")
            self.loadingLabel = QLabel("Loading...",self.tmpVBox,"loadingLabel")
            self.optLayout.addWidget(self.tmpVBox)

            self.opt.show()
            self.th = OptionsThread(self,self.devices[no-1][0])
            self.th.start()
        else:
            self.emit(PYSIGNAL("noDeviceSelected"),())

    def customEvent(self,event):
        if(event.type() == 1001):
            self.loadOptions(event.options,event.device)

    def loadOptions(self,options,device):
        self.device, self.options = device,options
        
        self.opt.hide()
        
        self.optLayout.remove(self.tmpVBox)
        
        self.groupBoxes = []
        self.optionList = []
        for option in self.options:
            if option[1] == "mode":
                self.basicOptionsBox.removeChild(self.scanMode)
                self.scanMode = Option(self.basicOptionsBox, option, self.device)
                self.optionList.append(self.scanMode)
                self.scanMode = self.scanMode.getWidget(None)
            elif option[1] == "resolution":
                self.basicOptionsBox.removeChild(self.resolution)
                self.resolution = Option(self.basicOptionsBox, option, self.device)
                self.optionList.append(self.resolution)
                self.resolution = self.resolution.getWidget(None)
            elif option[1] == "preview":
                continue
            elif option[4] == sane.TYPE_GROUP:
                groupBox = QGroupBox(1, Qt.Vertical, option[2], self.opt, option[2] + "GroupBox")
                groupBox.setFlat(True)
                self.groupBoxes.append(groupBox)
                self.optLayout.addWidget(groupBox)
            else:
                groupBox.setColumns(groupBox.columns() + 1)
                o = Option(groupBox, option, self.device)
                self.optionList.append(o)
                self.connect(o.widget, PYSIGNAL("stateChanged"), self.updateOptions)
        
        self.opt.show()

        self.emit(PYSIGNAL("newDeviceSelected"),())
    
    def getOptionValues(self):
        retList = []
        for option in self.optionList:
            retList.append(option.getValue())
        return retList
    
    def setOptionValues(self,values):
        if len(values) == len(self.optionList):
            for i in range(0,len(self.optionList)):
                self.optionList[i].setValue(values[i])
    
    def clearOptions(self):
        self.scanMode.setEnabled(False)
        self.resolution.setEnabled(False)
        if self.opt != None:
            self.advancedTabLayout.remove(self.opt)
            self.opt = None
            self.optLayout = None
            if self.device != None:
                self.device.close()
                self.device = None
            self.options = None
            self.groupBoxes = None
            for o in self.optionList:
                self.disconnect(o.widget,PYSIGNAL("stateChanged"),self.updateOptions)
            self.optionList = None
            