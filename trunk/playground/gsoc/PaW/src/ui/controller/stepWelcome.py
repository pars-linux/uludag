from PyQt4 import QtGui
from ui.controller.stepTemplate import StepWidget
from ui.gui.welcome import Ui_welcome

class Widget(QtGui.QWidget, StepWidget):
    heading = "Welcome to PaW!"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_welcome()
	self.gui.setupUi(self)

    def onSubmit(self):
        """
        This installer should not work for Win 95, 98, Me, 3.1 users.
        Prevent installation.
        """
        if self.mainEngine.compatibility.winMajorVersion() < 5:
            # see Compatibility.winMajorVersion method for details.
            QtGui.QMessageBox.critical(self, 'Compatibility Error', 'This installer does not support your operating system. Please install Windows 2000, XP, 2003 or newer.', QtGui.QMessageBox.Ok)
            return False
        elif not self.mainEngine.compatibility.isAdministrator():
            QtGui.QMessageBox.critical(self, 'Not Enough Privileges', 'You do not have administrator user privileges. Please try to run this program as an administrator.', QtGui.QMessageBox.Ok)
            return False

        return True
        

    def nextIndex(self):
	return 1
