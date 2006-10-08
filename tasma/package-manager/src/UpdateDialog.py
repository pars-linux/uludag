from qt import *
from khtml import *
from kdecore import i18n
import pisi.api
import CustomEventListener

class UpdateDialog(QDialog):
    def __init__(self, parent=None, upgradables=None):
        QDialog.__init__(self,parent)
        self.setCaption(i18n("Currently Available Updates"))
        self.parent = parent
        self.updatesToProcess = []

        layout1 = QGridLayout(self,2,1)
        layout2 = QHBox(self)
        layout3 = QVBox(self)

        self.updateButton = QPushButton(i18n("Upgrade selected packages"),layout3)
        self.updateButton.setEnabled(False)

        layout1.addWidget(layout2,1,1)
        layout1.addWidget(layout3,2,1)

        self.htmlPart = KHTMLPart(layout2)
        self.parent.createHTML(upgradables, self.htmlPart)

        self.connect(self.htmlPart,SIGNAL("completed()"),self.registerEventListener)
        self.connect(self.updateButton,SIGNAL("clicked()"),self.parent.updatePackages)

        self.resize(self.width()-50,self.height()-50)

    def registerEventListener(self):
        self.eventListener = CustomEventListener.CustomEventListener(self, self.updatesToProcess)
        node = self.htmlPart.document().getElementsByTagName(DOM.DOMString("body")).item(0)
        node.addEventListener(DOM.DOMString("click"),self.eventListener,True)

    def updateButtons(self):
        if self.updatesToProcess:
            self.updateButton.setEnabled(True)
        else:
            self.updateButton.setEnabled(False)

    def refreshDialog(self):
        upgradables = pisi.api.list_upgradable()
        if not upgradables:
            self.updatesToProcess = []
        
        try:
            self.parent.createHTML(upgradables, self.htmlPart)
        except Exception, e:
            print e

        self.updateButtons()
