

from qt import *

class OptionsReadyEvent(QCustomEvent):
    def __init__(self,options,device):
        QCustomEvent.__init__(self,1001);
        self.options = options;
        self.device = device;