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
import browser

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


class ProjectWindow(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
        self.setMinimumSize(560, 440)
        self.setCaption("Pardusman")
        
        mb = self.menuBar()
        file_ = QPopupMenu(self)
        mb.insertItem("&File", file_)
        file_.insertItem("&Open", self.openProject, self.CTRL + self.Key_O)
        file_.insertItem("&Save", self.saveProject, self.CTRL + self.Key_S)
        file_.insertItem("Save &as...", self.saveAsProject, self.CTRL + self.SHIFT + self.Key_S)
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
        self.toolbar = bar
        QLabel(" ", bar)
        but = QToolButton(getIconSet("package"), _("Select packages"), "lala", self.browse, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but = QToolButton(getIconSet("gear"), _("Make ISO"), "lala", self.make, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        self.console = Console(vb)
        
        self.setCentralWidget(vb)
        
        self.project_file = None
        self.project = project.Project()
        self.project2ui()
    
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
        KApplication.kApplication().closeAllWindows()
    
    def browseResult(self, comps, paks, allpaks):
        self.toolbar.setEnabled(True)
        # FIXME: set paks
    
    def browse(self):
        self.ui2project()
        repo = self.project.get_repo()
        self.toolbar.setEnabled(False)
        w = browser.Browser(self, repo, self.browseResult)
        w.show()
    
    def make(self):
        self.ui2project()
        # FIXME: self.project.make()
    
    def ui2project(self):
        tmp = unicode(self.release_files.text())
        if tmp:
            self.project.release_files = tmp
        tmp = unicode(self.work_dir.text())
        if tmp:
            self.project.work_dir = tmp
        tmp = unicode(self.repo_uri.text())
        if tmp:
            self.project.repo_uri = tmp
        if self.media_type.selectedId() == 0:
            self.project.media_type = "install"
        else:
            self.project.media_type = "live"
    
    def project2ui(self):
        tmp = self.project.release_files
        if not tmp:
            tmp = ""
        self.release_files.setText(tmp)
        tmp = self.project.work_dir
        if not tmp:
            tmp = ""
        self.work_dir.setText(tmp)
        tmp = self.project.repo_uri
        if not tmp:
            tmp = ""
        self.repo_uri.setText(tmp)
        if self.project.media_type == "install":
            self.media_type.setButton(0)
        else:
            self.media_type.setButton(1)
    
    def openProject(self):
        name = QFileDialog.getOpenFileName(".", "All (*)", self, "lala", _("Select a project..."))
        name = unicode(name)
        if name == "":
            return
        err = self.project.open(name)
        if err:
            self.console.error("%s\n" % err)
            return
        self.project_file = name
        self.project2ui()
    
    def saveProject(self):
        if self.project_file:
            self.ui2project()
            self.project.save(self.project_file)
        else:
            self.saveAsProject()
    
    def saveAsProject(self):
        name = QFileDialog.getSaveFileName(".", "All (*)", self, "lala", _("Save project as..."))
        name = unicode(name)
        if name == "":
            return
        self.ui2project()
        self.project.save(name)
        self.project_file = name


#
# Main program
#

def main(args):
    description = I18N_NOOP("Pardus distribution media maker")
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
    w = ProjectWindow()
    w.show()
    app.exec_loop()

if __name__ == "__main__":
    main(sys.argv)
