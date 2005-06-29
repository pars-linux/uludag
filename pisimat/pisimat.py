#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import sys, time
from qt import *
import greet
import paklist

class MainWindow(QMainWindow):
	def __init__(self, *args):
		QMainWindow.__init__(self, *args)
		self.setCaption("Pisimat - Pisi Package Maker Tool")
		self.setMinimumSize(540,320)
		self.pl = paklist.PakList(self)
	
	def start(self):
		a = greet.greet(self)
		self.pl.scan_dir(a[2])

if __name__ == "__main__":
	app = QApplication(sys.argv)
	app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
	w = MainWindow()
	w.show()
	w.start()
	app.exec_loop()
