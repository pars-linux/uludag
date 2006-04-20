# -*- coding: utf-8 -*-

from qt import *
from kdecore import i18n
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
            self.showButton.setText(i18n("Show more information >>"))
            self.infoBrowser.hide()
        else:
            self.showButton.setText(i18n("Show less information <<"))
            self.infoBrowser.show()
        self.adjustSize()
