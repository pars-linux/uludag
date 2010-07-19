# -*- coding: utf-8 -*-
from PyKDE4.kio import KDirWatch
from operations import *

from PyQt4.QtCore import SIGNAL, QThread

class Monitor(QThread):
	def __init__(self,app):
		"""
		Set up the initial thread for monitoring the directory
		"""
		QThread.__init__(self)
		self.dw = KDirWatch()
		self.app = app

	def run(self):
		"""
		Run condition for the thread, which will install the monitor in the directory.
		"""
		app = self.app
		(self.dw).addDir(source_path)
		app.connect(self.dw,SIGNAL("dirty(QString)"),self.doBackup)

	def doBackup(self):
		performBackup()
		self.emit(SIGNAL("backupDone"))
