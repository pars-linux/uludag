# -*- coding: utf-8 -*-

from qt import *
import PisiKga
import SuccessDialog

class Success(SuccessDialog.SuccessDialog):
    def __init__(self, parent=None):
        SuccessDialog.SuccessDialog.__init__(self,parent)
        self.showHideBrowser()
        self.infoPixmap.setPixmap(PisiKga.loadIcon("info"))
        self.connect(self.showButton, SIGNAL("clicked()"), self.showHideBrowser)

    def showHideBrowser(self):
        if self.infoBrowser.isShown():
            self.showButton.setText(u"Daha fazla bilgi göster >>")
            self.infoBrowser.hide()
        else:
            self.showButton.setText(u"Daha az bilgi <<")
            self.infoBrowser.show()
        self.adjustSize()
