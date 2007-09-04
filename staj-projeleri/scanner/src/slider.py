
from qt import *

class Slider(QVBox):
    #def __init__(self,parent,name,option,device):
    #    QSlider.__init__(self,parent,name)
    #    self.option = option
    #    self.device = device
    #    self.setMinValue(self.option.constraint[0])
    #    self.setMaxValue(self.option.constraint[1])
    #    self.setPageStep(self.option.constraint[2])
    #    self.setValue(self.device.__getattr__(option.name.replace("-","_")))
    #    self.connect(self,SIGNAL("valueChanged(int)"),self.valueChangedAction)
    
    def __init__(self,orientation,parent,name,option,device):
        QVBox.__init__(self,parent,name)
        
        self.label = QLabel(option.title,self,option.title)
        
        self.slider = QSlider(orientation,self,name)
        self.option = option
        self.device = device
        self.slider.setMinValue(self.option.constraint[0])
        self.slider.setMaxValue(self.option.constraint[1])
        self.slider.setPageStep(self.option.constraint[2])
        self.updateState()
        self.connect(self.slider,SIGNAL("valueChanged(int)"),self.valueChangedAction)
    
    #def __init__(self,min,max,step,value,orientation,parent,name,option,device):
    #    QSlider.__init__(self,min,max,step,value,orientation,parent,name)
    #    self.option = option
    #    self.device = device
    #    self.connect(self,SIGNAL("valueChanged(int)"),self.valueChangedAction)
    
    
    def valueChangedAction(self,i):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.device.__setattr__(self.option.name.replace("-","_"),i)
            print self.option.name, i
        self.emit(PYSIGNAL("stateChanged"),())
        
    def updateState(self):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.slider.setValue(self.device.__getattr__(self.option.name.replace("-","_")))
            self.setEnabled(self.option.is_settable())
            self.show()
        else:
            self.hide()
