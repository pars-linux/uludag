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
from qt import *
from kdecore import *
from kdeui import *

from utility import *

import project

# no i18n yet
def _(x):
    return x


class Console(QTextEdit):
    def __init__(self, parent):
        QTextEdit.__init__(self, parent)
        self.setTextFormat(self.LogText)


class Project(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setMinimumSize(560, 440)
        self.setCaption("Pardusman")
        
        mb = self.menuBar()
        file_ = QPopupMenu(self)
        mb.insertItem("&File", file_)
        file_.insertItem("&Open", self.quit, self.CTRL + self.Key_O)
        file_.insertItem("&Save", self.quit, self.CTRL + self.Key_S)
        file_.insertItem("Save &as...", self.quit, self.CTRL + self.SHIFT + self.Key_S)
        file_.insertSeparator()
        file_.insertItem("&Quit", self.quit, self.CTRL + self.Key_Q)
        vb = QVBox(self)
        vb.setSpacing(6)
        vb.setMargin(12)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        
        QLabel(hb).setPixmap(QPixmap("logo.png"))
        
        box = QWidget(hb)
        grid = QGridLayout(box, 8, 2, 6, 6)
        
        lab = QLabel(_("Repository:"), box)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.repo_uri = QLineEdit(box)
        grid.addWidget(self.repo_uri, 0, 1)
        
        lab = QLabel(_("Release files:"), box)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.release_files = QLineEdit(hb2)
        QPushButton("...", hb2)
        grid.addWidget(hb2, 1, 1)
        
        lab = QLabel(_("Work folder:"), box)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.work_dir = QLineEdit(hb2)
        QPushButton("...", hb2)
        grid.addWidget(hb2, 2, 1)
        
        lab = QLabel(_("Media type:"), box)
        grid.addWidget(lab, 3, 0, Qt.AlignRight)
        self.media_type = QHButtonGroup(box)
        QRadioButton(_("Installation"), self.media_type)
        QRadioButton(_("Live system"), self.media_type)
        grid.addWidget(self.media_type, 3, 1)
        
        lab = QLabel(_("Media size:"), box)
        grid.addWidget(lab, 4, 0, Qt.AlignRight)
        self.media_size = QComboBox(False, box)
        self.media_size.insertItem(getIconPixmap("cdrom_unmount"), _("CD (700 MB)"), 0)
        self.media_size.insertItem(getIconPixmap("dvd_unmount"), _("DVD (4.2 GB)"), 1)
        self.media_size.insertItem(getIconPixmap("usbpendrive_unmount"), _("FlashDisk (1 GB)"), 2)
        self.media_size.insertItem(getIconPixmap("hdd_unmount"), _("Custom size"), 3)
        grid.addWidget(self.media_size, 4, 1)
        
        but = QPushButton(_("Select packages"), box)
        self.connect(but, SIGNAL("clicked()"), self.browse)
        grid.addWidget(but, 5, 1, Qt.AlignRight)
        
        self.console = Console(vb)
        
        self.setCentralWidget(vb)
    
    def quit(self):
        qApp.closeAllWindows()
    
    def browse(self):
        import packages
        import browser
        a = packages.Repository('http://paketler.pardus.org.tr/pardus-1.1/pisi-index.xml', 'test')
        a.parse_index()
        w = browser.Browser(self, a, None)
        w.show()
    
    def loadProject(self):
        name = QFileDialog.getOpenFileName(".", "All (*)", self, "lala", _("Select a project..."))
        doc = piksemel.parse(unicode(name))
        if doc.name() != "pardusman-project":
            return
        if doc.getAttribute("type") == "media":
            prj = project.Project(self)
            prj.load_project(unicode(name), doc)


#
# Main program
#

def main(args):
    description = I18N_NOOP("Pardus release media maker")
    version = "0.1"
    about = KAboutData(
        "pardusman",
        "Pardusman",
        version,
        description,
        KAboutData.License_GPL
    )
    KCmdLineArgs.init(args, about)
    app = KApplication()
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    w = Project()
    w.show()
    app.exec_loop()

if __name__ == "__main__":
    main(sys.argv)
