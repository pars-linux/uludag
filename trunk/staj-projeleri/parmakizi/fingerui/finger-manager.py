#!/usr/bin/python
# -*- coding: utf-8 -*-
"""finger-manager gui."""
from PyQt4.QtCore import pyqtSignature, SIGNAL, QEventLoop
from PyQt4.QtGui import QDialog, QPixmap, QApplication, QMessageBox, qApp
import pyfprint, time          #Utility libs
import fingerform, swipe        #UI classes
import handler                  #DBus Handler from user-manager
from dbus.mainloop.qt import DBusQtMainLoop
from base64 import b64encode as b64, b64decode as b64dec

#TODO: better solution to connectSlotByName problem for on_dialog_finished()
#FIXME: swipe popup not painting in time. when fixed, add to verify too.
#FIXME: write dir must be only readable by root

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

        self.__devices = None
        self.__device = None

        super(fmDialog, self).__init__(parent)
        self.setupUi(self) #QT init

        self.startUi()
        self._initFprint()
        self.connect(self, SIGNAL("finished(int)"), self._exitFprint)

    #--------ui functions-------

    @pyqtSignature("")
    def on_pushEnroll_clicked(self):
        """Enroll button slot."""
        popup = swipe.swipeDialog()
        popup.show()
        qApp.processEvents(QEventLoop.AllEvents)
        self.enroll()
        popup.reject()

    @pyqtSignature("")
    def on_pushErase_clicked(self):
        """Erase button slot."""
        self.erase()

    @pyqtSignature("")
    def on_pushVerify_clicked(self):
        """Verify button slot."""
        self.verify()

    @pyqtSignature("")
    def on_pushClose_clicked(self):
        """Close button slot."""
        self._exitFprint()
        self.reject()

    def startUi(self):
        """Sets the UI to its initial situation.
        If user has an image, set it. Else, display 'no image'."""
        #print self._getPrintStatus()
        if self._getPrintStatus():
            (data, img) = self._loadPrint()
            self.viewFinger.setPixmap(img)
        else:
            print "noimg"
            #place 'no image' text / img

    def updateUi(self):
        """Updates the UI to set disabled buttons where appropriate.
        Example: When there is no existing fprint, then the user should
        not be able to press erase."""
        pass

    #------helper functions------

    def _initFprint(self):
        """Start the fprint class and discover devices."""
        pyfprint.fp_init()
        self.__devices = pyfprint.discover_devices()
        print [x.get_driver().get_full_name() for x in self.__devices]
        if self.__devices == []:
            sys.exit("No devices found")
        self.__device = self.__devices[0]

    def _exitFprint(self):
        """Exit the fprint class."""
        self._closeDevice()
        pyfprint.fp_exit()

    def _openDevice(self):
        """Open the current device, if not already open."""
        if not self.__device.dev:
            self.__device.open()

    def _closeDevice(self):
        """Close the current device, if not already closed."""
        if self.__device.dev:
            self.__device.close()

    def _savePrint(self, fprint, img):
        """Save serialized print data."""
        return self._comarCall('saveFPData', 'modifyfingerprintdata', (self.__uid, b64(fprint.get_data()), b64(img.get_data())))

    def _loadPrint(self):
        """Load serialized print data.
        Returns a tuple containing the unserialized data and image."""
        (data, img) = self._comarCall('loadFPData', 'modifyfingerprintdata', (self.__uid))
        return (pyfprint.Fprint(b64dec(data)), QPixmap(b64dec(img)))

    def _erasePrint(self):
        """Erase print data."""
        self._comarCall('eraseFPdata', 'modifyfingerprintdata', (self.__uid))

    def _getPrintStatus(self):
        """Check if print exists or not.
        To use, call this function and then check the value of self.__status."""
        return self._comarCall('getFPStatus', 'getfingerprintdata', (self.__uid))

    def _comarCall(self, method, action, params, doneAction=None):
        """Call a COMAR method. Action must be the part after
        tr.org.pardus.comar.user.manager Params must be given in a tuple.
        Eg: _comarCall('getFPStatus', 'getfingerprintdata', (1000), donefunc)"""
        ch = handler.CallHandler("baselayout", "User.Manager", method, "tr.org.pardus.comar.user.manager." + action, self.winId(), False)
        if doneAction:
            ch.registerDone(doneAction)
        ch.registerError(self._comarErr)
        ch.registerAuthError(self._comarErr)
        ch.registerDBusError(self._comarErr)
        if type(params) == tuple:
            return ch.call(*params)
        else:
            return ch.call(params)

    def _comarErr(self, exception):
        QMessageBox.warning(self, "Finger-Manager Error", str(exception))

    @staticmethod
    def _comarPrint(param):
        print param

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
        pixmap = self._pixmapize(img)
        self.viewFinger.setPixmap(pixmap)
        self._savePrint(fprnt, img)
        self._closeDevice()

    def erase(self):
        """Erase stored fingerprint data."""
        self._erasePrint()

    def verify(self):
        """Get fingerprint data and verify against previously stored data."""
        compareprint = self._loadPrint()
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
    DBusQtMainLoop(set_as_default=True)
    form = fmDialog(1000)
    form.show()
    app.exec_()
