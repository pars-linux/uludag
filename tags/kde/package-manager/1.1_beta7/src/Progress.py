from qt import *
from kdecore import *
from ProgressDialog import *

import pisi

class Progress(ProgressDialog):
    def __init__(self, parent=None):
        ProgressDialog.__init__(self)
        self.parent = parent
        animatedPisi = QMovie(locate("data","package-manager/pisianime.gif"))
        self.animeLabel.setMovie(animatedPisi)
        self.forcedClose = False
        self.connect(self.cancelButton,SIGNAL("clicked()"),self.cancelThread)
        self.cancelButton.setEnabled(False)
        self.hideStatus()
        self.hideOperationDescription()
        
        self.packageNo = 1
        self.totalPackages = 1
        self.packageName = ""

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

    def setCurrentOperation(self, text):
        self.currentOperationLabel.setText(text)

    def setOperationDescription(self, text):
        self.operationDescription.setText(text)

    def setStatus(self, text):
        self.statusInfo.setText(text)

    def showStatus(self):
        self.statusInfo.show()

    def showOperationDescription(self):
        self.operationDescription.show()

    def hideStatus(self):
        self.setStatus("")

    def hideOperationDescription(self):
        self.setOperationDescription("")

    def updateProgressBar(self, progress):
        self.progressBar.setProgress(float(progress))
    
    def reset(self):
        self.setCurrentOperation(i18n("<b>Preparing PiSi...</b>"))
        self.hideStatus()
        self.hideOperationDescription()
        self.packageNo = 1
        self.totalPackages = 1
        self.progressBar.setProgress(0)
        self.cancelButton.setEnabled(False)

    def cancelThread(self):
        self.setCurrentOperation(i18n("<b>Cancelling operation...</b>"))
        self.cancelButton.setEnabled(False)
        self.parent.command.cancel()

    def closeForced(self):
        self.forcedClose = True
        self.close()

    def close(self, alsoDelete=False):
        if self.forcedClose:
            ProgressDialog.close(self,alsoDelete)
            self.forcedClose = False
            return True

        self.forcedClose = False
        return False

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return
        else:
            ProgressDialog.keyPressEvent(self,event)

    def updateOperationDescription(self, operation, package=None):
        if not package:
            package = self.packageName
        
        self.setOperationDescription(i18n('Now %1 <b>%2</b> package').arg(operation).arg(package))

    def updateDownloadingInfo(self, operation, file, percent, rate, symbol):
        self.packageName = pisi.util.parse_package_name(file)[0]
        self.setOperationDescription(i18n('Now %1 <b>%2</b> package').arg(operation).arg(self.packageName))
        self.updateProgressBar(percent)
        self.setStatus(i18n('Fetching package (%1/%2) at %3 %4')
                       .arg(self.packageNo)
                       .arg(self.totalPackages)
                       .arg(round(int(rate), 1))
                       .arg(symbol))
        self.showStatus()
        self.showOperationDescription()

    def updateUpgradingInfo(self, percent, rate, symbol):
        self.updateProgressBar(percent)
        self.setStatus(i18n('Fetching package list at %3 %4')
                       .arg(round(int(rate), 1))
                       .arg(symbol))
        self.showStatus()
        self.showOperationDescription()
