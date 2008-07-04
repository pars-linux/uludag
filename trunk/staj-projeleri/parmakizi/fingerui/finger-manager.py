#!/usr/bin/python
# -*- coding: utf-8 -*-
"""finger-manager gui."""
from PyQt4.QtCore import pyqtSignature
from PyQt4.QtGui import QDialog, QPixmap, QApplication
import fingerform
import libfprint

class fmDialog(QDialog, fingerform.Ui_dialogFinger):
    """Dialog for finger-manager.
    Supports 3 basic functions: Enroll, Verify and Erase.
    Enroll asks the user for fingerprint data and saves it.
    Verify verifies the fingerprint data with the currently saved data.
    Erase erases the currently saved data."""
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
        self.setupUi(self) #QT init
        
        self.startUi()
        self._initFprint()

    #--------ui functions-------

    @pyqtSignature("")
    def on_pushEnroll_clicked(self):
        """Enroll button event handler."""
        self.enroll()

    @pyqtSignature("")
    def on_pushErase_clicked(self):
        """Erase button event handler."""
        print "FP for uid " + self.__uid.__str__()

    @pyqtSignature("")
    def on_pushVerify_clicked(self):
        """Verify button event handler."""
        self.verify()

    @pyqtSignature("")
    def on_pushClose_clicked(self):
        self._exitFprint()
        self.reject()

    @pyqtSignature("int")
    def on_dialogFinger_finished(self, result):
        """Handle the cases where the user presses ESC."""
        print "fooasdas"
        self._exitFprint()

    def closeEvent(self, event):
        """Handle the close event to exit library on time."""
        print "died"
        event.accept()
        self._exitFprint()
        #super(fmDialog, self).closeEvent(event)

    def startUi(self):
        """Sets the UI to its initial situation.
        If user has an image, set it. Else, display 'no image'."""
        #does img for UID exist?
        #if so, pull it in
        #else, place 'no image' text / img
        pass

    def updateUi(self):
        """Updates the UI to set disabled buttons where appropriate.
        Example: When there is no existing fprint, then the user should
        not be able to press erase."""
        pass

    #------helper functions------

    def _initFprint(self):
        """Start the fprint class and discover devices."""
        libfprint.fp_init()
        self.__devices = libfprint.discover_devices()
        print [x.get_driver().get_full_name() for x in self.__devices]
        if self.__devices == []:
            sys.exit("No devices found")
        self.__device = self.__devices[0]

    def _exitFprint(self):
        """Exit the fprint class."""
        self._closeDevice()
        libfprint.fp_exit()

    def _openDevice(self):
        """Open the current device, if not already open."""
        if not self.__device.dev:
            self.__device.open()

    def _closeDevice(self):
        """Close the current device, if not already closed."""
        if self.__device.dev:
            self.__device.close()

    @staticmethod
    def _savePrint(fprint, path=".printdata"): #TODO: Comarize.
        """Save serialized print data."""
        printfile = open(path, "w")
        printfile.write(fprint.get_data())
        printfile.close()

    @staticmethod
    def _loadPrint(path=".printdata"): #TODO: Comarize.
        """Load serialized print data."""
        printfile = open(path, "r")
        printdata = printfile.read()
        printfile.close()
        return libfprint.Fprint(printdata)

    @staticmethod
    def _pixmapize(img, filename=".tmpimg"):
        """Convert image into pixmap."""
        img.save_to_file(filename) #TODO: comarize OR Fix workaround.
        return QPixmap(filename)

    #------- main functions --------

    #QImage.Format_RGB32 works.
    def getImage(self):
        """Get the fingerprint image and then display it. Blocking."""
        self._openDevice()
        img = self.__device.capture_image(True)
        img = img.binarize()
        pixmap = self._pixmapize(img, "parmak.pgm")
        self.viewFinger.setPixmap(pixmap)
        self._closeDevice()


    def enroll(self):
        """Get fingerprint data, store it, and show image. Blocking."""
        self._openDevice()
        while 1:
            (fprnt, img) = self.__device.enroll_finger()
            if fprnt == "xxx": #TODO: Fix binding return. Also, memory leak?
                print "Please retry" 
            else:
                print "Enrolled"
                break
        pixmap = self._pixmapize(img.binarize())
        self.viewFinger.setPixmap(pixmap)
        self._savePrint(fprnt) #TODO: save with uid
        self._closeDevice()


    def verify(self):
        """Get fingerprint data and verify against previously stored data."""
        compareprint = self._loadPrint() #TODO: comarize w/ uid, check existance
        self._openDevice()
        while 1:
            (ret , img) = self.__device.verify_finger(compareprint)
            if ret == True:
                print "FP matched"
                break
            elif ret == False:
                print "Match failed"
                break
            else:
                print "please retry"
        pixmap = self._pixmapize(img.binarize())
        self.viewFinger.setPixmap(pixmap)
        self._closeDevice()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = fmDialog(1)
    form.show()
    app.exec_()
