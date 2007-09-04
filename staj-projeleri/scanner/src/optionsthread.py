
#from threading import Thread

from qt import *
from optionsreadyevent import *

import sane
import time

class OptionsThread(QThread):
    def __init__(self,parent,deviceName):
        QThread.__init__(self)
        self.deviceName = deviceName
        self.parent = parent
        
    def run(self):
        self.usleep(10)
        self.device = sane.open(self.deviceName)
        self.options = self.device.get_options()
        qApp.postEvent(self.parent,OptionsReadyEvent(self.options,self.device))
        
    def getDeviceAndOptions(self):
        return self.device,self.options