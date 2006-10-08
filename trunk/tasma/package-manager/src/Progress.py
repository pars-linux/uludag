from qt import *
from kdecore import *
from ProgressDialog import *

class Progress(ProgressDialog):
    def __init__(self, parent=None):
        ProgressDialog.__init__(self)
        animatedPisi = QMovie(locate("data","package-manager/pisianime.gif"))
        self.animeLabel.setMovie(animatedPisi)
        self.forcedClose = False

        self.currentOperation = None
        self.currentFile = None
        self.totalAppCount = 1
        self.currentAppIndex = 1

        self.connect(self.cancelButton,SIGNAL("clicked()"),self.cancelThread)

    def setLabelText(self,text):
        text = KStringHandler.rPixelSqueeze(text, self.fontMetrics(), self.currentOperationLabel.width()-10)
        self.currentOperationLabel.setText(text)

    def updateProgressText(self):
        self.setLabelText(i18n('Now %1 <b>%2</b> (%3 of %4)')
                          .arg(self.currentOperation).arg(self.currentFile).arg(self.currentAppIndex).arg(self.totalAppCount))

    def updateProgressBar(self, filename, length, rate, symbol,downloaded_size,total_size):
        self.updateProgressText()
        self.speedLabel.setText(i18n('<b>Speed:</b> %1 %2').arg(rate).arg(symbol))

        tpl = pisi.util.human_readable_size(downloaded_size)
        downloadedText,type1 = (int(tpl[0]), tpl[1])
        type1 = pisi.util.human_readable_size(downloaded_size)[1]
        tpl = pisi.util.human_readable_size(total_size)
        totalText,type2 = (int(tpl[0]), tpl[1])

        self.sizeLabel.setText(i18n('<b>Downloaded/Total:</b> %1 %2/%3 %4').arg(downloadedText).arg(type1).arg(totalText).arg(type2))
        self.progressBar.setProgress((float(downloaded_size)/float(total_size))*100)

    def cancelThread(self):
        # Reset progressbar
        self.setLabelText(i18n("<b>Cancelling operation...</b>"))
        self.speedLabel.hide()
        self.sizeLabel.hide()

#       self.command.terminate()
        self.parent.possibleError = True
        self.parent.finished()

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

    def reset(self):
        self.progressBar.setProgress(0)
        self.setLabelText(i18n("<b>Preparing PiSi...</b>"))
        self.speedLabel.setText(i18n('<b>Speed:</b> N/A'))
        self.sizeLabel.setText(i18n('<b>Downloaded/Total:</b> N/A'))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            return
        else:
            ProgressDialog.keyPressEvent(self,event)
