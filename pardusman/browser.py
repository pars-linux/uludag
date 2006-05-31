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

import os
import zipfile

import piksemel
from utility import size_fmt
from qt import *

# no i18n yet
def _(x):
    return x

#
# Utilities
#

def pisi_paks(path):
    paks = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            if fn.endswith(".pisi"):
                paks.append(os.path.join(root, fn))
    return paks


class Component(QCheckListItem):
    def __init__(self, browser, name, pakname):
        # Component exists
        if browser.components.has_key(name):
            browser.components[name].append(pakname)
            return
        
        # New component
        self.browser = browser
        self.name = name
        QCheckListItem.__init__(self, browser.comps, name, QCheckListItem.CheckBox)
        browser.components[name] = [ pakname ]
    
    def stateChange(self, bool):
        packages = self.browser.packages
        for pak in self.browser.components[self.name]:
            if packages.has_key(pak):
                packages[pak].stateChange(bool)
        
        self.browser.list.triggerUpdate()


class Package(QCheckListItem):
    def __init__(self, browser, path):
        # Open package file
        zip = zipfile.ZipFile(path, 'r')
        doc = None
        for info in zip.infolist():
            if info.filename == "metadata.xml":
                doc = piksemel.parseString(zip.read(info.filename))
        if not doc:
            return
        
        # Collect data
        self.path = path
        pak = doc.getTag("Package")
        self.name = pak.getTagData("Name")
        self.size = os.stat(path).st_size
        self.inst_size = int(pak.getTagData("InstalledSize"))
        self.summary = pak.getTagData("Summary")
        self.deps = []
        deps = pak.getTag("RuntimeDependencies")
        if deps:
            for tag in deps.tags():
                self.deps.append(tag.firstChild().data())
        self.mark = 0
        
        # Handle component
        self.partof = pak.getTagData("PartOf")
        Component(browser, self.partof, self.name)
        
        # Add to the list
        self.browser = browser
        QCheckListItem.__init__(self, browser.list, self.name, QCheckListItem.CheckBox)
        if not browser.packages.has_key(self.name):
            browser.packages[self.name] = self
    
    def text(self, column):
        return (self.name, size_fmt(self.size), size_fmt(self.inst_size))[column]
    
    def paintCell(self, painter, cg, column, width, align):
        c = cg.text()
        if self.mark:
            cg.setColor(QColorGroup.Text, Qt.red)
        QCheckListItem.paintCell(self, painter, cg, column, width, align)
        cg.setColor(QColorGroup.Text, c)
    
    def stateChange(self, bool):
        packages = self.browser.packages
        if bool:
            if self.mark == 0:
                self.browser._select_pak(self)
            self.mark += 1
        else:
            if self.mark == 1:
                self.browser._unselect_pak(self)
            self.mark -= 1
        
        for pak in self.deps:
            if packages.has_key(pak):
                packages[pak].stateChange(bool)
        
        self.browser.list.triggerUpdate()
    
    def compare(self, other, col, ascend):
        if col == 0:
            return QListViewItem.compare(self, other, col, ascend)
        elif col == 1:
            if self.size < other.size:
                return -1
            elif self.size == other.size:
                return 0
            else:
                return 1
        elif col == 2:
            if self.inst_size < other.inst_size:
                return -1
            elif self.inst_size == other.inst_size:
                return 0
            else:
                return 1


class PackageSelectorWidget(QVBox):
    def __init__(self, parent):
        QVBox.__init__(self, parent)
        self.setSpacing(3)
        
        hb = QHBox(self)
        hb.setSpacing(3)
        hb.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        QLabel(_("Binary package folder:"), hb)
        self.package_path = QLineEdit(hb)
        self.package_path.setReadOnly(True)
        
        split = QSplitter(self)
        
        self.comps = QListView(split)
        self.comps.addColumn(_("Component"))
        self.comps.setResizeMode(QListView.AllColumns)
        self.comps.setColumnWidthMode(0, QListView.Maximum)
        self.comps.setSorting(0)
        split.setResizeMode(self.comps, QSplitter.FollowSizeHint)
        
        self.list = QListView(split)
        self.list.addColumn(_("Package"))
        self.list.addColumn(_("Archive Size"))
        self.list.addColumn(_("Installed Size"))
        self.list.setResizeMode(QListView.AllColumns)
        self.list.setColumnAlignment(1, Qt.AlignRight)
        self.list.setColumnAlignment(2, Qt.AlignRight)
        self.list.setColumnWidthMode(0, QListView.Maximum)
        self.list.setColumnWidthMode(1, QListView.Maximum)
        self.list.setColumnWidthMode(2, QListView.Maximum)
        split.setResizeMode(self.list, QSplitter.Stretch)
        
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        self.total = 0
        self.total_zip = 0
        self.nr_paks = 0
        self._update_label()
    
    def browse_packages(self, path):
        self.package_path.setText(path)
        self.packages = {}
        self.components = {}
        self.comps.clear()
        self.list.clear()
        for pak in pisi_paks(path):
            Package(self, pak)
    
    def get_selection(self):
        comps = []
        item = self.comps.firstChild()
        while item:
            if item.isOn():
                comps.append(item.name)
            item = item.nextSibling()
        
        selpaks = []
        allpaks = []
        item = self.list.firstChild()
        while item:
            if item.mark > 0:
                if item.isOn():
                    selpaks.append(item.path)
                allpaks.append(item.path)
            item = item.nextSibling()
        
        return (comps, selpaks, allpaks)
    
    def set_selection(self, selection):
        for name in selection[0]:
            item = self.comps.firstChild()
            while item:
                if item.name == name:
                    item.setState(QCheckListItem.On)
                item = item.nextSibling()
        
        for path in selection[1]:
            item = self.list.firstChild()
            while item:
                if item.path == path:
                    item.setState(QCheckListItem.On)
                item = item.nextSibling()
    
    def _update_label(self):
        if self.nr_paks == 0:
            self.label.setText(_("No packages selected."))
        else:
            self.label.setText(
                _("%d packages selected, %s bytes archive size, %s bytes installed size.") %
                (self.nr_paks, size_fmt(self.total_zip), size_fmt(self.total)))
    
    def _select_pak(self, pak):
        self.total_zip += pak.size
        self.total += pak.inst_size
        self.nr_paks += 1
        self._update_label()
    
    def _unselect_pak(self, pak):
        self.total_zip -= pak.size
        self.total -= pak.inst_size
        self.nr_paks -= 1
        self._update_label()


class PackageSelector(QDialog):
    def __init__(self, parent, path, callback, selection):
        QDialog.__init__(self, parent)
        self.callback = callback
        vb = QVBoxLayout(self, 6)
        self.selector = PackageSelectorWidget(self)
        self.selector.setMinimumSize(620, 420)
        vb.addWidget(self.selector)
        but = QPushButton(_("Use selected packages"), self)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        vb.addWidget(but, 0, Qt.AlignRight)
        self.selector.browse_packages(path)
        if selection:
            self.selector.set_selection(selection)
        self.show()
    
    def accept(self):
        sel = self.selector
        self.callback(sel.get_selection(), sel.total_zip, sel.total)
        QDialog.accept(self)
    
    def reject(self):
        self.callback(None, 0, 0)
        QDialog.reject(self)
