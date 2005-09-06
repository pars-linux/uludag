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

import sys
import os
from qt import *

import config
import browser
import editor

class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.setCaption("Pisimat - Pisi Package Maker Tool")
        self.setMinimumSize(620,420)
        # menu
        bar = self.menuBar()
        file_ = QPopupMenu(self)
        bar.insertItem("&File", file_)
        file_.insertItem("New Package", self.new_pak, self.CTRL + self.Key_N)
        file_.insertItem("Import Ebuild", self.import_ebuild, self.CTRL + self.Key_I)
        file_.insertItem("Edit Package", self.edit_pak, self.CTRL + self.Key_E)
        file_.insertSeparator()
        file_.insertItem("Quit", self.quit, self.CTRL + self.Key_Q)
        # package list
        self.browser = browser.Browser(self)
        self.setCentralWidget(self.browser)
        self.winlist = []
    
    def quit(self):
        sys.exit(0)
    
    def new_pak(self):
        pak = self.browser.get_selected()
        if not pak:
            return
        # FIXME: show and ask for folder too
        t = QInputDialog.getText("Create a new package", "Name", QLineEdit.Normal)
        if t[1] == False:
            return
        pname = str(t[0])
        pdir = os.path.join(pak.path[:pak.path.rfind('/')], pname)
        if os.path.exists(pdir):
            print "Doh!"
            return
        os.mkdir(pdir)
        ed = editor.Editor(pdir, pname)
        ed.save()
        self.winlist.append(ed)

    
    def import_ebuild(self):
        pass
    
    def edit_pak(self):
        pak = self.browser.get_selected()
        if pak:
            ed = editor.Editor(pak.path, pak.name)
            self.winlist.append(ed)


def main():
    app = QApplication(sys.argv)
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    w = MainWindow()
    w.show()
    w.browser.collect_pspecs(config.pspec_folder)
    app.exec_loop()

if __name__ == "__main__":
    main()
