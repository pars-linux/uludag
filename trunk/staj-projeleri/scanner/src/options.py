
from qt import *

import sane
from labeledline import *
from option import *
from optionsthread import *

class Options(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        #self.optFrame = QWidget(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,False))
        self.setMinimumSize(QSize(350,410))
        self.setMaximumSize(QSize(350,32767))
        self.hLayout = QHBoxLayout(self)
        
        self.tabWidget = QTabWidget(self,"tabWidget")
        self.tabWidget.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.tabWidget.sizePolicy().hasHeightForWidth()))
        self.tabWidget.setMinimumSize(QSize(350,410))
        self.tabWidget.setMaximumSize(QSize(350,32767))
        self.hLayout.addWidget(self.tabWidget)
        
        self.tab = QScrollView(self.tabWidget,"scrollView")
        self.tabViewport = QWidget(self.tab.viewport(),"tab")
        self.tabViewport.setMinimumWidth(328);
        #self.tabViewport.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.tabWidget.sizePolicy().hasHeightForWidth()))
        self.tab.viewport().setPaletteBackgroundColor(self.tabViewport.paletteBackgroundColor())
        self.tab.viewport().setPaletteForegroundColor(QColor(0,0,0))
        self.tabLayout = QVBoxLayout(self.tabViewport)
        
        self.tab.addChild(self.tabViewport)
        
        self.devices = sane.get_devices()
        
        self.deviceSelectBox = QGroupBox(1,Qt.Horizontal,"Devices",self.tabViewport,"deviceSelectBox")
        self.deviceSelectBox.setFlat(True)
        self.tabLayout.addWidget(self.deviceSelectBox)
        
        self.deviceSelect = QComboBox(False,self.deviceSelectBox,"deviceSelect")
        
        self.deviceSelect.insertItem("Select a Device")
        
        for device in self.devices:
            self.deviceSelect.insertItem(device[1] + " " + device[2])
        
        self.connect(self.deviceSelect,SIGNAL("activated(int)"),self.deviceSelected)

        self.opt = None
        
        self.tabWidget.insertTab(self.tab,QString.fromLatin1(""))

        self.tab_2 = QWidget(self.tabWidget,"tab_2")
                
        self.tabWidget.insertTab(self.tab_2,QString.fromLatin1(""))
        
        self.languageChange()
        
        self.device = None

    def languageChange(self):
        self.tabWidget.changeTab(self.tab,self.__tr("Basic Settings"))
        self.tabWidget.changeTab(self.tab_2,self.__tr("Advanced Settings"))
        
    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
    
    def updateOptions(self):
        print "updating options"
        for option in self.optionList:
            option.widget.updateState()
    
    def deviceSelected(self,no):
        self.clearOptions()
        if no > 0:
            self.opt = QWidget(self.tabViewport)
            self.tabLayout.addWidget(self.opt)
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
            if option[4] == sane.TYPE_GROUP:
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
        if self.opt != None:
            self.tabLayout.remove(self.opt)
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
            