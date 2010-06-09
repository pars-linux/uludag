from PyQt4 import QtGui,QtCore

from gui.widgetMain import Ui_MainWidget
import gui.stepWelcome as stepWelcome
from gui.stepTemplate import StepWidget
import gui.stepSource as stepSource

class PaWnGui(QtGui.QWidget, Ui_MainWidget): #is also a mainWidget
    steps = [stepWelcome, stepSource] # step screen widgets
    historyStack = []

    def __init__(self, mainEngine, parent=None):
	QtGui.QWidget.__init__(self, parent)
	Ui_MainWidget.__init__(self)

	self.mainEngine = mainEngine

	self.setupUi(self)
	self.connectSignals()
	self.populateWidgets()
	self.show()

	self.jumpScreen(0) # start

	self.move(300,200)

    def connectSignals(self):
	QtCore.QObject.connect(self.btnNext, QtCore.SIGNAL('clicked()'), self.goNext)
	QtCore.QObject.connect(self.btnBack, QtCore.SIGNAL('clicked()'), self.goBack)
	QtCore.QObject.connect(self.btnFinish, QtCore.SIGNAL('clicked()'), self.goFinish)


    def populateWidgets(self):
	for step in self.steps:
	    self.stackedWidget.addWidget(step.Widget())

    def	changeScreen(self, index):
	print 'requested to change to', index

	prevIndex =  self.stackedWidget.currentIndex()
	
	if not (prevIndex == index):
	    prevWidget = self.stackedWidget.widget(prevIndex)

	    if(prevWidget.onSubmit()):
		curWidget = self.stackedWidget.widget(index)
		self.historyStack.append(prevIndex)
		self.jumpScreen(index)
		print 'changed index to ',index
		
		curWidget.onEnter()

    def jumpScreen(self, index):
	print self.historyStack
	self.stackedWidget.setCurrentIndex(index)
	self.onScreenChange() # event

    def findNextIndex(self):
	return self.stackedWidget.currentWidget().nextIndex()

    def goNext(self):
	self.changeScreen(self.findNextIndex())

    def goBack(self):
	if len(self.historyStack):
	    self.jumpScreen(self.historyStack.pop())

    def goFinish(self):
	print 'Finish!!!1'

    def onScreenChange(self):
	self.updateNavButtons()
	self.updateHeading()

    def updateNavButtons(self):
	if len(self.historyStack) == 0:
	    self.btnBack.setEnabled(False)
	    self.btnFinish.setEnabled(False)
	else:
	    if self.stackedWidget.currentWidget().isFinishStep():
		self.btnBack.setEnabled(False)
		self.btnNext.setEnabled(False)
		self.btnFinish.setEnabled(True)
	    else:
		self.btnFinish.setEnabled(False)

    def updateHeading(self):
	heading = self.stackedWidget.currentWidget().heading
	self.lblHeading.setText(QtGui.QApplication.translate("MainWidget", heading, None, QtGui.QApplication.UnicodeUTF8))