

from qt import *

class ScanEvent(QCustomEvent):
    def __init__(self,image):
        QCustomEvent.__init__(self,1002);
        self.image = image
        
class PreviewEvent(QCustomEvent):
    def __init__(self, image):
	QCustomEvent.__init__(self,1003)
	self.image = image
		
class StopEvent(QCustomEvent):
    def __init__(self):
	QCustomEvent.__init__(self,1004)
	
class SaveEvent(QCustomEvent):
    def __init__(self, total, saved):
	QCustomEvent.__init__(self,1005)
	self.total = total
	self.saved = saved
	 