from qt import *
import Progress

class ProgressDialog(Progress.Progress):
    def __init__(self, parent=None):
        Progress.Progress.__init__(self, parent, "dialog", True, Qt.WStyle_Customize|Qt.WStyle_Title)
