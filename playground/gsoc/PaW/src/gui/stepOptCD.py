import os
import sys
import ConfigParser
from utils import levenshtein

from gui.stepTemplate import StepWidget
from PyQt4 import QtGui
from gui.widgetOptCD import Ui_widgetOptCD

class Widget(QtGui.QWidget, StepWidget):
    heading = "Show Your CD/DVD Path"
    cd = None

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_widgetOptCD()
	self.gui.setupUi(self)

	self.populateCDs()

    def openFileDialog(self):
	fileDialog =QtGui.QFileDialog()
	self.cdPath = fileDialog.getExistingDirectory(self, 'Select CD Drive or Folder')

	self.onPathUpdated()

    def onPathUpdated(self):
	self.gui.txtPath.setText(self.cdPath)

    def populateCDs(self):
	self.gui.comboDrive.clear()
	for cd in self.mainEngine.compatibility.cds:
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

    def determineCDVersion(self, tolerance = 5):
        """
        Determines Pardus release version by parsing gfxboot.cfg and
        obtaining distro name then comparing it with names defined in
        versions.xml file using Levenshtein distance of 'tolerance' value.
        Newer version with appropriate distane will be matched.
        """
        # TODO: tolerance TBD.
        currentDrive = self.getSelectedCDDrive()

        gfxboot_cfg = self.locate_gfxboot_cfg('%s\\' % currentDrive.DeviceID)
        if not gfxboot_cfg: return None

        config_parser = ConfigParser.ConfigParser()
        config_parser.read(gfxboot_cfg)
        distro_name = config_parser.get('base','distro')

        if not distro_name: return None

        for version in self.mainEngine.versionManager.versions:
            if levenshtein(version.name, distro_name) < tolerance:
                return version

    def onSubmit(self):
	currentDrive = self.getSelectedCDDrive()

        if not currentDrive:
	    QtGui.QMessageBox.warning(self, 'Warning', 'Please choose Pardus CD drive or folder to proceed.', QtGui.QMessageBox.Ok)
	    return False
        elif self.isEmptyDrive(currentDrive):
            QtGui.QMessageBox.warning(self, 'Could not read CD/DVD', 'You do not have CD/DVD in %s or drive is not ready. If you have a working CD/DVD in it, please try again.' % currentDrive.DeviceID, QtGui.QMessageBox.Ok)
            return False
	else:
            self.mainEngine.config.cdDrive = self.getSelectedCDDrive()
            version = self.determineCDVersion()

            if version:
                self.mainEngine.version = version
            else:
                reply = QtGui.QMessageBox.warning(self, 'Unknown Pardus CD/DVD', 'Unable to identify Pardus release of CD/DVD in %s. It is NOT recommended to continue installation. Do you want to exit?' % currentDrive.DeviceID, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
                if reply == QtGui.QMessageBox.Yes: sys.exit()
	    return False # TODO: make this true.

    def nextIndex(self):
	return 0
