# -*- coding: utf-8 -*-

from qt import *
from kdecore import *
from kdeui import *
from kfile import *
from scanthread import *
from utility import *


class ScanResultMulti(KDialog):
    def __init__(self,parent = None,name = None,modal = 1,fl = 0):
        KDialog.__init__(self,parent,name,modal,fl)

        self.pixmaps = []
        self.items = []
        
        if not name:
            self.setName("ScanResultMulti")


        ScanResultMultiLayout = QVBoxLayout(self,11,6,"ScanResultMultiLayout")

        toplayout = QHBoxLayout(None,0,6,"toplayout")

        self.iconView = QIconView(self,"iconView")
        self.iconView.setMinimumSize(QSize(130,0))
        self.iconView.setMaximumSize(QSize(130,32767))
        self.iconView.setHScrollBarMode(QIconView.AlwaysOff)
        self.iconView.setSelectionMode(QIconView.Extended)
        self.iconView.setItemTextPos(QIconView.Bottom)
        self.iconView.setItemsMovable(0)
        toplayout.addWidget(self.iconView)

        self.scrollView = QScrollView(self,"scrollView")
        self.scrollView.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.scrollView.sizePolicy().hasHeightForWidth()))

        self.pixmapLabel = QLabel(self.scrollView.viewport(),"pixmapLabel")
        self.pixmapLabel.setGeometry(QRect(0,0,100,100))
        self.pixmapLabel.setScaledContents(1)
        self.scrollView.addChild(self.pixmapLabel)
        toplayout.addWidget(self.scrollView)
        ScanResultMultiLayout.addLayout(toplayout)

        bottomlayout = QHBoxLayout(None,0,6,"bottomlayout")
        leftspacer = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        bottomlayout.addItem(leftspacer)

        self.saveAllButton = QPushButton(self,"saveAllButton")
        bottomlayout.addWidget(self.saveAllButton)

        self.saveSelectedButton = QPushButton(self,"saveSelectedButton")
        bottomlayout.addWidget(self.saveSelectedButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        bottomlayout.addWidget(self.cancelButton)
        rightspacer = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        bottomlayout.addItem(rightspacer)
        ScanResultMultiLayout.addLayout(bottomlayout)

        self.connect(self.iconView,SIGNAL("currentChanged(QIconViewItem*)"),self.loadPixmapOf)
        self.connect(self.cancelButton,SIGNAL("released()"),self.reject)
        self.connect(self.saveAllButton,SIGNAL("released()"),self.saveAll)
        self.connect(self.saveSelectedButton,SIGNAL("released()"),self.saveSelected)
        self.languageChange()

        self.resize(QSize(640,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)


    def languageChange(self):
        self.setCaption(i18n("Scan Result"))
        self.saveAllButton.setText(i18n("Save All"))
        self.saveSelectedButton.setText(i18n("Save Selected"))
        self.cancelButton.setText(i18n("Cancel"))


    #def __tr(self,s,c = None):
        #return qApp.translate("ScanResultMulti",s,c)
    
    def addImage(self,image):
        if(not image.isNull()):
            self.pixmaps.append(QPixmap(image))
            item = QIconViewItem(self.iconView,"image"+repr(len(self.pixmaps))+".png",QPixmap(image.smoothScale(100,100,QImage.ScaleMin)))
            item.setRenameEnabled(True)
            self.items.append(item)

    def loadPixmapOf(self,item):
        if item != 0:
            self.pixmapLabel.setPixmap(self.pixmaps[item.index()])
        else:
            self.pixmapLabel.clear()

    def customEvent(self,event):
        if(event.type() == 1005):
	    self.saveFinished(event.total, event.saved)

    def saveFinished(self, total, saved):
	    if total != 0:
	    	KMessageBox.information(self,repr(saved) +" of "+ repr(total) + " file(s) successfully saved.","Save Result")
	    self.setCaption(i18n("Scan Result"))
	    self.saveAllButton.setEnabled(True)
            self.saveSelectedButton.setEnabled(True)
            self.cancelButton.setEnabled(True)
            
    def saveAll(self):
	#output = QImageIO.outputFormats()
	#temp = ""
	#for i in output:
		#temp += "*." + i + "\n"
		##if i != output.getLast():
			##temp += "\n"
	temp = i18n("*.png|PNG-Files\n*.JPEG *.jpg|JPEG-Files\n*.bmp|Bitmap-Files")
	fileName = unicode(KFileDialog.getSaveFileName("",temp,self,i18n("Save As")))
	self.setCaption(i18n("Please Wait"))
	self.saveAllButton.setEnabled(False)
        self.saveSelectedButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
	self.saveThread = SaveThread(self, fileName)
	self.saveThread.start()
                
    def saveSelected(self):
	temp = i18n("*.png|PNG-Files\n*.JPEG *.jpg|JPEG-Files\n*.bmp|Bitmap-Files")
	fileName = unicode(KFileDialog.getSaveFileName("",temp,self,i18n("Save As")))
	self.setCaption(i18n("Please Wait"))
	self.saveAllButton.setEnabled(False)
        self.saveSelectedButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
	self.saveThread = SaveSelectedThread(self, fileName)
	self.saveThread.start()
	