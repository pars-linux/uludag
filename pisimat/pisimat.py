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

class NewPakWindow(QDialog):
    def __init__(self, path):
        QDialog.__init__(self)
        self.setCaption("New Package Settings")
        vb = QVBoxLayout(self, 6)
        g = QGridLayout(vb, 2, 2, 6)
        lab = QLabel("Name", self)
        g.addWidget(lab, 0, 0)
        lab = QLabel("Folder", self)
        g.addWidget(lab, 1, 0)
        self.name = QLineEdit(self)
        g.addWidget(self.name, 0, 1)
        hb = QHBoxLayout(self, 1)
        self.dir = QLineEdit(self)
        self.dir.setText(path)
        hb.addWidget(self.dir)
        b = QPushButton("...", self)
        self.connect(b, SIGNAL("clicked()"), self.ask_file)
        hb.addWidget(b)
        g.addLayout(hb, 1, 1)
        b = QPushButton("OK", self)
        b.setDefault(True)
        self.connect(b, SIGNAL("clicked()"), self.accept)
        vb.addWidget(b)
        self.pname = None
        self.pdir = None
    
    def ask_file(self):
        s = QFileDialog.getExistingDirectory(self.dir.text(), self, "lala", "Choose package folder", False)
        self.dir.setText(s)
    
    def accept(self):
        if not self.name.text() or not self.dir.text():
            return
        QDialog.accept(self)
        self.pname = unicode(self.name.text())
        self.pdir = unicode(self.dir.text())


class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.setCaption("Pisimat - Pisi Package Maker Tool")
        self.setMinimumSize(620,420)
        # menu
        bar = self.menuBar()
        file_ = QPopupMenu(self)
        bar.insertItem("&File", file_)
        file_.insertItem("Settings", config.show, self.CTRL + self.Key_S)
        file_.insertSeparator()
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
        if pak:
            path = pak.path[:pak.path.rfind('/')]
        else:
            path = config.pspec_folder
        dlg = NewPakWindow(path)
        dlg.exec_loop()
        if not dlg.pname:
            return
        pdir = os.path.join(dlg.pdir, dlg.pname)
        if os.path.exists(pdir):
            print "Doh!"
            return
        os.mkdir(pdir)
        ed = editor.Editor(pdir, dlg.pname)
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
    config.load()
    editor.setup_pisi()
    w.browser.collect_pspecs(config.pspec_folder)
    app.exec_loop()

if __name__ == "__main__":
    main()
