# -*- coding: utf-8 -*-

from qt import *
from kdecore import *
from kdeui import *
from kfile import *


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
        self.setCaption(self.__tr("Scan Result"))
        self.saveAllButton.setText(self.__tr("Save All"))
        self.saveSelectedButton.setText(self.__tr("Save Selected"))
        self.cancelButton.setText(self.__tr("Cancel"))


    def __tr(self,s,c = None):
        return qApp.translate("ScanResultMulti",s,c)
    
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
            
    def saveAll(self):
        saved = 0
        total = 0
        outputFormats = QImageIO.outputFormats()
	temp = "*.png|PNG-Files\n*.JPEG *.jpg|JPEG-Files"
	fileName = unicode(KFileDialog.getSaveFileName("",temp,self,"Save As"))
	if (fileName != ""):
		tmp = fileName.rsplit('.',1)
		for item in self.items:
			total+=1
			#tmp = fileName.rsplit('.',1)
			format = None
			if len(tmp) == 1:
				fileName = tmp[0]
			if len(tmp) == 2:
				fileName, extension = tmp[0],tmp[1]
				if extension.lower() == "jpg":
					format = "JPEG"
				if extension.upper() in outputFormats:
					format = extension.upper()
					fileName += saved.__str__() + "." + extension
			if format == None:
				format = "PNG"
				fileName += saved.__str__() + "." + format.lower()
			if self.pixmapLabel.pixmap().save(fileName,str(format)):
				saved+=1
			
		KMessageBox.information(self,repr(saved) +" of "+ repr(total) + " file(s) successfully saved.","Save Result")
                
    def saveSelected(self):
        saved = 0
        total = 0
        outputFormats = QImageIO.outputFormats()
	temp = "*.png|PNG-Files\n*.JPEG *.jpg|JPEG-Files"
	fileName = unicode(KFileDialog.getSaveFileName("",temp,self,"Save As"))
	if (fileName != ""):
		tmp = fileName.rsplit('.',1)
		for item in self.items:
			if item.isSelected():
				total+=1
				#tmp = fileName.rsplit('.',1)
				format = None
				if len(tmp) == 1:
					fileName = tmp[0]
				if len(tmp) == 2:
					fileName, extension = tmp[0],tmp[1]
					if extension.lower() == "jpg":
						format = "JPEG"
					if extension.upper() in outputFormats:
						format = extension.upper()
						fileName += saved.__str__() + "." + extension
				if format == None:
					format = "PNG"
					fileName += saved.__str__() + "." + format.lower()
				if self.pixmapLabel.pixmap().save(fileName,str(format)):
					saved+=1
				
		KMessageBox.information(self,repr(saved) +" of "+ repr(total) + " file(s) successfully saved.","Save Result")