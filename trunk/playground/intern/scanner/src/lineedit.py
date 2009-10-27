
from qt import *

class LineEdit(QHBox):
    def __init__(self,parent,name,option,device):
        QHBox.__init__(self,parent,name)
        
        self.label = QLabel(option.title,self,option.title)
        
        self.lineEdit = QLineEdit(self,name)
        self.option = option
        self.device = device
        self.updateState()
        self.connect(self.lineEdit,SIGNAL("returnPressed()"),self.returnPressedAction)
        
    def returnPressedAction(self):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.device.__setattr__(self.option.name.replace("-","_"),self.lineEdit.text())
            print self.option.name, self.text()
        self.emit(PYSIGNAL("stateChanged"),())
        
    def updateState(self):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.lineEdit.setText(repr(self.device.__getattr__(self.option.name.replace("-","_"))))
            self.setEnabled(self.option.is_settable())
            self.show()
        else:
            self.hide()