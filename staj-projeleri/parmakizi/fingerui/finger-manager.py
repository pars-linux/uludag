from PyQt4.QtCore import *
from PyQt4.QtGui import *
import fingerform

class fmDialog(QDialog, fingerform.Ui_dialogFinger):
    def __init__(self, parent=None):
        super(fmDialog, self).__init__(parent)
        self.setupUi(self)
        self.UpdateUi()

    def UpdateUi(self):
        pass

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = fmDialog()
    form.show()
    app.exec_()

