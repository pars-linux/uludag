
from qt import *

import sane

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

        pageStep = self.option.constraint[2]
        self.mult = 1
        if pageStep == 0:
            pageStep = 1
        while pageStep*self.mult < 1:
            self.mult *= 2
        self.slider.setMinValue(self.option.constraint[0]*self.mult)
        self.slider.setMaxValue(self.option.constraint[1]*self.mult)
        self.slider.setPageStep(pageStep*self.mult)
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
            if self.option.type == sane.TYPE_FIXED:
                self.device.__setattr__(self.option.name.replace("-","_"),float(i)/self.mult)
            else:
                self.device.__setattr__(self.option.name.replace("-","_"),i/self.mult)
            print self.option.name, i
        self.emit(PYSIGNAL("stateChanged"),())
        
    def updateState(self):
        self.option = self.device[self.option.name.replace("-","_")]
        if self.option.is_active():
            self.slider.setValue(self.device.__getattr__(self.option.name.replace("-","_"))*self.mult)
            self.setEnabled(self.option.is_settable())
            self.show()
        else:
            self.hide()
