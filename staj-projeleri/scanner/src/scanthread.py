
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
	
class SaveThread(QThread):
    def __init__(self, parent, fileName):
	QThread.__init__(self)
	self.parent = parent
	self.fileName = fileName
	self.total = 0
	self.saved = 0
	
    def run(self):
	outputFormats = QImageIO.outputFormats()
	if (self.fileName != ""):
		tmp = self.fileName.rsplit('.',1)
		for item in self.parent.items:
			self.total+=1
			#tmp = fileName.rsplit('.',1)
			format = None
			if len(tmp) == 1:
				fileName = tmp[0]
			if len(tmp) == 2:
				fileName, extension = tmp[0],tmp[1]
				if extension.lower() == "jpg":
					format = "JPEG"
				if extension.upper() in outputFormats:
					format = extension.upper()
					if self.saved == 0:
						fileName += "." + extension
					else:
						fileName += self.saved.__str__() + "." + extension
			if format == None:
				format = "PNG"
				if self.saved == 0:
					fileName += "." + format.lower()
				else:
					fileName += self.saved.__str__() + "." + format.lower()
			if self.parent.pixmapLabel.pixmap().save(fileName,str(format)):
				self.saved+=1
	
	qApp.postEvent(self.parent, SaveEvent(self.total, self.saved))
	
class SaveSelectedThread(QThread):
    def __init__(self, parent, fileName):
	QThread.__init__(self)
	self.parent = parent
	self.fileName = fileName
	self.total = 0
	self.saved = 0
	
    def run(self):
	outputFormats = QImageIO.outputFormats()
	if (self.fileName != ""):
		tmp = self.fileName.rsplit('.',1)
		for item in self.parent.items:
			if item.isSelected():
				self.total+=1
				#tmp = fileName.rsplit('.',1)
				format = None
				if len(tmp) == 1:
					fileName = tmp[0]
				if len(tmp) == 2:
					fileName, extension = tmp[0],tmp[1]
					if extension.lower() == "jpg":
						format = "JPEG"
					if extension.upper() in outputFormats:
						format = extension.upper()
						if self.saved == 0:
							fileName += "." + extension
						else:
							fileName += self.saved.__str__() + "." + extension
				if format == None:
					format = "PNG"
					if self.saved == 0:
						fileName += "." + format.lower()
					else:
						fileName += self.saved.__str__() + "." + format.lower()
				if self.parent.pixmapLabel.pixmap().save(fileName,str(format)):
					self.saved+=1
	
	qApp.postEvent(self.parent, SaveEvent(self.total, self.saved))