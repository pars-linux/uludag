from qt import *
import Progress

class ProgressDialog(Progress.Progress):
    def __init__(self, parent=None):
        Progress.Progress.__init__(self)
        animatedPisi = QMovie("./pisianime.gif")
        self.animeLabel.setMovie(animatedPisi)

        
