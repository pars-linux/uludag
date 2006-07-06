from qt import *
from khtml import *
from kdecore import i18n

class UpdateDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self,parent)
        self.setCaption(i18n("Currently Available Updates"))
        self.parent = parent
        
        layout1 = QGridLayout(self,2,1)
        layout2 = QHBox(self)
        layout3 = QVBox(self)

        self.updateButton = QPushButton(i18n("Upgrade selected packages"),layout3)
        self.updateButton.setEnabled(False)
        
        layout1.addWidget(layout2,1,1)
        layout1.addWidget(layout3,2,1)

        self.htmlPart = KHTMLPart(layout2)
        self.resize(self.width()-50,self.height()-50)

    def updateButtons(self):
        if len(self.parent.updatesToProcess):
            self.updateButton.setEnabled(True)
        else:
            self.updateButton.setEnabled(False)
