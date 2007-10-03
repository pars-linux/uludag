import sys
from qt import *
from kdecore import *
from kdeui import *
from kfile import *
import sane

from options import *
from toolbar import *
from previewArea import *
from scanresult import *
from scanresultmulti import *
from extractor import *
from progress import *

from scanthread import *

from toolbarimages import *

def loadIcon(name, group=KIcon.MainToolbar):
    return KGlobal.iconLoader().loadIcon(name, group)

class ScanWindow(KMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        KMainWindow.__init__(self,parent,name,fl)
        
        #sane.init()
        
        self.statusBar()
	self.statusBar().message("Ready")

        if not name:
            self.setName("Scanner")

        self.setCentralWidget(QWidget(self,"qt_central_widget"))

        self.hLayout = QHBoxLayout(self.centralWidget(),11,6,"mainFormLayout")

        self.options = Options(self.centralWidget())
        self.hLayout.addWidget(self.options)
        
        self.connect(self.options,PYSIGNAL("newDeviceSelected"),self.newDeviceSelected)
        self.connect(self.options,PYSIGNAL("noDeviceSelected"),self.noDeviceSelected)
	
	self.toolBar()
	#self.toolBar().setBarPos(KToolBar.Left)
	self.previewArea = PreviewArea(self.centralWidget())

	self.toolBar().insertButton(loadIcon("scanner"), 1, SIGNAL("released()"), self.previewScan, True, "Preview")
	self.toolBar().insertButton(loadIcon("scanner"), 2, SIGNAL("released()"), self.startScan, True, "Scan")
	self.toolBar().insertButton(loadIcon("view_remove"), 3, SIGNAL("released()"), self.previewArea.previewImage.fit, True, "Fit Scan Area")
	self.toolBar().insertButton(loadIcon("view_fit_window"), 4, SIGNAL("released()"), self.previewArea.previewImage.fitSelect, True, "Fit Selected Area")
	self.toolBar().insertButton(loadIcon("viewmag+"), 5, SIGNAL("released()"), self.previewArea.previewImage.zoomin, True, "Zoom In")
	self.toolBar().insertButton(loadIcon("viewmag1"), 6, SIGNAL("released()"), self.previewArea.previewImage.zoomactual, True, "Actual Size")
	self.toolBar().insertButton(loadIcon("viewmag-"), 7, SIGNAL("released()"), self.previewArea.previewImage.zoomout, True, "Zoom Out")

        #self.toolbar = Toolbar(self.centralWidget())
        #self.hLayout.addWidget(self.toolbar)

        #self.previewArea = PreviewArea(self.centralWidget())
        self.hLayout.addWidget(self.previewArea)

        #self.connect(self.toolbar.previewButton,SIGNAL("released()"),self.previewScan)
        #self.connect(self.toolbar.scanButton,SIGNAL("released()"),self.startScan)
        #self.connect(self.toolbar.fitButton,SIGNAL("released()"),self.previewArea.previewImage.fit)
        #self.connect(self.toolbar.fitSelectButton,SIGNAL("released()"),self.previewArea.previewImage.fitSelect)
        #self.connect(self.toolbar.zoominButton,SIGNAL("released()"),self.previewArea.previewImage.zoomin)
        #self.connect(self.toolbar.actualSizeButton,SIGNAL("released()"),self.previewArea.previewImage.zoomactual)
        #self.connect(self.toolbar.zoomoutButton,SIGNAL("released()"),self.previewArea.previewImage.zoomout)

        self.connect(self.previewArea.previewImage,PYSIGNAL("selectionCreated"),self.selectArea)
	
	self.progress = Progress(self.centralWidget())
	#self.connect(self.options.device, PYSIGNAL("sigScanProgress"), self.progress.setProgress)
	self.progress.setTotalSteps(0)
	self.progress.hide()
	
	self.connect(self.progress,SIGNAL("canceled()"),self.stopScan)
	
	self.menuBar()
	self.menuBar().insertItem(QString("Help"), self.helpMenu())

        self.noDeviceSelected()

        self.languageChange()

        self.resize(QSize(744,600).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

    def exit(self):
        print "exiting"
        sane.exit()

    def languageChange(self):
        self.setCaption(self.__tr("Scanner"))

    def __tr(self,s,c = None):
        return qApp.translate("Scanner",s,c)

    def newDeviceSelected(self):
        #self.toolbar.setEnabled(True)
	self.toolBar().setEnabled(True)
        self.previewArea.setEnabled(True)
        br_x = br_y = -1
        if self.options.device != None:
            for option in self.options.optionList:
                if option.deviceOption.name == "br-x":
                    br_x = option.deviceOption.constraint[1]
                if option.deviceOption.name == "br-y":
                    br_y = option.deviceOption.constraint[1]
        if br_x != -1 and br_y != -1:
            self.previewArea.formEmptyImage(br_x,br_y)

    def noDeviceSelected(self):
        #self.toolbar.setEnabled(False)
	self.toolBar().setEnabled(False)
        self.previewArea.noImage()
        self.previewArea.setEnabled(False)
	
    def selectArea(self,ratio_tl_x,ratio_tl_y,ratio_br_x,ratio_br_y):
        if self.options.device != None:
            for option in self.options.optionList:
                if option.deviceOption.is_settable() and option.deviceOption.is_active():
                    if ratio_br_x == 0 and ratio_br_y == 0 and ratio_tl_x == 0 and ratio_tl_y == 0:
                        if option.deviceOption.name == "tl-x":
                            self.options.device.__setattr__("tl_x",option.deviceOption.constraint[0])
                        if option.deviceOption.name == "tl-y":
                            self.options.device.__setattr__("tl_y",option.deviceOption.constraint[0])
                        if option.deviceOption.name == "br-x":
                            self.options.device.__setattr__("br_x",option.deviceOption.constraint[1])
                        if option.deviceOption.name == "br-y":
                            self.options.device.__setattr__("br_y",option.deviceOption.constraint[1])
                    else:
                        if option.deviceOption.name == "tl-x":
                            self.options.device.__setattr__("tl_x",option.deviceOption.constraint[0] + ratio_tl_x * (option.deviceOption.constraint[1]-option.deviceOption.constraint[0]))
                        if option.deviceOption.name == "tl-y":
                            self.options.device.__setattr__("tl_y",option.deviceOption.constraint[0] + ratio_tl_y * (option.deviceOption.constraint[1]-option.deviceOption.constraint[0]))
                        if option.deviceOption.name == "br-x":
                            self.options.device.__setattr__("br_x",option.deviceOption.constraint[0] + ratio_br_x * (option.deviceOption.constraint[1]-option.deviceOption.constraint[0]))
                        if option.deviceOption.name == "br-y":
                            self.options.device.__setattr__("br_y",option.deviceOption.constraint[0] + ratio_br_y * (option.deviceOption.constraint[1]-option.deviceOption.constraint[0]))
            self.options.updateOptions()

    def previewScan(self):
        if self.options.device != None:
            qApp.processEvents()
	    self.statusBar().message("Busy")
	    self.progress.show()
            self.oldValues = self.options.getOptionValues()
            
            for option in self.options.optionList:
                if option.deviceOption.is_settable() and option.deviceOption.is_active():
                    if option.deviceOption.name == "preview":
                        self.options.device.__setattr__("preview",1)
                    if option.deviceOption.name == "resolution":
                        self.options.device.__setattr__("resolution",min(option.deviceOption.constraint))
                    if option.deviceOption.name == "tl-x":
                        self.options.device.__setattr__("tl_x",min(option.deviceOption.constraint))
                    if option.deviceOption.name == "tl-y":
                        self.options.device.__setattr__("tl_y",min(option.deviceOption.constraint))
                    if option.deviceOption.name == "br-x":
                        self.options.device.__setattr__("br_x",max(option.deviceOption.constraint))
                    if option.deviceOption.name == "br-y":
                        self.options.device.__setattr__("br_y",max(option.deviceOption.constraint))
                    
            #self.options.device.start()
     
            #im = self.options.device.snap();
     	    self.previewThread = PreviewThread(self, self.options.device)
	    self.previewThread.start()
	    #self.previewThread.work(self.options)
            #self.previewArea.previewImage.setImage(im)
            
            #self.options.setOptionValues(oldValues)
	    #self.statusBar().message("Ready")
	    
	    
    def stopScan(self):
	if self.options.device != None:
		#self.options.device.cancel()
		self.stopThread = StopThread(self, self.options.device)
		self.stopThread.start()
		#qApp.wakeUpGuiThread()
		qApp.processEvents()
		self.progress.setLabelText("<p align=\"center\">Stopping</p>")
		#self.statusBar().message("Ready")
		#self.progress.hide()
		
    def backToNormal(self):
	self.progress.setLabelText("<p align=\"center\">Scanning in progress</p>")
	self.statusBar().message("Ready")
	self.progress.hide()

    def customEvent(self,event):
        if(event.type() == 1002):
            self.createScanWindow(event.image)
	if(event.type() == 1003):
	    self.createPreview(event.image)
	if(event.type() == 1004):
	    self.backToNormal()
	    
    def createScanWindow(self, im):
            self.maxDiff = 20
            self.aveRgb = 0x222625
            self.minSize = 90000
            self.enableExtract = True
            if self.enableExtract:
                extract(im,self.maxDiff,self.aveRgb,self.minSize)
                s = ScanResultMulti(self,"scanResultMulti",1)
                tmpImage = QImage()
                while(nextImage(tmpImage)):
                    s.addImage(tmpImage)
            else:
                s = ScanResult(im,self,"scanResult",1)
	    s.show()
	    #self.progress.setProgress(100)
	    self.progress.hide()
	    self.statusBar().message("Ready")
	    
    def createPreview(self, im):
            self.statusBar().message("Ready")
	    self.progress.hide()
	    self.previewArea.previewImage.setImage(im)
            self.options.setOptionValues(self.oldValues)

    def startScan(self):
        if self.options.device != None:
	    self.statusBar().message("Busy")
	    qApp.processEvents()
	    self.progress.show()
	    #self.progress.setProgress(0)
	    #self.hide()
	    
	    #self.options.device.start()
            #im = self.options.device.snap()
	    
	    self.scanThread = ScanThread(self, self.options.device)
	    self.scanThread.start()
	    #self.scanThread.work(self.options)
	    #while(self.worker.finished() == False):
		#pass
	    
	    #im = self.scanThread.getImage()
	    
	    #qApp.processEvents()
	    #qEventLoop.processEvents(AllEvents,500)
	    
	    
	    
            #self.maxDiff = 20
            #self.aveRgb = 0x222625
            #self.minSize = 90000
            #self.enableExtract = True
            #if self.enableExtract:
                #extract(im,self.maxDiff,self.aveRgb,self.minSize)
                #s = ScanResultMulti(self,"scanResultMulti",1)
                #tmpImage = QImage()
                #while(nextImage(tmpImage)):
                    #s.addImage(tmpImage)
            #else:
                #s = ScanResult(im,self,"scanResult",1)
            
	    #self.progress.setProgress(100)
            #s.show()
	    #self.statusBar().message("Ready")
	    #self.progress.reset()
	    #self.show()
	    #self.progress.hide()
     
            #return
