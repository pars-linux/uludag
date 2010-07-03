from PyQt4 import QtGui,QtCore

from gui.widgetMain import Ui_MainWidget
import gui.stepWelcome as stepWelcome
import gui.stepConfiguration as stepConfiguration
import gui.stepSource as stepSource
import gui.stepOptISO as stepOptISO
import gui.stepOptCD as stepOptCD
import gui.stepOptInternet as stepOptInternet
import gui.stepDownloading as stepDownloading

class PaWnGui(QtGui.QWidget, Ui_MainWidget): #is also a mainWidget
    steps = [stepWelcome, stepConfiguration, stepSource, stepOptISO, stepOptCD, stepOptInternet, stepDownloading] # step screen widgets
    historyStack = []

    def __init__(self, mainEngine, parent=None):
	QtGui.QWidget.__init__(self, parent)
	Ui_MainWidget.__init__(self)

	self.mainEngine = mainEngine

	self.setupUi(self)
	self.connectSignals()
	self.populateWidgets()
	self.updateNavButtons()
	self.jumpScreen(0)
	self.show()

	self.move(300,200)

    def connectSignals(self):
	QtCore.QObject.connect(self.btnNext, QtCore.SIGNAL('clicked()'), self.goNext)
	QtCore.QObject.connect(self.btnBack, QtCore.SIGNAL('clicked()'), self.goBack)
	QtCore.QObject.connect(self.btnFinish, QtCore.SIGNAL('clicked()'), self.goFinish)


    def populateWidgets(self):
	for step in self.steps:
	    self.stackedWidget.addWidget(step.Widget(self.mainEngine))

    def	proceedScreen(self, index):
	#print 'requested to proceed to', index
	prevIndex =  self.stackedWidget.currentIndex()
	
	if not (prevIndex == index):
	    prevWidget = self.stackedWidget.widget(prevIndex)
	    if prevWidget.onSubmit():
		self.historyStack.append(prevIndex)
		self.jumpScreen(index)
		#print 'appended', self.historyStack


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

    def goFinish(self):
	pass

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
