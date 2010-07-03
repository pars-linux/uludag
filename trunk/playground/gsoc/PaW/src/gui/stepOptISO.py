import sys
import os
from utils import humanReadableSize
from gui.stepTemplate import StepWidget
from PyQt4 import QtGui, QtCore

from gui.widgetOptISO import Ui_widgetOptISO

class Widget(QtGui.QWidget, StepWidget):
    heading = "Choose ISO File"

    version = None # populated upon first specified file

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetOptISO()
	self.gui.setupUi(self)

	self.filePath = ''
	QtCore.QObject.connect(self.gui.btnBrowse, QtCore.SIGNAL('clicked()'), self.openFileDialog)
        QtCore.QObject.connect(self.gui.btnValidate, QtCore.SIGNAL('clicked()'), self.validateFile)

    def openFileDialog(self):
	fileDialog =QtGui.QFileDialog()
	fileDialog.setNameFilter('*.iso') # Does not work!
	self.filePath = str(fileDialog.getOpenFileName(self, 'Open ISO File'))
	self.onFileUpdated()

    def onFileUpdated(self):
	self.gui.txtFileName.setText(self.filePath)
        useFileSize = True # Hard-coded switch. True for 'validate by size'.

        if useFileSize:
            # Extract version of ISO file by size
            # Assume that all ISO images have different size in bytes.
            size = os.path.getsize(os.path.normpath(self.filePath))
            self.version = self.mainEngine.versionManager.getBySize(size)
        else:
            # Extract version of ISO file by its MD5 sum.
            # TODO: MD5 sum can be slower on some PCs and it freezes GUI.
            self.version = self.mainEngine.versionManager.getByMD5Sum(self.md5sumFile())

        if self.version:
            self.gui.lblVersion.setText('Valid %s image!' % self.version.name)
        else:
            self.gui.lblVersion.setText('Unknown Pardus Live CD image.')

    def onSubmit(self):
	if not self.filePath:
	    QtGui.QMessageBox.warning(self, 'Warning', 'Please choose an ISO file (*.iso) to proceed.', QtGui.QMessageBox.Ok)
	    return False
	else:
            if not self.version:
                reply = QtGui.QMessageBox.warning(self, 'Unknown CD Image',
                            'Could not determine version of ISO file. It is not recommended to continue installation.\nDo you want to quit?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

                if reply == QtGui.QMessageBox.Yes:
                    sys.exit() # TODO: do not exit immediately. rollback changes.

            self.mainEngine.version = self.version
	    return True

    def md5sumFile(self):
        if not self.filePath:
            return None
        elif not os.path.isfile(os.path.normpath(self.filePath)):
            return None
        else:
            hash = self.mainEngine.md5sum.encryptFile(self.filePath)
            return hash

    def validateFile(self):
        computed, original = None, None
        if self.version: original = self.version.md5sum
        if self.filePath and self.version: computed = self.md5sumFile()

        if not self.filePath:
            title = 'No Image Specified'
	    msg = 'Choose an *.iso CD/DVD image file from your PC to validate.'
	    method = QtGui.QMessageBox.warning
        elif not self.version:
            title = 'Could not verify'
	    msg = 'Could not verify image since the file you have chosen is not recognized as a valid Pardus CD/DVD image.'
	    method = QtGui.QMessageBox.warning
	elif computed == original:
	    title = 'Validated'
	    msg = 'Downloaded file is valid. You can proceed installation safely.'
	    method = QtGui.QMessageBox.information
	else:
	    title = 'Invalid File!'
	    msg = 'Downloaded file is INVALID or CORRUPT. It is STRONGLY recommended NOT to continue installation.'
	    method = QtGui.QMessageBox.error

	method(self, title, msg, QtGui.QMessageBox.Ok)

    def nextIndex(self):
	return 0