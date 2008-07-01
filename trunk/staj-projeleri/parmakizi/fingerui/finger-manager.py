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
        self.getImage()
        self.closeDevice()
        self.exitFprint()

    #--------ui functions-------

    @pyqtSignature("")
    def on_pushEnroll_clicked(self):
        print "Enrolled for uid " + self.__uid.__str__()

    @pyqtSignature("")
    def on_pushErase_clicked(self):
        print "FP for uid " + self.__uid.__str__() + " erased"

    @pyqtSignature("")
    def on_pushVerify_clicked(self):
        print "FP matches!"

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

    def closeDevice(self):
        self.__device.close()

    def getImage(self):
        self.__device.open()
        img = self.__device.capture_image(True)
        img.standardize()
        img = img.binarize()
        #img.save_to_file("parmak.ppm")
        pixmap = QPixmap()
        print pixmap.loadFromData(img.get_data())


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = fmDialog(1)
    form.show()
    app.exec_()
