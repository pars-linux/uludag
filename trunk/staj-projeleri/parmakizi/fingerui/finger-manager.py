#!/usr/bin/python
# -*- coding: utf-8 -*-
"""finger-manager gui."""
from PyQt4.QtCore import pyqtSignature, SIGNAL, QEventLoop
from PyQt4.QtGui import QDialog, QApplication, QMessageBox, qApp
from PyQt4.QtGui import QPixmap
import pyfprint                 #Utility libs
import fingerform, swipe        #UI classes
import handler                  #DBus Handler from user-manager
import thread
from dbus.mainloop.qt import DBusQtMainLoop
from base64 import b64encode as b64, b64decode as b64dec

#TODO: better solution to connectSlotByName problem for on_dialog_finished()
#FIXME: swipe popup not painting in time. when fixed, add to verify too.

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

        self._initFprint()

        self.startUi()
        self.connect(self, SIGNAL("finished(int)"), self._exitFprint)
    #--------ui functions-------

    @pyqtSignature("")
    def on_pushEnroll_clicked(self):
        """Enroll button slot."""
        popup = swipe.swipeDialog()
        popup.show()
        qApp.processEvents(QEventLoop.AllEvents)
        #thread.start_new_thread(self.enroll())
        self.enroll()
        popup.reject()
        self.updateUi()

    @pyqtSignature("")
    def on_pushErase_clicked(self):
        """Erase button slot."""
        self.erase()
        self.updateUi()

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
        if self._getPrintStatus():
            img = self._loadPrint()[1]
            self.viewFinger.setPixmap(img)
        else:
            pass #place 'no image' text / img
        self.updateUi()

    def updateUi(self):
        """Updates the UI to set disabled buttons where appropriate.
        Example: When there is no existing fprint, then the user should
        not be able to press erase."""
        if not self._deviceExists():
            self.pushEnroll.setEnabled(False)
            self.pushVerify.setEnabled(False)

        if not self._getPrintStatus():
            self.pushErase.setEnabled(False)

    #------helper functions------

    def _initFprint(self):
        """Start the fprint class and discover devices."""
        pyfprint.fp_init()
        self.__devices = pyfprint.discover_devices()
        print "Dev: " + str([x.get_driver().get_full_name() for x in self.__devices])
        if self.__devices == []:
            QMessageBox.warning(self, "Okuyucu bulunamadi.", "Bilgisayarinizda\
 bir parmakizi okuyucu bulunamadigindan parmakizi tanitma ve deneme islemleri \
gerceklestirilemeyecek.")
        else:
            self.__device = self.__devices[0]

    def _exitFprint(self):
        """Exit the fprint class."""
        self._closeDevice()
        pyfprint.fp_exit()

    def _deviceExists(self):
        """Check if there are any discovered devices."""
        return self.__device != None

    def _deviceIsOpen(self):
        """Check if devices are open."""
        return self.__device.dev != None

    def _openDevice(self):
        """Open the current device, if not already open."""
        if self._deviceExists() and (not self._deviceIsOpen()):
            self.__device.open()

    def _closeDevice(self):
        """Close the current device, if not already closed."""
        if self._deviceExists() and self._deviceIsOpen():
            self.__device.close()

    def _savePrint(self, fprint, img):
        """Save serialized print data."""
        ser_fp = b64(fprint.get_data())
        ser_img = b64(self.toPGM(img))
        return self._comarCall('saveFPData', 'modifyfingerprintdata', (self.__uid, ser_fp, ser_img))

    def _loadPrint(self):
        """Load serialized print data.
        Returns a tuple containing the unserialized data and image."""
        (data, img) = self._comarCall('loadFPData', 'modifyfingerprintdata', (self.__uid))
        return (pyfprint.Fprint(b64dec(data)), self.toPixmap(b64dec(img)))

    def _erasePrint(self):
        """Erase print data."""
        self._comarCall('eraseFPData', 'modifyfingerprintdata', (self.__uid))
        self.viewFinger.clear()
        self.viewFinger.setText("Resim\n Yok")

    def _getPrintStatus(self):
        """Check if print exists or not.
        To use, call this function and then check the value of self.__status."""
        return self._comarCall('getFPStatus', 'getfingerprintdata', (self.__uid))

    def _comarCall(self, method, action, params, doneAction=None):
        """Call a COMAR method. Action must be the part after
        tr.org.pardus.comar.user.manager Params must be given in a tuple.
        E: _comarCall('getFPStatus', 'getfingerprintdata', (1000), donefunc)"""
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
        """Return comar errors in a fancy way."""
        QMessageBox.warning(self, "Finger-Manager Error", str(exception))

    @staticmethod
    def toPGM(img):
        """Convert raw fprint data to PGM format."""
        return "P5 %s %s 255\n%s" % (img.get_width(), img.get_height(), img.get_data())

    @staticmethod
    def toPixmap(pgm):
        """Convert PGM data to pixmap"""
        pixmap = QPixmap()
        pixmap.loadFromData(pgm, "PGM")
        return pixmap

    #------- main functions --------

    #QImage.Format_RGB32 works.
    def getImage(self):
        """Get the fingerprint image and then display it. Blocking."""
        if not self._deviceExists():
            print "No device found / functionality is disabled."
            return False
        self._openDevice()
        img = self.__device.capture_image(True)
        img = img.binarize()
        pixmap = self.toPixmap(self.toPGM(img))
        self.viewFinger.setPixmap(pixmap)
        self._closeDevice()


    def enroll(self):
        """Get fingerprint data, store it, and show image. Blocking."""
        if not self._deviceExists():
            print "No device found / functionality is disabled."
            return False
        self._openDevice()
        while 1:
            (fprnt, img) = self.__device.enroll_finger()
            if fprnt == "xxx": #TODO: Fix binding return. Also, memory leak?
                print "Please retry" 
            else:
                print "Enrolled"
                break
        pixmap = self.toPixmap(self.toPGM(img))
        self.viewFinger.setPixmap(pixmap)
        self._savePrint(fprnt, img)
        self._closeDevice()

    def erase(self):
        """Erase stored fingerprint data."""
        self._erasePrint()

    def verify(self):
        """Get fingerprint data and verify against previously stored data."""
        if not self._deviceExists():
            print "No device found / functionality is disabled."
            return False
        comparedata = self._loadPrint()[0]
        self._openDevice()
        while 1:
            (ret , img) = self.__device.verify_finger(comparedata)
            if ret == True:
                QMessageBox.information(self, "Parmakizi eslesti!",
                "Denediginiz parmakizi kayitli olanla eslesti.")
                break
            elif ret == False:
                QMessageBox.warning(self, "Parmakizi eslesmedi!",
                "Denediginiz parmakizi kayitli olanla eslesmedi!")
                break
            else:
                QMessageBox.warning(self, "Tekrar deneyin",
                "Parmakizi tam olarak okunamadi. Lutfen parmaginizi\
ortalayarak ve normal hizda gecirerek tekrar deneyin.")
        pixmap = self.toPixmap(self.toPGM(img))
        self.viewFinger.setPixmap(pixmap)
        self._closeDevice()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    DBusQtMainLoop(set_as_default=True)
    form = fmDialog(1000)
    form.show()
    app.exec_()
