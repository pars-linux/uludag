import os
import sys
import ConfigParser
from utils import levenshtein

from PyQt4 import QtGui, QtCore
from ui.controller.stepTemplate import StepWidget
from ui.gui.usb import Ui_usb

from logger import getLogger
log = getLogger('USB Option Step')

class Widget(QtGui.QWidget, StepWidget):
    heading = "Install from USB Memory Stick"
    usb = None

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_usb()
	self.gui.setupUi(self)
        self.connect(self.gui.comboDrive, QtCore.SIGNAL('currentIndexChanged(int)'), self.onDriveUpdated)

    def onEnter(self):
        self.populateUSBs()

    def onDriveUpdated(self):
        pass
#        version = self.determineUSBVersion()
#        if version:
#            usbDrive = self.getSelectedUSBDrive()
#            self.gui.lblPath.setText("%s CD detected in %s successfully." % (version.name, usbDrive.DeviceID))
#        else:
#            self.gui.lblPath.setText("Unrecognized Pardus CD in drive %s." % self.usbPath)

    def populateUSBs(self):
	self.gui.comboDrive.clear()
        self.mainEngine.compatibility.winPopulateUSBs()
        usbDrives = self.mainEngine.compatibility.usbs
        if not usbDrives or len(usbDrives)==0:
            self.gui.lblPath.setText("No plugged USB drive detected on your computer.")
            self.gui.comboDrive.setDisabled(True)
        else:
            self.gui.comboDrive.setDisabled(False)
	for usb in usbDrives:
	    self.gui.comboDrive.addItem('%s %s' %(usb.DeviceID, usb.Name))

    def getSelectedUSBDrive(self):
	for usb in self.mainEngine.compatibility.usbs:
	    if usb.DeviceID == self.gui.comboDrive.currentText()[:2]:
                # TODO: TBD: First 2 letters of combobox is drive letter+colon.
                # This may fail in the future.
		return usb
	return None

    def locate_gfxboot_cfg(self, path):
            """
            Locates first occurrence of gfxboot.cfg in the path.
                'path' should be an absolute path.
            """
            filename = 'gfxboot.cfg'
            contents = os.listdir(path)
            try: index = contents.index(filename)
            except ValueError: index = -1 # indicates does not exist

            if not index == -1 and os.path.isfile(os.path.join(path,filename)):
                return os.path.join(path, filename)
            else:
                for item in contents:
                    if os.path.isdir(os.path.join(path, item)): # nested dirs
                        result = self.locate_gfxboot_cfg(os.path.join(path,item))
                        if result: return result
            return None

    def determineUSBVersion(self, tolerance = 10):
        """
        Determines Pardus release version by parsing gfxboot.cfg and
        obtaining distro name then comparing it with names defined in
        versions.xml file using Levenshtein distance of 'tolerance' value.
        Newer version with appropriate distane will be matched.
        """
        # TODO: tolerance TBD.
        currentDrive = self.getSelectedUSBDrive()

        gfxboot_cfg = self.locate_gfxboot_cfg('%s\\' % currentDrive.DeviceID)
        if not gfxboot_cfg:
            log.debug('Could not locate gfxboot.cfg')
            return None

        config_parser = ConfigParser.ConfigParser()
        config_parser.read(gfxboot_cfg)
        distro_name = config_parser.get('base','distro')

        if not distro_name:
            log.debug('No distro specified in gfxboot.cfg')
            return None

        result = None
        for version in self.mainEngine.versionManager.versions:
            l_distance = levenshtein(version.name, distro_name)
            if l_distance < tolerance:
                result = version

        if result:
            log.debug('Detected version: %s' % result.name)
            return result
        else:
            log.debug('Could not detect version in Levenshtein distance of %d.' % tolerance)
        return None

    def onSubmit(self):
	currentDrive = self.getSelectedUSBDrive()

        if not currentDrive:
            QtGui.QMessageBox.warning(self, 'Warning', 'Please choose USB drive which has Pardus CD contents to proceed.', QtGui.QMessageBox.Ok)
            return False
	else:
            self.mainEngine.config.usbDrive = self.getSelectedUSBDrive()
            version = self.determineUSBVersion()
            if version:
                self.mainEngine.version = version
            else:
                reply = QtGui.QMessageBox.warning(self, 'Unknown Pardus Live CD contents in USB.', 'Unable to identify Pardus release of CD/DVD in %s. It is NOT recommended to continue installation. Do you want to exit?' % currentDrive.DeviceID, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes: sys.exit()

	    return True

    def nextIndex(self):
        return 8
