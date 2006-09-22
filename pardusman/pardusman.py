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
import select
import subprocess
import piksemel
from qt import *
from kdecore import *
from kdeui import *

from utility import *

import project

# no i18n yet
def _(x):
    return x


class Console(KTextEdit):
    def __init__(self, parent):
        KTextEdit.__init__(self, parent)
        self.setTextFormat(self.LogText)
    
    def _echo(self, sock, error=False):
        while len(select.select([sock.fileno()], [], [], 0)[0]) > 0:
            data = os.read(sock.fileno(), 1024)
            if data:
                if error:
                    self.error(data)
                else:
                    self.info(data)
            else:
                return
    
    def info(self, msg):
        self.append(unicode(msg))
    
    def state(self, msg):
        self.append("<font color=blue>%s</font>" % unicode(msg))
    
    def error(self, msg):
        self.append("<font color=red>%s</font>" % unicode(msg))
    
    def run(self, command):
        pop = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            KApplication.kApplication().processEvents()
            self._echo(pop.stdout)
            self._echo(pop.stderr, True)
            ret = pop.poll()
            if ret != None:
                return ret


class Project(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
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
        vb.setMargin(6)
        
        hb = QHBox(vb)
        hb.setSpacing(6)
        
        QLabel(hb).setPixmap(QPixmap("logo.png"))
        
        vb2 = QVBox(hb)
        vb2.setSpacing(3)
        
        box = QWidget(vb2)
        grid = QGridLayout(box, 5, 2, 6, 6)
        
        lab = QLabel(_("Repository:"), box)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.repo_uri = QLineEdit(box)
        grid.addWidget(self.repo_uri, 0, 1)
        
        lab = QLabel(_("Release files:"), box)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.release_files = QLineEdit(hb2)
        but = QPushButton("...", hb2)
        self.connect(but, SIGNAL("clicked()"), self.selectFiles)
        grid.addWidget(hb2, 1, 1)
        
        lab = QLabel(_("Work folder:"), box)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.work_dir = QLineEdit(hb2)
        but = QPushButton("...", hb2)
        self.connect(but, SIGNAL("clicked()"), self.selectWorkdir)
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
        
        bar = QToolBar("lala", None, vb2)
        QLabel(" ", bar)
        but = QToolButton(getIconSet("package"), _("Select packages"), "lala", self.browse, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but = QToolButton(getIconSet("gear"), _("Make ISO"), "lala", self.make, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        self.console = Console(vb)
        
        self.setCentralWidget(vb)
    
    def selectFiles(self):
        path = QFileDialog.getExistingDirectory(
            self.release_files.text(),
            self,
            "lala",
            _("Select release files folder"),
            False
        )
        self.release_files.setText(path)
    
    def selectWorkdir(self):
        path = QFileDialog.getExistingDirectory(
            self.work_dir.text(),
            self,
            "lala",
            _("Select folder for temporary files and cache"),
            False
        )
        self.work_dir.setText(path)
    
    def quit(self):
        qApp.closeAllWindows()
    
    def browse(self):
        import packages
        import browser
        a = packages.Repository('http://paketler.pardus.org.tr/pardus-1.1/pisi-index.xml', 'test')
        a.parse_index()
        w = browser.Browser(self, a, None)
        w.show()
    
    def make(self):
        self.console.run("ls -l")
    
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
