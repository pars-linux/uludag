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
import tempfile
import subprocess
from qt import *
from kdecore import *
from kdeui import *

from utility import *

import project
import browser

# i18n
def _(x):
    return unicode(i18n(x))

class Progress:
    def __init__(self, win):
        self.win = win
        self.dialog = None
    
    def started(self, title):
        self.dialog = KProgressDialog(self.win, "lala", title, "", False)
        self.dialog.showCancelButton(False)
        self.dialog.show()
        KApplication.kApplication().processEvents()
    
    def progress(self, msg, percent):
        self.dialog.setLabel(msg)
        # otherwise KProgressDialog automatically closes itself, sigh
        if percent < 100:
            self.dialog.progressBar().setProgress(percent)
        KApplication.kApplication().processEvents(500)
    
    def finished(self):
        if self.dialog:
            self.dialog.done(0)
        self.dialog = None


class ProjectWindow(KMainWindow):
    def __init__(self):
        KMainWindow.__init__(self)
        self.setMinimumSize(560, 240)
        self.project_file = None
        self.updateCaption()
        pman = QPixmap(locate("data", "pardusman/logo.png"))
        self.setIcon(pman)
        
        mb = self.menuBar()
        file_ = QPopupMenu(self)
        mb.insertItem(_("&File"), file_)
        file_.insertItem(_("&Open"), self.openProject, self.CTRL + self.Key_O)
        file_.insertItem(_("&Save"), self.saveProject, self.CTRL + self.Key_S)
        file_.insertItem(_("Save &as..."), self.saveAsProject, self.CTRL + self.SHIFT + self.Key_S)
        file_.insertSeparator()
        file_.insertItem(_("&Quit"), self.quit, self.CTRL + self.Key_Q)
        
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
        
        lab = QLabel(_("Title:"), box)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.title = QLineEdit(box)
        QToolTip.add(
            self.title,
            _("Title of distribution media, used in grub menu.")
        )
        grid.addWidget(self.title, 0, 1)
        
        lab = QLabel(_("Work folder:"), box)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.work_dir = QLineEdit(hb2)
        QToolTip.add(
            self.work_dir,
            _("This folder holds local repository cache\nand temporary files generated during the\nISO making process.")
        )
        but = QPushButton("...", hb2)
        self.connect(but, SIGNAL("clicked()"), self.selectWorkdir)
        grid.addWidget(hb2, 1, 1)
        
        lab = QLabel(_("Repository:"), box)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        self.repo_uri = QLineEdit(box)
        QToolTip.add(
            self.repo_uri,
            _("PiSi package repository of the distribution.\nMust be a URL pointing to the repository index\nfile (i.e. pisi-index.xml.bz2).")
        )
        grid.addWidget(self.repo_uri, 2, 1)
        
        lab = QLabel(_("Release files:"), box)
        grid.addWidget(lab, 3, 0, Qt.AlignRight)
        hb2 = QHBox(box)
        hb2.setSpacing(3)
        self.release_files = QLineEdit(hb2)
        QToolTip.add(
            self.release_files,
            _("Content of this folder is copied\nonto the root folder of CD.")
        )
        but = QPushButton("...", hb2)
        self.connect(but, SIGNAL("clicked()"), self.selectFiles)
        grid.addWidget(hb2, 3, 1)

        lab = QLabel(_("Extra Parameters:"), box)
        grid.addWidget(lab, 4, 0, Qt.AlignRight)
        self.exparams = QLineEdit(box)
        QToolTip.add(
            self.exparams,
            _("This parameters will add to the install media's GRUB")
        )
        grid.addWidget(self.exparams, 4, 1)

        lab = QLabel(_("Type:"), box)
        grid.addWidget(lab, 5, 0, Qt.AlignRight)
        self.project_type = QHButtonGroup(box)
        QRadioButton(_("Installation"), self.project_type)
        QRadioButton(_("Live system"), self.project_type)
        grid.addWidget(self.project_type, 5, 1)
        
        lab = QLabel(_("Media:"), box)
        grid.addWidget(lab, 6, 0, Qt.AlignRight)
        self.project_media = QComboBox(False, box)
        grid.addWidget(self.project_media, 6, 1)
        
        self.media_types = [
            ("cd", 700, _("CD (700 MB)"), "cdrom_unmount"),
            ("dvd", 4300, _("DVD (4.2 GB)"), "dvd_unmount"),
            ("flashdisk", 1024, _("FlashDisk (1 GB)"), "usbpendrive_unmount"),
            ("custom", 0, _("Custom size"), "hdd_unmount"),
        ]
        for media_type, media_size, label, icon in self.media_types:
            x = self.project_media.insertItem(getIconPixmap(icon), label)
        
        bar = QToolBar("lala", None, vb)
        self.toolbar = bar
        QLabel(" ", bar)
        but = QToolButton(getIconSet("reload"), _("Update Repo"), "lala", self.update, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but = QToolButton(getIconSet("package"), _("Select packages"), "lala", self.browse, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        but = QToolButton(getIconSet("gear"), _("Make ISO"), "lala", self.make, bar)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        self.console = self.statusBar()
        
        self.setCentralWidget(vb)
        
        self.project = project.Project()
        self.project2ui()
        
        self.progress = Progress(self)
    
    def getMedia(self):
        return self.media_types[self.project_media.currentItem()][0]
    
    def setMedia(self, mtype):
        index = 0
        for media_type, media_size, label, icon in self.media_types:
            if media_type == mtype:
                self.project_media.setCurrentItem(index)
                return
            index += 1
        self.project_media.setCurrentItem(len(self.media_types) - 1)
    
    def getMediaSize(self):
        return self.media_types[self.project_media.currentItem()][1] * 1024 * 1024
    
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
    
    def browseResult(self, comps, paks):
        self.toolbar.setEnabled(True)
        if comps != None:
            self.project.selected_components = comps
            self.project.selected_packages = paks
    
    def checkSettings(self):
        if not self.ui2project():
            return
        if self.project.release_files and not os.path.exists(self.project.release_files):
            self.console.message(_("Release files directory does not exist."))
            return
        return True
    
    def update(self):
        if not self.checkSettings():
            return
        self.project.get_repo(self.progress, update_repo=True)
    
    def browse(self):
        if not self.checkSettings():
            return
        repo = self.project.get_repo(self.progress)
        self.toolbar.setEnabled(False)
        w = browser.Browser(
            self,
            repo,
            self.browseResult,
            self.project.selected_components,
            self.project.selected_packages,
            self.getMediaSize()
        )
        w.show()
    
    def make(self):
        if not self.checkSettings():
            return
        repo = self.project.get_repo(self.progress)
        f = tempfile.NamedTemporaryFile()
        self.project.save(f.name)
        ppath = sys.argv[0]
        if ppath[0] != '/':
            ppath = os.path.join(os.getcwd(), ppath)
        cmd = 'konsole --notabbar --nomenubar --noclose --noframe --workdir "%s" -e "%s" make "%s"' % (os.getcwd(), ppath, f.name)
        subprocess.Popen(["kdesu", "-d", "-u", "root", "-c", cmd])
        self.f = f
    
    def ui2project(self):
        tmp = unicode(self.title.text())
        if tmp:
            self.project.title = tmp
        else:
            self.project.title = None
            self.console.message(_("Project title not given."))
            return
        tmp = unicode(self.release_files.text())
        if tmp:
            self.project.release_files = tmp
        else:
            self.project.release_files = None
        tmp = unicode(self.exparams.text())
        if tmp:
            self.project.exparams = tmp
        else:
            self.project.exparams = None
        tmp = unicode(self.work_dir.text())
        if tmp:
            self.project.work_dir = tmp
        else:
            self.project.work_dir = None
            self.console.message(_("Project directory not given."))
            return
        tmp = unicode(self.repo_uri.text())
        if tmp:
            self.project.repo_uri = tmp
        else:
            self.project.repo_uri = None
            self.console.message(_("Repository address not given."))
            return
        if self.project_type.selectedId() == 0:
            self.project.type = "install"
        else:
            self.project.type = "live"
        self.project.media = self.getMedia()
        return True
    
    def project2ui(self):
        if self.project.title:
            tmp = unicode(self.project.title)
        else:
            tmp = ""
        self.title.setText(tmp)
        if self.project.release_files:
            tmp = unicode(self.project.release_files)
        else:
            tmp = ""
        self.release_files.setText(tmp)
        if self.project.exparams:
            tmp = unicode(self.project.exparams)
        else:
            tmp = ""
        self.exparams.setText(tmp)
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
        if self.project.type == "install":
            self.project_type.setButton(0)
        else:
            self.project_type.setButton(1)
        self.setMedia(self.project.media)
    
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
            self.console.message("%s" % err)
            return
        self.project_file = name
        self.project2ui()
        self.updateCaption()
        self.console.message(_("Project '%s' opened.") % name)
    
    def saveProject(self):
        if self.project_file:
            if not self.ui2project():
                return
            self.project.save(self.project_file)
            self.console.message(_("Saved."))
        else:
            self.saveAsProject()
    
    def saveAsProject(self):
        name = QFileDialog.getSaveFileName(".", "All (*)", self, "lala", _("Save project as..."))
        name = unicode(name)
        if name == "":
            return
        if not self.ui2project():
            return
        self.project.save(name)
        self.project_file = name
        self.updateCaption()
        self.console.message(_("Project saved as '%s'.") % name)


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

    about.addCredit("Gürer Özen", None, "gurer@pardus.org.tr")
    about.addAuthor("Bahadır Kandemir", None, "bahadir@pardus.org.tr")

    KCmdLineArgs.init(args, about)
    app = KApplication()
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    w = ProjectWindow()
    if project_file:
        w.openProject(name=project_file)
    w.show()
    app.exec_loop()
