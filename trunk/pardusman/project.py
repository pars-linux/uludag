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


class Project:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.work_dir = None
        self.release_files = None
        self.repo_uri = None
        self.media_type = "install"
        self.media_size = 700 * 1024 * 1024
        self.selected_components = []
        self.selected_packages = []
        self.all_packages = []
    
    def open(self, filename):
        try:
            doc = piksemel.parse(filename)
        except piksemel.ParseError:
            return _("Not a Pardusman project file, invalid xml!")
        if doc.name() != "PardusmanProject":
            return _("Not a Pardusman project file")
        
        self.reset()
        
        self.media_type = doc.getAttribute("type")
        self.media_size = doc.getAttribute("size")
        self.work_dir = doc.getTagData("WorkDir")
        self.release_files = doc.getTagData("ReleaseFiles")
        
        paksel = doc.getTag("PackageSelection")
        for tag in paksel.tags("SelectedComponent"):
            self.selected_components.append(tag.firstChild().data())
        for tag in paksel.tags("SelectedPackage"):
            self.selected_packages.append(tag.firstChild().data())
        for tag in paksel.tags("Package"):
            self.all_packages.append(tag.firstChild().data())
    
    def save(self, filename):
        doc = piksemel.newDocument("PardusmanProject")
        doc.setAttribute("type", self.media_type)
        doc.setAttribute("size", str(self.media_size))
        if self.work_dir:
            doc.insertTag("WorkDir").insertData(self.work_dir)
        if self.release_files:
            doc.insertTag("ReleaseFiles").insertData(self.release_files)
        if self.repo_uri:
            paks = doc.insertTag("PackageSelection")
            paks.setAttribute("repo_uri", self.repo_uri)
            for item in self.selected_components:
                paks.insertTag("SelectedComponent").insertData(item)
            for item in self.selected_packages:
                paks.insertTag("SelectedPackage").insertData(item)
            for item in self.all_packages:
                paks.insertTag("Package").insertData(item)
        data = doc.toPrettyString()
        f = file(filename, "w")
        f.write(data)
        f.close()
    
    def make(self, console):
        pass



"""
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
