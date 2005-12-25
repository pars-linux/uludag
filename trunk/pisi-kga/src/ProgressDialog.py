from qt import *
from kdecore import *
import Progress

class ProgressDialog(Progress.Progress):
    def __init__(self, parent=None):
        Progress.Progress.__init__(self)
        animatedPisi = QMovie(locate("data","pisi_kga/pisianime.gif"))
        self.animeLabel.setMovie(animatedPisi)

    def setLabelText(self,text):
        text = KStringHandler.rPixelSqueeze(text, self.fontMetrics(), self.currentOperationLabel.width()-10)
        self.currentOperationLabel.setText(text)

