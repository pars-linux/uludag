
from qt import *

import sane
from labeledline import *
from checkbox import *
from combobox import *
from slider import *
from lineedit import * 

class Option:
    def __init__(self,parent,option,device):
        self.option = option
        self.device = device
        self.widget = None
        self.getWidget(parent)

    def getWidget(self,parent):
        if self.widget == None:
            if self.option[2] != None:
                self.deviceOption = self.device[self.option[1].replace('-','_')]
                if self.deviceOption.type == sane.TYPE_BOOL:
                    self.widget = CheckBox(self.deviceOption.title,parent,"checkbox",self.deviceOption,self.device)
                elif self.deviceOption.type == sane.TYPE_INT:
                    if isinstance(self.deviceOption.constraint,list):
                        self.widget = ComboBox(False,parent,"combobox",self.deviceOption,self.device)
                    elif isinstance(self.deviceOption.constraint,tuple):
                        self.widget = Slider(Qt.Horizontal,parent,"slider",self.deviceOption,self.device)
                    elif self.deviceOption.constraint == None:
                        self.widget = LineEdit(parent,"lineedit",self.deviceOption,self.device);
                elif self.deviceOption.type == sane.TYPE_FIXED:
                    if isinstance(self.deviceOption.constraint,list):
                        self.widget = ComboBox(False,parent,"combobox",self.deviceOption,self.device)
                    elif isinstance(self.deviceOption.constraint,tuple):
                        self.widget = Slider(Qt.Horizontal,parent,"slider",self.deviceOption,self.device)
                    elif self.deviceOption.constraint == None:
                        self.widget = LineEdit(parent,"lineedit",self.deviceOption,self.device)
                elif self.deviceOption.type == sane.TYPE_STRING:
                    if isinstance(self.deviceOption.constraint,list):
                        self.widget = ComboBox(False,parent,"combobox",self.deviceOption,self.device)
                    elif self.deviceOption.constraint == None:
                        self.widget = LineEdit(parent,"lineedit",self.deviceOption,self.device)
                else:
                    self.widget = QWidget(parent)
            else:
                self.widget = QWidget(parent)
        
        return self.widget
    
    def getValue(self):
        self.deviceOption = self.device[self.deviceOption.name.replace("-","_")]
        if self.deviceOption.is_active():
            attr = self.device.__getattr__(self.deviceOption.name.replace("-","_"))
        else:
            attr = None
        return attr
    
    def setValue(self,value):
        self.deviceOption = self.device[self.deviceOption.name.replace("-","_")]
        if self.deviceOption.is_active():
            self.device.__setattr__(self.deviceOption.name.replace("-","_"),value)