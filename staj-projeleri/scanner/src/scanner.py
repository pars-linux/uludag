import sys
from qt import *
import sane

from options import *
from toolbar import *
from previewArea import *
from scanresult import *
from scanresultmulti import *
from extractor import *

class ScanWindow(QMainWindow):
    def __init__(self,parent = None,name = None,fl = 0):
        QMainWindow.__init__(self,parent,name,fl)
        
        sane.init()
        
        self.statusBar()

        if not name:
            self.setName("Scanner")


        self.setCentralWidget(QWidget(self,"qt_central_widget"))

        self.hLayout = QHBoxLayout(self.centralWidget(),11,6,"mainFormLayout")

        self.options = Options(self.centralWidget())
        self.hLayout.addWidget(self.options)
        
        self.connect(self.options,PYSIGNAL("newDeviceSelected"),self.newDeviceSelected)
        self.connect(self.options,PYSIGNAL("noDeviceSelected"),self.noDeviceSelected)

        self.toolbar = Toolbar(self.centralWidget())
        self.hLayout.addWidget(self.toolbar)

        self.previewArea = PreviewArea(self.centralWidget())
        self.hLayout.addWidget(self.previewArea)

        self.connect(self.toolbar.previewButton,SIGNAL("released()"),self.previewScan)
        self.connect(self.toolbar.scanButton,SIGNAL("released()"),self.startScan)
        self.connect(self.toolbar.fitButton,SIGNAL("released()"),self.previewArea.previewImage.fit)
        self.connect(self.toolbar.fitSelectButton,SIGNAL("released()"),self.previewArea.previewImage.fitSelect)
        self.connect(self.toolbar.zoominButton,SIGNAL("released()"),self.previewArea.previewImage.zoomin)
        self.connect(self.toolbar.actualSizeButton,SIGNAL("released()"),self.previewArea.previewImage.zoomactual)
        self.connect(self.toolbar.zoomoutButton,SIGNAL("released()"),self.previewArea.previewImage.zoomout)

        self.connect(self.previewArea.previewImage,PYSIGNAL("selectionCreated"),self.selectArea)

        self.helpContentsAction = QAction(self,"helpContentsAction")
        self.helpIndexAction = QAction(self,"helpIndexAction")
        self.helpAboutAction = QAction(self,"helpAboutAction")

        self.MenuBar = QMenuBar(self,"MenuBar")

        self.helpMenu = QPopupMenu(self)
        self.helpContentsAction.addTo(self.helpMenu)
        self.helpIndexAction.addTo(self.helpMenu)
        self.helpMenu.insertSeparator()
        self.helpAboutAction.addTo(self.helpMenu)
        self.MenuBar.insertItem(QString(""),self.helpMenu,1)

        self.noDeviceSelected()

        self.languageChange()

        self.resize(QSize(744,588).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.helpIndexAction,SIGNAL("activated()"),self.helpIndex)
        self.connect(self.helpContentsAction,SIGNAL("activated()"),self.helpContents)
        self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)

    def exit(self):
        print "exiting"
        sane.exit()

    def languageChange(self):
        self.setCaption(self.__tr("Form1"))
        self.helpContentsAction.setText(self.__tr("Contents"))
        self.helpContentsAction.setMenuText(self.__tr("&Contents..."))
        self.helpContentsAction.setAccel(QString.null)
        self.helpIndexAction.setText(self.__tr("Index"))
        self.helpIndexAction.setMenuText(self.__tr("&Index..."))
        self.helpIndexAction.setAccel(QString.null)
        self.helpAboutAction.setText(self.__tr("About"))
        self.helpAboutAction.setMenuText(self.__tr("&About"))
        self.helpAboutAction.setAccel(QString.null)
        if self.MenuBar.findItem(1):
            self.MenuBar.findItem(1).setText(self.__tr("&Help"))


    def helpIndex(self):
        print "Form1.helpIndex(): Not implemented yet"

    def helpContents(self):
        print "Form1.helpContents(): Not implemented yet"

    def helpAbout(self):
        print "Form1.helpAbout(): Not implemented yet"

    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)

    def newDeviceSelected(self):
        self.toolbar.setEnabled(True)
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
        self.toolbar.setEnabled(False)
        self.previewArea.noImage()
        self.previewArea.setEnabled(False)

    def selectArea(self,ratio_tl_x,ratio_tl_y,ratio_br_x,ratio_br_y):
        if self.options.device != None:
            for option in self.options.optionList:
                if option.deviceOption.is_settable() and option.deviceOption.is_active():
                    if option.deviceOption.name == "tl-x":
                        self.options.device.__setattr__("tl_x",ratio_tl_x * option.deviceOption.constraint[1])
                    if option.deviceOption.name == "tl-y":
                        self.options.device.__setattr__("tl_y",ratio_tl_y * option.deviceOption.constraint[1])
                    if option.deviceOption.name == "br-x":
                        self.options.device.__setattr__("br_x",ratio_br_x * option.deviceOption.constraint[1])
                    if option.deviceOption.name == "br-y":
                        self.options.device.__setattr__("br_y",ratio_br_y * option.deviceOption.constraint[1])
            self.options.updateOptions()

    def previewScan(self):
        if self.options.device != None:
            oldValues = self.options.getOptionValues()
            
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
                    
            self.options.device.start()
    
            im = self.options.device.snap();
     
            self.previewArea.previewImage.setImage(im)
            
            self.options.setOptionValues(oldValues)

    def startScan(self):
        if self.options.device != None:
            self.options.device.start()
    
            im = self.options.device.snap();
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
     
            return
