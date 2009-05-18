#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file

from PyQt4 import QtGui
from PyQt4.QtCore import QResource

from ui_progressdialog import Ui_ProgressDialog

class ProgressDialog(QtGui.QDialog, Ui_ProgressDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)
        self.startAnimation()

    def startAnimation(self):
        self.movie = QtGui.QMovie(self)
        self.animeLabel.setMovie(self.movie)
        self.movie.setFileName("data/pisianime.gif")
        self.movie.start()

    def updateProgress(self, progress):
        self.progressBar.setValue(progress)
