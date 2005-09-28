import EthernetWidget
from qt import *

class EthernetPage(EthernetWidget.EthernetWidget):
    def __init__(self,parent=None):
        EthernetWidget.EthernetWidget.__init__(self,parent)
        
        self.connect(self.ipManualButton, SIGNAL("stateChanged(int)"), self.updateInfoFrame)
        self.connect(self.dnsManualButton, SIGNAL("stateChanged(int)"), self.updateDnsFrame)

    def updateInfoFrame(self):
        if self.ipManualButton.isChecked():
            self.ipManualFrame.setEnabled(True)
        else:
            self.ipManualFrame.setEnabled(False)

    def updateDnsFrame(self):
        if self.dnsManualButton.isChecked():
            self.dnsManualFrame.setEnabled(True)
        else:
            self.dnsManualFrame.setEnabled(False)

