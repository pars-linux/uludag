
from qt import *

class CheckBox(QCheckBox):
    #def __init__(self,parent,name,option,device):
    #    QCheckBox.__init__(self,parent,name)
    #    self.option = option
    #    self.device = device
    #    self.connect(self,SIGNAL("toggled(bool)"),self.toggledAction)
        
    def __init__(self,text,parent,name,option,device):
        QCheckBox.__init__(self,text,parent,name)
        self.option = option
        self.device = device
        self.updateState()
        self.connect(self,SIGNAL("toggled(bool)"),self.toggledAction)
        
    def toggledAction(self,b):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.device.__setattr__(self.option.name.replace("-","_"),b)
            print self.option.name, b
        self.emit(PYSIGNAL("stateChanged"),())
        
    def updateState(self):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.setChecked(self.device.__getattr__(self.option.name.replace("-","_")))
            self.setEnabled(self.option.is_settable())
            self.show()
        else:
            self.hide()
            