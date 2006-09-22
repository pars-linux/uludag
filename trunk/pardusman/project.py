#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import piksemel

# no i18n yet
def _(x):
    return x

INSTALL, LIVE = range(2)


class Project:
    def __init__(self):
        self.filename = None
        self.work_dir = None
        self.release_files = None
        self.repo_uri = None
        self.media_type = INSTALL
        self.media_size = 700 * 1024 * 1024
        self.selected_components = []
        self.selected_packages = []
        self.all_packages = []
    
    def open(self, name):
        pass
    
    def save(self, name=None):
        pass
    
    def make(self, console):
        pass



"""
class Project(QMainWindow):
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.setMinimumSize(520, 360)
        
        self.pak_selection = None
        self.pak_size = 0
        self.pak_inst_size = 0
        self.project_name = None
        
        vb = QVBox(self)
        vb.setSpacing(6)
        vb.setMargin(6)
        self.setCentralWidget(vb)
        
        tab = QTabWidget(vb)
        self.tab = tab
        tab.setMargin(6)
        
        w = QWidget(tab)
        tab.addTab(w, _("Details"))
        
        grid = QGridLayout(w, 8, 2, 6, 6)
        
        lab = QLabel(_("Project name:"), w)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.name = QLineEdit(w)
        grid.addWidget(self.name, 0, 1)
        
        line = HLine(_("Media Content:"), w)
        grid.addMultiCellWidget(line, 1, 1, 0, 1)
        self.contentdir = makePathEntry(
            _("Release files:"),
            _("Select release files..."),
            grid, 2, w
        )
        self.cdroot = makePathEntry(
            _("Boot image:"),
            _("Select boot image..."),
            grid, 3, w, is_dir=False
        )
        
        line = HLine(_("Package selection:"), w)
        grid.addMultiCellWidget(line, 4, 4, 0, 1)
        self.sourcedir = makePathEntry(
            _("SVN checkout (source packages):"),
            _("Select SVN checkout folder..."),
            grid, 5, w
        )
        self.packagedir = makePathEntry(
            _("Binary packages:"),
            _("Select binary package folder..."),
            grid, 6, w
        )
        
        but = QPushButton(_("Select packages"), w)
        self.packagebut = but
        self.connect(but, SIGNAL("clicked()"), self.selectPackages)
        grid.addMultiCellWidget(but, 7, 7, 0, 1)
        
        self.paklabel= QLabel(w)
        grid.addMultiCellWidget(self.paklabel, 8, 8, 0, 1)
        
        self.console = Console(self)
        tab.addTab(self.console, _("Log"))
        
        hb = QHBox(vb)
        hb.setSpacing(12)
        
        but = QPushButton(_("Save"), hb)
        self.connect(but, SIGNAL("clicked()"), self.save)
        but = QPushButton(_("Save as..."), hb)
        self.connect(but, SIGNAL("clicked()"), self.save_as)
        but = QPushButton(_("Prepare Media"), hb)
        self.connect(but, SIGNAL("clicked()"), self.prepareMedia)
        
        self.updateStatus()
        
        self.show()
    
    def prepareMedia(self):
        con = self.console
        self.tab.setCurrentPage(1)
        con.state("\n==> Preparing media for '%s'\n" % self.name.text())
        op = operations.ISO(con, "tmp")
        op.setup_contents(self.contentdir.text())
        op.setup_cdroot(self.cdroot.text())
        op.setup_packages(self.pak_selection[2])
        op.setup_pisi_index(self.sourcedir.text())
        if 0 == op.make(self.name.text()):
            con.state("--- media prepared succesfully ---\n\n")
        else:
            con.state("--- operation failed ---")
    
    def save_project(self, filename):
        doc = piksemel.newDocument("pardusman-project")
        doc.setAttribute("type", "media")
        doc.insertTag("name").insertData(unicode(self.name.text()))
        doc.insertTag("release_files").insertData(unicode(self.contentdir.text()))
        doc.insertTag("boot_image").insertData(unicode(self.cdroot.text()))
        paks = doc.insertTag("packages")
        paks.setAttribute("path", unicode(self.packagedir.text()))
        paks.setAttribute("source", unicode(self.sourcedir.text()))
        if self.pak_selection:
            for item in self.pak_selection[0]:
                paks.insertTag("component").insertData(unicode(item))
            for item in self.pak_selection[1]:
                paks.insertTag("selected-package").insertData(unicode(item))
            for item in self.pak_selection[2]:
                paks.insertTag("package").insertData(unicode(item))
            paks.insertTag("zip-size").insertData(str(self.pak_size))
            paks.insertTag("installed-size").insertData(str(self.pak_inst_size))
        data = doc.toPrettyString()
        f = file(filename, "w")
        f.write(data)
        f.close()
    
    def load_project(self, filename, doc):
        self.project_name = filename
        self.name.setText(doc.getTagData("name"))
        self.contentdir.setText(doc.getTagData("release_files"))
        self.cdroot.setText(doc.getTagData("boot_image"))
        paks = doc.getTag("packages")
        self.packagedir.setText(paks.getAttribute("path"))
        self.sourcedir.setText(paks.getAttribute("source"))
        self.pak_selection = ([], [], [])
        L = self.pak_selection[0]
        for item in paks.tags("component"):
            L.append(item.firstChild().data())
        L = self.pak_selection[1]
        for item in paks.tags("selected-package"):
            L.append(item.firstChild().data())
        L = self.pak_selection[2]
        for item in paks.tags("package"):
            L.append(item.firstChild().data())
        self.updateStatus()
    
    def save(self):
        if self.project_name:
            self.save_project(self.project_name)
        else:
            self.save_as()
    
    def save_as(self):
        filename = QFileDialog.getSaveFileName(".", "All (*)", self, "lala", _("Save project as..."))
        self.project_name = unicode(filename)
        self.save_project(self.project_name)
        self.updateStatus()
    
    def updateStatus(self):
        if self.pak_selection and len(self.pak_selection[2]) > 0:
            self.paklabel.setText(_("(%d packages, %s size, %s installed)") % 
                (len(self.pak_selection[2]), utility.size_fmt(self.pak_size), utility.size_fmt(self.pak_inst_size)))
        else:
            self.paklabel.setText(_("(no packages selected yet)"))
        
        if self.project_name:
            self.setCaption(_("%s - Pardusman") % self.project_name)
        else:
            self.setCaption(_("New project - Pardusman"))
    
    def selectPackages(self):
        self.packagebut.setEnabled(False)
        self.packagedir.setEnabled(False)
        w = browser.PackageSelector(self, self.packagedir.text(), self.selectResult, self.pak_selection)
    
    def selectResult(self, selection, size, instsize):
        self.packagebut.setEnabled(True)
        self.packagedir.setEnabled(True)
        if selection:
            self.pak_selection = selection
            self.pak_size = size
            self.pak_inst_size = instsize
            self.updateStatus()
"""
