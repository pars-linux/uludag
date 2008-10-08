#!/usr/bin/python
from tabbed import Ui_MainWindow
import sys
from PyQt4 import QtGui
from PyQt4  import QtCore
import pypulse

class app(QtGui.QMainWindow):
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.quit_all)
		self.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.addTab)
		self.connect(self.ui.pushButton_3, QtCore.SIGNAL("clicked()"), self.removeTab)
		self.connect(self.ui.pushButton_4, QtCore.SIGNAL("clicked()"), self.getFeedback)


	def getFeedback(self):
		feedback()

	def addTab(self):
		self.newTab  =  QtGui.QWidget()
		self.newTab.setObjectName("hede")
		self.ui.tabWidget.addTab(self.newTab, "hede")

	def removeTab(self):
		self.ui.tabWidget.removeTab(self.ui.tabWidget.currentIndex())

	def action(self):
		print "hammering"

	def quit_all(self):
		quit()

class mein(QtGui.QApplication):
	def __init__(self):
		QtGui.QApplication.__init__(self, sys.argv)


def go():
	"""
	default subscribe flags
	PA_SUBSCRIPTION_MASK_SINK
	PA_SUBSCRIPTION_MASK_SOURCE
	PA_SUBSCRIPTION_MASK_SINK_INPUT
	PA_SUBSCRIPTION_MASK_CLIENT
	PA_SUBSCRIPTION_MASK_SERVER
	"""
	pypulse.initialize()
	pypulse.context_set_state_callback()
	if pypulse.is_connection_valid:
		print "main.py: connection valid"
		#pypulse.context_set_subscribe_callback()
		pypulse.context_connect()
		# enter mainloop
		pypulse.loop()

def feedback():
	pypulse.check_values()


def main():
	main_app = mein()
	guiPart = app()
	guiPart.show()
	go()
	#main_app.go()



if __name__ == "__main__":
	main()
