

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