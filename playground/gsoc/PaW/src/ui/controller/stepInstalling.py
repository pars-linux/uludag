from PyQt4 import QtGui
from ui.controller.stepTemplate import StepWidget
from ui.gui.installing import Ui_installing

class Widget(QtGui.QWidget, StepWidget):
    heading = "Installing Pardus"
    installed = False

    def __init__(self, mainEngine):
	QtGui.QWidget.__init__(self,None)
	StepWidget.__init__(self, mainEngine)

	self.gui = Ui_installing()
	self.gui.setupUi(self)
        self.mainEngine.installer.connectGui(self)

    def onEnter(self):
        self.installed = False
        self.updateButtons()
        if self.mainEngine.version:
            versionName = self.mainEngine.version.name
        else:
            versionName = 'Unknown'

        self.gui.lblVersion.setText(versionName)
        self.mainEngine.installer.start()

    def updateButtons(self):
        self.mainEngine.gui.btnBack.setVisible(False)
	next = True if self.installed else False
        self.mainEngine.gui.btnNext.setEnabled(next)

    def onAdvance(self, percentage):
        self.gui.progressBar.setValue(percentage)
        currentTask = self.mainEngine.installer.tasklist.currentTask

        if currentTask:
            # TODO: bug: does not update status label:
            # most probably about threading issues.
            self.gui.lblStatus.setText(currentTask.description)

            txt = self.gui.textEdit.toPlainText()
            txt += currentTask.description+'\n'
            self.gui.textEdit.setText(txt)
            self.gui.textEdit.ensureCursorVisible() # TODO: Does not work?

        if self.mainEngine.installer.tasklist.isFinished():
            self.gui.lblStatus.setText('Finished. Click Next to proceed.')
            self.installed = True
            self.updateButtons()

    def onFinish(self):
        self.installed = True
        self.updateButtons()
        pass

    def onSubmit(self):
	return True

    def nextIndex(self):
	return 9