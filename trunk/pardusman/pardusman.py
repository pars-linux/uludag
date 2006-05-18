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
import piksemel

import browser

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
        self.setMinimumSize(620, 420)
        
        bar = self.menuBar()
        file_ = QPopupMenu(self)
        bar.insertItem("&Project", file_)
        file_.insertItem("Save...", self.save_list, self.CTRL + self.Key_S)
        file_.insertSeparator()
        file_.insertItem("Quit", self.quit, self.CTRL + self.Key_Q)
        
        self.psel = browser.PackageSelector(self)
        self.psel.setMargin(6)
        self.setCentralWidget(self.psel)
    
    def quit(self):
        qApp.quit()
    
    def save_list(self):
        s = QFileDialog.getSaveFileName("package.list")
        f = file(str(s), "w")
        item = self.list.firstChild()
        while item:
            if item.mark > 0:
                f.write("%s\n" % item.filename)
            item = item.nextSibling()
        f.close()
    
    def use_path(self, path):
        self.psel.browse_packages(path)


#
# Main program
#

def main():
    app = QApplication([])
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    w = MainWindow()
    w.show()
    w.use_path(sys.argv[1])
    app.exec_loop()

if __name__ == "__main__":
    main()
