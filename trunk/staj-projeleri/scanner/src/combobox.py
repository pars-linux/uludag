
from qt import *

class ComboBox(QHBox):
    #def __init__(self,parent,name,option,device):
    #    QComboBox.__init__(self,parent,name)
    #    self.option = option
    #    self.device = device
    #    for c in self.option.constraints:
    #        self.insertItem(repr(c))
    #    self.connect(self,SIGNAL("activated(int)"),self.activatedAction)
        
    def __init__(self,rw,parent,name,option,device):
        QHBox.__init__(self,parent,name)
        
        self.label = QLabel(option.title,self,option.title)
        self.comboBox = QComboBox(rw,self,name)
        self.option = option
        self.device = device
        for c in self.option.constraint:
            self.comboBox.insertItem(repr(c))
        self.updateState()
        self.connect(self.comboBox,SIGNAL("activated(int)"),self.activatedAction)    
    
    def activatedAction(self,i):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.device.__setattr__(self.option.name.replace("-","_"),self.option.constraint[i])
            print self.option.name, self.option.constraint[i]
        self.emit(PYSIGNAL("stateChanged"),())

    def updateState(self):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.attr = self.device.__getattr__(self.option.name.replace("-","_"))
            self.comboBox.setCurrentItem(self.option.constraint.index(self.attr))
            self.setEnabled(self.option.is_settable())
            self.show()
        else:
            self.hide()