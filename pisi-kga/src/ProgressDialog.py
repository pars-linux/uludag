from qt import *
from kdecore import *
import Progress

class ProgressDialog(Progress.Progress):
    def __init__(self, parent=None):
        Progress.Progress.__init__(self)
        animatedPisi = QMovie(locate("data","pisi_kga/pisianime.gif"))
        self.animeLabel.setMovie(animatedPisi)
        self.forcedClose = False

    def setLabelText(self,text):
        text = KStringHandler.rPixelSqueeze(text, self.fontMetrics(), self.currentOperationLabel.width()-10)
        self.currentOperationLabel.setText(text)

    def closeForced(self):
        self.forcedClose = True
        self.close()
        
    def close(self, alsoDelete=False):
        if self.forcedClose:
            Progress.Progress.close(self,alsoDelete)
            self.forcedClose = False
            return True
        
        self.forcedClose = False
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return
        else:
            Progress.Progress.keyPressEvent(self,event)
        
