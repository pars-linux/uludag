import os
import sys

from PyQt4 import QtGui, QtCore
from ui.controller.stepTemplate import StepWidget
from ui.gui.cd import Ui_cd
from utils import locate_file_in_path
from utils import version_name_from_gfxboot

import logger
log = logger.getLogger('CD Option Step')

class Widget(QtGui.QWidget, StepWidget):
    heading = "Install from Pardus Live CD/DVD"
    cd = None
    gfxboot_cfg_file = "gfxboot.cfg"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_cd()
	self.gui.setupUi(self)
        self.connect(self.gui.comboDrive, QtCore.SIGNAL('currentIndexChanged(int)'), self.onDriveUpdated)

    def onEnter(self):
        self.populateCDs()

    def onDriveUpdated(self):
        pass
        version = self.determineCDVersion()
        if version:
            cdDrive = self.getSelectedCDDrive()
            self.gui.lblPath.setText("%s CD detected in %s successfully." % (version.name, cdDrive.DeviceID))
        else:
            self.gui.lblPath.setText("Unrecognized Pardus CD in drive.")

    def populateCDs(self):
	self.gui.comboDrive.clear()
        self.mainEngine.compatibility.winPopulateCDs()
        cdDrives = self.mainEngine.compatibility.cds
        if not cdDrives or len(cdDrives) == 0:
            self.gui.lblPath.setText("No CD/DVD-ROM detected on your computer.")
            self.gui.comboDrive.setDisabled(True)
        else:
            self.gui.comboDrive.setDisabled(False)
	for cd in cdDrives:
	    self.gui.comboDrive.addItem('%s %s' %(cd.DeviceID, cd.Name))

    def getSelectedCDDrive(self):
	for cd in self.mainEngine.compatibility.cds:
	    if cd.DeviceID == self.gui.comboDrive.currentText()[:2]:
                # TODO: TBD: First 2 letters of combobox is drive letter+colon.
                # This may fail in the future.
		return cd
	return None

    def isEmptyDrive(self, CD):
        """
        Returns False if CD root is accessible.
        True if any IO, Permission errors occur. That means CD is not readable.
        """
        try:
            return not isinstance(os.listdir(CD.DeviceID),list) # check i.e. f:\
        except WindowsError, IOError:
            return True

    def determineCDVersion(self, tolerance = 10):
        """
        Determines Pardus release version by parsing gfxboot.cfg and
        obtaining distro name then comparing it with names defined in
        versions.xml file using Levenshtein distance of 'tolerance' value.
        """
        # TODO: tolerance TBD.
        currentDrive = self.getSelectedCDDrive()
        if not currentDrive: return None
        
        gfxboot_cfg = locate_file_in_path('%s\\' % currentDrive.DeviceID, self.gfxboot_cfg_file)
        if not gfxboot_cfg:
            log.debug('Could not locate %s.' % self.gfxboot_cfg_file)
            return None

        distro_name = version_name_from_gfxboot(gfxboot_cfg)

        if not distro_name:
            log.debug('No distro specified in %.' % self.gfxboot_cfg_file)
            return None

        result = self.mainEngine.versionManager.getByDistance(distro_name, tolerance)
                
        if result:
            log.debug('Detected version: %s' % result.name)
            return result
        else:
            log.debug('Could not detect version in Levenshtein distance of %d.' % tolerance)
        return None

    def onSubmit(self):
	currentDrive = self.getSelectedCDDrive()

        if not currentDrive:
	    QtGui.QMessageBox.warning(self, 'Warning', 'Please choose Pardus CD drive or folder to proceed.', QtGui.QMessageBox.Ok)
	    return False
        elif self.isEmptyDrive(currentDrive):
            QtGui.QMessageBox.warning(self, 'Could not read CD/DVD', 'You do not have a CD/DVD in %s or drive is not ready. If you have a working CD/DVD in it, please try again.' % currentDrive.DeviceID, QtGui.QMessageBox.Ok)
            return False
	else:
            self.mainEngine.config.cdDrive = self.getSelectedCDDrive()
            version = self.determineCDVersion()

            if version:
                self.mainEngine.version = version
            else:
                reply = QtGui.QMessageBox.warning(self, 'Unknown Pardus CD/DVD', 'Unable to identify Pardus release of CD/DVD in %s. It is NOT recommended to continue installation. Do you want to exit?' % currentDrive.DeviceID, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes: sys.exit() # TODO: redirect to a exit event function
                
	    return True

    def nextIndex(self):
	return 8
