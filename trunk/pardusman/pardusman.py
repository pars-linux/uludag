#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys

import project

# no i18n yet
def _(x):
    return x

from qt import *

#
# UI Classes
#


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setCaption("Pardusman")
        
        hb = QHBox(self)
        hb.setSpacing(6)
        
        QLabel(hb).setPixmap(QPixmap("logo.png"))
        
        vb = QVBox(hb)
        vb.setSpacing(12)
        but = QPushButton(_("Prepare Pardus Media"), vb)
        self.connect(but, SIGNAL("clicked()"), self.newMedia)
        but = QPushButton(_("Prepare Pardus Live Media"), vb)
        but.setEnabled(False)
        but = QPushButton(_("Load a project"), vb)
        but.setEnabled(False)
        QLabel(_("Recent projects:"), vb)
        QListBox(vb)
        but = QPushButton(_("Enough work today, Quit"), vb)
        self.connect(but, SIGNAL("clicked()"), self.quit)
        
        hb.setMargin(12)
        self.setCentralWidget(hb)
    
    def quit(self):
        qApp.quit()
    
    def newMedia(self):
        project.Project(self)


#
# Main program
#

def main():
    app = QApplication([])
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    w = MainWindow()
    w.show()
    app.exec_loop()

if __name__ == "__main__":
    main()
