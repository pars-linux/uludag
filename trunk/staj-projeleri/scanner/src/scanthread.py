
#from threading import Thread

from qt import *
from scanevent import *

import sane

class ScanThread(QThread):
    def __init__(self,parent, device):
        QThread.__init__(self)
	self.device = device
        self.parent = parent
	self.image = None
	
    def run(self):
	self.device.start()
	#self.emit(PYSIGNAL("sigScanProgress"),0)
	self.image = self.device.snap()
	
	qApp.postEvent(self.parent,ScanEvent(self.image))
	
    def getImage(self):
	return self.image
	
	
class PreviewThread(QThread):
    def __init__(self,parent, device):
        QThread.__init__(self)
	self.device = device
        self.parent = parent
	self.image = None
        
    def run(self):
	self.device.start()
	self.image = self.device.snap()

	qApp.postEvent(self.parent,PreviewEvent(self.image))
	
    def getImage(self):
	return self.image
    
class StopThread(QThread):
    def __init__(self,parent, device):
	QThread.__init__(self)
	self.parent = parent
	self.device = device
	
    def run(self):
	self.device.cancel()
	qApp.postEvent(self.parent,StopEvent())