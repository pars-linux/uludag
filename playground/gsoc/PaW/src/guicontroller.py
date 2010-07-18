from PyQt4 import QtGui,QtCore

from ui.gui.main import Ui_main
import ui.controller.stepWelcome as stepWelcome
import ui.controller.stepConfiguration as stepConfiguration
import ui.controller.stepSource as stepSource
import ui.controller.stepOptISO as stepOptISO
import ui.controller.stepOptCD as stepOptCD
import ui.controller.stepOptUSB as stepOptUSB
import ui.controller.stepOptInternet as stepOptInternet
import ui.controller.stepDownloading as stepDownloading
import ui.controller.stepInstalling as stepInstalling
import ui.controller.stepFinish as stepFinish

class PaWGui(QtGui.QWidget, Ui_main): #is also a mainWidget
    steps = [stepWelcome, stepConfiguration, stepSource, stepOptISO, stepOptCD,
        stepOptInternet, stepOptUSB, stepDownloading, stepInstalling, stepFinish]
    historyStack = []

    def __init__(self, mainEngine, parent=None):
	QtGui.QWidget.__init__(self, parent)
	Ui_main.__init__(self)

	self.mainEngine = mainEngine

	self.setupUi(self)
	self.connectSignals()
	self.populateWidgets()
	self.updateNavButtons()
	self.jumpScreen(0)
	self.show()

	self.centerWindow()

    def connectSignals(self):
	QtCore.QObject.connect(self.btnNext, QtCore.SIGNAL('clicked()'), self.goNext)
	QtCore.QObject.connect(self.btnBack, QtCore.SIGNAL('clicked()'), self.goBack)
	QtCore.QObject.connect(self.btnFinish, QtCore.SIGNAL('clicked()'), self.goNext)


    def populateWidgets(self):
	for step in self.steps:
	    self.stackedWidget.addWidget(step.Widget(self.mainEngine))

    def	proceedScreen(self, index):
	prevIndex =  self.stackedWidget.currentIndex()
	
	if not (prevIndex == index):
	    prevWidget = self.stackedWidget.widget(prevIndex)
	    if prevWidget.onSubmit():
		self.historyStack.append(prevIndex)
		self.jumpScreen(index)

    def jumpScreen(self, index):
	self.stackedWidget.setCurrentIndex(index)
	self.onScreenChange() # event

	curWidget = self.stackedWidget.widget(index)
	curWidget.onEnter()

    def nextIndex(self):
	return self.stackedWidget.currentWidget().nextIndex()

    def goNext(self):
	self.proceedScreen(self.nextIndex())

    def goBack(self):
	if len(self.historyStack):
	    curWidget = self.stackedWidget.currentWidget()
	    if(curWidget.onRollback()):
		self.jumpScreen(self.historyStack.pop())

    def onScreenChange(self):
	self.updateNavButtons()
	self.updateHeading()

    def updateNavButtons(self):
	if len(self.historyStack) == 0:
	    self.btnBack.hide()
	    self.btnFinish.hide()
	else:
	    if self.stackedWidget.currentWidget().isFinishStep():
		self.btnBack.hide()
		self.btnNext.hide()
		self.btnFinish.show()
	    else:
		self.btnBack.show()
		self.btnFinish.hide()

    def updateHeading(self):
	heading = self.stackedWidget.currentWidget().heading
	self.lblHeading.setText(QtGui.QApplication.translate("MainWidget", heading, None, QtGui.QApplication.UnicodeUTF8))

    def centerWindow(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        x = (screen.width() - self.width()) / 2
        y = (screen.height() - self.height()) / 2
        self.move(x, y)

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.warning(self, 'Are you sure to quit?', 'Do you really want to quit the installation? If you quit, everything installed will be removed.', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply ==  QtGui.QMessageBox.Yes:
            self.mainEngine.cleanup()
            event.accept()
        else:
            event.ignore()
