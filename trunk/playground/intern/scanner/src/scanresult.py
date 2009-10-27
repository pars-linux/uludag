# -*- coding: utf-8 -*-
from qt import *
from utility import *

class ScanResult(QDialog):
    def __init__(self,image,parent = None,name = None,modal = 0,fl = 0):
        QDialog.__init__(self,parent,name,modal,fl)

        if not name:
            self.setName("ScanResult")


        ScanResultLayout = QVBoxLayout(self,11,6,"ScanResultLayout")

        self.scrollView = QScrollView(self,"scrollView")
        self.scrollView.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.scrollView.sizePolicy().hasHeightForWidth()))
        self.scrollView.setMinimumSize(QSize(0,0))

        self.pixmapLabel = QLabel(self.scrollView.viewport(),"pixmapLabel")
        self.pixmapLabel.setScaledContents(1)
        self.scrollView.addChild(self.pixmapLabel)
        ScanResultLayout.addWidget(self.scrollView)

        self.pixmapLabel.setPixmap(QPixmap(image))
        
        layout = QHBoxLayout(None,0,6,"layout")
        leftSpacer = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout.addItem(leftSpacer)

        self.saveButton = QPushButton(self,"saveButton")
        layout.addWidget(self.saveButton)

        self.cancelButton = QPushButton(self,"cancelButton")
        layout.addWidget(self.cancelButton)
        rightSpacer = QSpacerItem(40,20,QSizePolicy.Expanding,QSizePolicy.Minimum)
        layout.addItem(rightSpacer)
        ScanResultLayout.addLayout(layout)

        self.languageChange()

        self.resize(QSize(640,480).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.cancelButton,SIGNAL("released()"),self.reject)
        self.connect(self.saveButton,SIGNAL("released()"),self.save)


    def languageChange(self):
        self.setCaption(i18n("Scan Result"))
        self.saveButton.setText(i18n("Save..."))
        self.cancelButton.setText(i18n("Cancel"))


    #def __tr(self,s,c = None):
        #return qApp.translate("ScanResult",s,c)


    def save(self):
        outputFormats = QImageIO.outputFormats()
        filter = ""
        for format in outputFormats:
            if format == "JPEG":
                filter += ";;" + format + "( *." + format.lower() + " *.jpg)"
            else:
                filter += ";;" + format + "( *." + format.lower() + ")"
            
        filter = filter.lstrip(';')
        
        fileDialog =  QFileDialog("~",filter,self,"fileDialog")
        fileDialog.setMode(QFileDialog.AnyFile)
        if fileDialog.exec_loop() == QDialog.Accepted :
            fileName = unicode(fileDialog.selectedFile())
            selectedFilter = str(fileDialog.selectedFilter())
            
            tmp = fileName.rsplit('.',1)
            
            format = None
            
            if len(tmp) == 2:
                fileName, extension = tmp[0],str(tmp[1])

                if extension.lower() == "jpg":
                    extension = "JPEG"
                    
                if extension.upper() in outputFormats:
                    format = extension.upper()
                else:
                    fileName += "." + extension
            
            if format == None:
                format = selectedFilter.split('(',1)[0].upper()

            if format == "JPEG":
                fileName += ".jpg"
            else:
                fileName += "."+format.lower()
            
            if self.pixmapLabel.pixmap().save(fileName,format):
                QMessageBox.information(self,"Save Result","File successfully saved.",QMessageBox.Ok)
            else:
                if QMessageBox.information(self,"Save Result","Save unsuccessful!",QMessageBox.Retry,QMessageBox.Cancel) == QMessageBox.Retry:
                    self.save();
                