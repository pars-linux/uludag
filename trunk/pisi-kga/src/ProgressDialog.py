from Progress import *

class ProgressDialog(Progress):
    def __init__(self, Parent=None):
        Progress.__init__(self,Parent)
        self.forceClose = False
        self.setModal(True)
        self.progressBar.setTotalSteps(100)

    def forcedClose(self):
        self.forceClose = True
        self.close()
        self.forceClose = False

    def closeEvent(self, event):
        if self.forceClose:
            event.accept()
        else:
            event.ignore()
