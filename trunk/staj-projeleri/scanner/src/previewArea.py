
from qt import *
from previewImage import * 

class PreviewArea(QWidget):
    def __init__(self,parent):
        QWidget.__init__(self,parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(280,410))
        self.setMaximumSize(QSize(32767,32767))
        self.layout = QHBoxLayout(self)
        
        self.scrollView1 = QScrollView(self,"scrollView1")
        self.layout.addWidget(self.scrollView1)

        self.previewImage = PreviewImage(self.scrollView1.viewport(),"previewImage")
        self.scrollView1.addChild(self.previewImage)

        self.connect(self.previewImage,PYSIGNAL("needsReposition"),self.reposition)
        
    def reposition(self,x,y):
        self.scrollView1.center(x,y)

    def formEmptyImage(self,x,y):
        self.previewImage.initImage = QImage(x,y,32)
        self.previewImage.fit()
        
    def noImage(self):
        self.previewImage.initImage = QImage()
        self.previewImage.image = QImage()
        self.previewImage.updateGeometry()
        self.previewImage.repaint()