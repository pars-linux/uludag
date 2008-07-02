from PyQt4.QtCore import *
from PyQt4.QtGui import *
import fingerform
from libfprint import *

class fmDialog(QDialog, fingerform.Ui_dialogFinger):
    def __init__(self, uid, parent=None):
        
        #uid
        if uid == None:
            raise ValueError
        self.__uid = uid

        #devices
        self.__devices = None

        #device
        self.__device = None


        super(fmDialog, self).__init__(parent)
        self.setupUi(self)
        self.UpdateUi()
        self.initFprint()
        self.initDevice()
        self.enroll()

    def __del__(self):
        #super(self.__class__, self).__del__()
        if self.__device:
            self.closeDevice()
        self.exitFprint()
        

    #--------ui functions-------

    @pyqtSignature("")
    def on_pushEnroll_clicked(self):
        self.enroll(self.__uid.__str__())

    @pyqtSignature("")
    def on_pushErase_clicked(self):
        print "FP for uid " + self.__uid.__str__()

    @pyqtSignature("")
    def on_pushVerify_clicked(self):
        self.verify(self.__uid.__str__())

    def UpdateUi(self):
        pass

    #------helper functions------
    def initFprint(self):
        fp_init()

    def initDevice(self):
        self.__devices = pyfprint.discover_devices()
        print [x.get_driver().get_full_name() for x in self.__devices]
        if self.__devices == []:
            raise "No devices found"
        self.__device = self.__devices[0]
    
    def exitFprint(self):
        fp_exit()

    def openDevice(self):
        self.__device.open()

    def closeDevice(self):
        self.__device.close()

    #QImage.Format_RGB32 works.
    def getImage(self):
        self.openDevice()
        img = self.__device.capture_image(True)
        img = img.binarize()
        pixmap = self._pixmapize(img, "parmak.pgm")
        self.viewFinger.setPixmap(pixmap)
        self.closeDevice()

    def _pixmapize(self, img, savepath=".tmpimg"):
        img.save_to_file(filename) #(TODO: comarize)
        return QPixmap(filename)

    def enroll(self, uid):
        self.openDevice()
        while 1:
            (fprnt, img) = self.__device.enroll_finger()
            if fprnt == "xxx": #TODO: Fix binding return data. Also, memory leak?
                print "Please retry" 
            else:
                print "Enrolled"
                break
        pixmap = self._pixmapize(img.binarize())
        self.viewFinger.setPixmap(pixmap)
        self._savePrint(fprnt)
        self.closeDevice()

    def _savePrint(self, fprint, path=".printdata"):
        file = open(path, "w")
        file.write(fprint.get_data())
        file.close()

    def _loadPrint(self, fprint, path=".printdata"):
        file=open(path, "r")
        printdata = file.read()
        file.close()
        return Fprint(printdata)

    def verify(self, uid):
        self.openDevice()
        while 1:
            (ret , img) = self.__device.verify_finger()
            if ret == True:
                break
            elif ret == FALSE:
                print "Match failed"
            else:
                print "please retry"
        pixmap = self._pixmapize(img.binarize())
        self.viewFinger.setPixmap(pixmap)
        self._savePrint(fprint)
        self.closeDevice()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = fmDialog(1)
    form.show()
    app.exec_()
