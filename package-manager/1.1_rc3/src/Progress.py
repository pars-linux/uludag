from qt import *
from kdecore import *
from ProgressDialog import *

import Basket
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
        self.hideOperationDescription()
        
        self.packageNo = 0
        self.totalPackages = 0
        self.packageName = ""

        self.totalSize = 0
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0

    def enableCancel(self):
        self.cancelButton.setEnabled(True)

    def setCurrentOperation(self, text):
        self.currentOperationLabel.setText(text)

    def setOperationDescription(self, text):
        self.operationDescription.setText(text)

    def updateStatus(self):
        completed, total = self.getCurrentDownloadedSize()
        self.completedInfo.setText(completed)
        self.totalInfo.setText(i18n("downloaded ( total: %1 )").arg(total))
        self.updatePackageInfo()

    def showStatus(self):
        self.packageInfo.show()
        self.completedInfo.show()
        self.totalInfo.show()

    def showOperationDescription(self):
        self.operationDescription.show()

    def hideStatus(self, hidepackage=False):
        if hidepackage:
            self.packageInfo.hide()

        self.completedInfo.hide()
        self.totalInfo.hide()

    def hideOperationDescription(self):
        self.setOperationDescription("")

    def updateProgressBar(self, progress):
        self.progressBar.setProgress(float(progress))
    
    def reset(self):
        self.setCurrentOperation(i18n("<b>Preparing PiSi...</b>"))

        self.completedInfo.setText(i18n("--"))
        self.totalInfo.setText(i18n("downloaded (total: -- )"))
        self.packageInfo.setText(i18n("-- / --  package"))

        self.hideOperationDescription()
        self.hideStatus()

        # package statistics
        self.packageNo = 0
        self.totalPackages = 0

        # size informations
        self.totalDownloaded = 0
        self.curPkgDownloaded = 0
        self.totalSize = 0

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

    def updateDownloadingInfo(self, operation, file):
        self.packageName = pisi.util.parse_package_name(file)[0]
        self.setOperationDescription(i18n('Now %1 <b>%2</b> package').arg(operation).arg(self.packageName))
        self.updateStatus()
        self.showOperationDescription()

    def updateUpgradingInfo(self):
        self.updateStatus()
        self.showOperationDescription()

    def updatePackageInfo(self):
        if self.parent.state == Basket.install_state:
            operation = i18n("installed")
        elif self.parent.state == Basket.remove_state:
            operation = i18n("removed")
        elif self.parent.state == Basket.upgrade_state:
            operation = i18n("upgraded")

        self.packageInfo.setText(i18n("%1 / %2 package %3").arg(self.packageNo).arg(self.totalPackages).arg(operation))

    # pisi does not provide total downloaded size, just package based.
    def updateTotalDownloaded(self, pkgDownSize, pkgTotalSize):
        if pkgDownSize == pkgTotalSize:
            self.totalDownloaded += int(pkgTotalSize)
            self.curPkgDownloaded = 0
        else:
            self.curPkgDownloaded = int(pkgDownSize)

    # pisi does not provide total operation percent, just package based.
    def updateTotalOperationPercent(self):
        totalDownloaded = self.totalDownloaded + self.curPkgDownloaded
        try:
            percent = (totalDownloaded * 100) / self.totalSize
        except ZeroDivisionError:
            percent = 100

        self.updateProgressBar(percent)

    def getCurrentDownloadedSize(self):
        totalDownloaded = self.totalDownloaded + self.curPkgDownloaded

        size = pisi.util.human_readable_size(totalDownloaded)
        totaldownloaded = "%.2f %s" % (size[0], size[1])

        size = pisi.util.human_readable_size(self.totalSize)
        totalsize = "%.2f %s" % (size[0], size[1])

        return (totaldownloaded, totalsize)

    def updatePackageProgress(self):
        try:
            percent = (self.packageNo * 100) / self.totalPackages
        except ZeroDivisionError:
            percent = 0

        self.updateProgressBar(percent)
