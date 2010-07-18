import sys
from PyQt4 import QtGui
from ui.controller.stepTemplate import StepWidget
from ui.gui.finish import Ui_finish

class Widget(QtGui.QWidget, StepWidget):
    finishStep = True
    heading = "Installation Completed"

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_finish()
	self.gui.setupUi(self)

    def onEnter(self):
        # Show summary on the gui.
        if hasattr(self.mainEngine, 'version') and self.mainEngine.version:
            self.gui.txtVersion.setText(self.mainEngine.version.name)
        else:
            self.gui.txtVersion.setText('Unknown Pardus version')
        self.gui.txtUsername.setText(self.mainEngine.config.username)
        self.gui.txtPassword.setText(self.mainEngine.config.password)

    def onSubmit(self):
        self.mainEngine.cleanup()

        if self.gui.chkReboot.isChecked():
            self.mainEngine.compatibility.reboot()
        else:
            sys.exit() # Succesful termination. Retcode is 0.

        return True # TODO: unreachable code statement. false recommended for latency on reboot.

    def nextIndex(self):
	return 999 # other than this window.otherwise, onSubmit won't be executed.