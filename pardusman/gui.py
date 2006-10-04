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
import maker

# no i18n yet
def _(x):
    return x


class Console(KTextEdit):
    def __init__(self, parent):
        KTextEdit.__init__(self, parent)
        self.setTextFormat(self.LogText)
        self.progress_win = None
    
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
    
    def progress(self, msg=None, percent=-1):
        if percent == -1:
            if msg:
                if self.progress_win:
                    self.progress_win.setCaption(msg)
                    KApplication.kApplication().processEvents()
                    return
                self.progress_win = KProgressDialog(
                    self.parent().parent(),
                    "lala",
                    msg,
                    "",
                    False
                )
                self.progress_win.showCancelButton(False)
                self.progress_win.show()
                KApplication.kApplication().processEvents()
            else:
                if self.progress_win:
                    self.progress_win.done(0)
                self.progress_win = None
        else:
            self.progress_win.setLabel(msg)
            # otherwise KProgressDialog automatically closes itself, sigh
            if percent < 100:
                self.progress_win.progressBar().setProgress(percent)
            KApplication.kApplication().processEvents(500)


class ProjectWindow(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
        self.setMinimumSize(560, 440)
        self.project_file = None
        self.updateCaption()
        pman = QPixmap("logo.png")
        self.setIcon(pman)
        
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
        
        lab = QLabel(hb)
        lab.setPixmap(pman)
        QToolTip.add(
            lab,
            _("Pardusman says:\n\n  Teh winnars dont use teh drugs!  \n ")
        )
        
        box = QWidget(hb)
        grid = QGridLayout(box, 5, 2, 6, 6)
        
        lab = QLabel(_("Work folder:"), box)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.work_dir = QLineEdit(hb2)
        QToolTip.add(
            self.work_dir,
            _("This folder holds local repository cache\nand temporary files generated during the\nISO making process.")
        )
        but = QPushButton("...", hb2)
        self.connect(but, SIGNAL("clicked()"), self.selectWorkdir)
        grid.addWidget(hb2, 0, 1)
        
        lab = QLabel(_("Repository:"), box)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        self.repo_uri = QLineEdit(box)
        QToolTip.add(
            self.repo_uri,
            _("PiSi package repository of the distribution.\nMust be a URL pointing to the repository index\nfile (i.e. pisi-index.xml.bz2).")
        )
        grid.addWidget(self.repo_uri, 1, 1)
        
        lab = QLabel(_("Release files:"), box)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.release_files = QLineEdit(hb2)
        QToolTip.add(
            self.release_files,
            _("Content of this folder is copied\nonto the root folder of CD.")
        )
        but = QPushButton("...", hb2)
        self.connect(but, SIGNAL("clicked()"), self.selectFiles)
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
        
        bar = QToolBar("lala", None, vb)
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
        if not path.isNull():
            self.release_files.setText(path)
    
    def selectWorkdir(self):
        path = QFileDialog.getExistingDirectory(
            self.work_dir.text(),
            self,
            "lala",
            _("Select folder for temporary files and cache"),
            False
        )
        if not path.isNull():
            self.work_dir.setText(path)
    
    def quit(self):
        KApplication.kApplication().closeAllWindows()
    
    def browseResult(self, comps, paks, allpaks):
        self.toolbar.setEnabled(True)
        if comps != None:
            self.project.selected_components = comps
            self.project.selected_packages = paks
            self.project.all_packages = allpaks
    
    def browse(self):
        self.ui2project()
        repo = self.project.get_repo(self.console)
        self.toolbar.setEnabled(False)
        w = browser.Browser(
            self,
            repo,
            self.browseResult,
            self.project.selected_components,
            self.project.selected_packages
        )
        w.show()
    
    def make(self):
        self.ui2project()
        # FIXME: launch with kdesu on a konsole
        maker.make_all(self.project)
    
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
        if self.project.release_files:
            tmp = unicode(self.project.release_files)
        else:
            tmp = ""
        self.release_files.setText(tmp)
        if self.project.work_dir:
            tmp = unicode(self.project.work_dir)
        else:
            tmp = ""
        self.work_dir.setText(tmp)
        if self.project.repo_uri:
            tmp = unicode(self.project.repo_uri)
        else:
            tmp = ""
        self.repo_uri.setText(tmp)
        if self.project.media_type == "install":
            self.media_type.setButton(0)
        else:
            self.media_type.setButton(1)
    
    def updateCaption(self):
        if self.project_file:
            self.setCaption(_("%s - Pardusman") % self.project_file)
        else:
            self.setCaption(_("New project - Pardusman"))
    
    def openProject(self, tmp=0, name=None):
        if not name:
            name = QFileDialog.getOpenFileName(".", "All (*)", self, "lala", _("Select a project..."))
            if name.isNull():
                return
            name = unicode(name)
        err = self.project.open(name)
        if err:
            self.console.error("%s\n" % err)
            return
        self.project_file = name
        self.project2ui()
        self.updateCaption()
        self.console.state("Project '%s' opened." % name)
    
    def saveProject(self):
        if self.project_file:
            self.ui2project()
            self.project.save(self.project_file)
            self.console.state("Saved.")
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
        self.updateCaption()
        self.console.state("Project saved as '%s'." % name)


def gui_main(args, project_file):
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
    if project_file:
        w.openProject(name=project_file)
    w.show()
    app.exec_loop()
