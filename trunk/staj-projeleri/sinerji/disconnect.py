#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_disconnect
import sys 

class Disconnect(QDialog, ui_disconnect.Ui_Disconnect):
    def __init__(self,  parent=None):
        super(Disconnect, self).__init__(parent)
        self.setupUi(self)
        self.disconnectButton.setFocusPolicy(Qt.NoFocus)
        self.okButton.setFocusPolicy(Qt.NoFocus)
    

    
    def setText(self, client):
        self.clientTextLabel.setText("%s is connected to you" % client)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Disconnect()
    form.show()
    sys.exit(app.exec_())


