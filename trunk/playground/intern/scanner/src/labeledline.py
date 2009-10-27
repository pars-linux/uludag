
from qt import *

class LabeledLine(QWidget):
    def __init__(self,parent,labelText):
        QWidget.__init__(self,parent)
        
        self.layout = QHBoxLayout(self)
        
        self.label = QLabel(labelText,self,"label")
        self.layout.addWidget(self.label)
        
        self.line = QFrame(self)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(self.line)