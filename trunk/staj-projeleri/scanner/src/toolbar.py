
from qt import *

from toolbarimages import *

class Toolbar(QFrame):
    def __init__(self,parent):
        
        self.image0 = QPixmap()
        self.image0.loadFromData(toolbarimage0_data,"PNG")
        self.image1 = QPixmap()
        self.image1.loadFromData(toolbarimage1_data,"PNG")
        
        QFrame.__init__(self,parent,"toolbar")
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(40,410))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

        LayoutWidget = QWidget(self,"layout7")
        LayoutWidget.setGeometry(QRect(5,6,32,400))
        layout7 = QVBoxLayout(LayoutWidget,0,6,"layout7")
        spacer3 = QSpacerItem(20,40,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout7.addItem(spacer3)

        self.previewButton = QToolButton(LayoutWidget,"previewButton")
        self.previewButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.previewButton.sizePolicy().hasHeightForWidth()))
        self.previewButton.setText("P")
	QToolTip.add(self.previewButton,self.__tr("Preview"))
        self.previewButton.setMinimumSize(QSize(30,30))
        self.previewButton.setAutoRaise(1)
        layout7.addWidget(self.previewButton)

        self.scanButton = QToolButton(LayoutWidget,"scanButton")
        self.scanButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.scanButton.sizePolicy().hasHeightForWidth()))
        self.scanButton.setText("S")
	QToolTip.add(self.scanButton,self.__tr("Scan"))
        self.scanButton.setMinimumSize(QSize(30,30))
        #self.scanButton.setIconSet(QIconSet(self.image0))
        self.scanButton.setAutoRaise(1)
        layout7.addWidget(self.scanButton)

        self.fitButton = QToolButton(LayoutWidget,"fitButton")
        self.fitButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.fitButton.sizePolicy().hasHeightForWidth()))
        self.fitButton.setMinimumSize(QSize(30,30))
        self.fitButton.setText("F")
	QToolTip.add(self.fitButton,self.__tr("Fit Scan Area"))
        self.fitButton.setAutoRaise(1)
        layout7.addWidget(self.fitButton)

        self.fitSelectButton = QToolButton(LayoutWidget,"fitSelectButton")
        self.fitSelectButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.fitSelectButton.sizePolicy().hasHeightForWidth()))
        self.fitSelectButton.setMinimumSize(QSize(30,30))
        self.fitSelectButton.setText("FS")
	QToolTip.add(self.fitSelectButton,self.__tr("Fit Selected Area"))
        self.fitSelectButton.setAutoRaise(1)
        layout7.addWidget(self.fitSelectButton)

        self.zoominButton = QToolButton(LayoutWidget,"zoominButton")
        self.zoominButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.zoominButton.sizePolicy().hasHeightForWidth()))
        self.zoominButton.setMinimumSize(QSize(30,30))
        self.zoominButton.setIconSet(QIconSet(self.image0))
	QToolTip.add(self.zoominButton,self.__tr("Zoom In"))	
        self.zoominButton.setAutoRaise(1)
        layout7.addWidget(self.zoominButton)

        self.actualSizeButton = QToolButton(LayoutWidget,"actualSizeButton")
        self.actualSizeButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.actualSizeButton.sizePolicy().hasHeightForWidth()))
        self.actualSizeButton.setMinimumSize(QSize(30,30))
        self.actualSizeButton.setText("AS")
	QToolTip.add(self.actualSizeButton,self.__tr("Actual Size"))
        self.actualSizeButton.setAutoRaise(1)
        layout7.addWidget(self.actualSizeButton)

        self.zoomoutButton = QToolButton(LayoutWidget,"zoomoutButton")
        self.zoomoutButton.setSizePolicy(QSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed,0,0,self.zoomoutButton.sizePolicy().hasHeightForWidth()))
        self.zoomoutButton.setMinimumSize(QSize(30,30))
        self.zoomoutButton.setIconSet(QIconSet(self.image1))
	QToolTip.add(self.zoomoutButton,self.__tr("Zoom Out"))
        self.zoomoutButton.setAutoRaise(1)
        layout7.addWidget(self.zoomoutButton)
        spacer4 = QSpacerItem(20,50,QSizePolicy.Minimum,QSizePolicy.Expanding)
        layout7.addItem(spacer4)

    def __tr(self,s,c = None):
        return qApp.translate("toolbar",s,c)
