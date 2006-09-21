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
from utility import size_fmt
from qt import *
from kdeui import *

# no i18n yet
def _(x):
    return x

#
# Utilities
#

class Component(QCheckListItem):
    def __init__(self, browser, comp):
        self.browser = browser
        self.comp = comp
        QCheckListItem.__init__(self, browser.comps, comp.name, QCheckListItem.CheckBox)
    
    def stateChange(self, bool):
        packages = self.browser.packages
        for name in self.comp.packages:
            packages[name].stateChange(bool)
        
        self.browser.list.triggerUpdate()


class Package(QCheckListItem):
    def __init__(self, browser, pak):
        self.browser = browser
        self.pak = pak
        self.mark = 0
        QCheckListItem.__init__(self, browser.list, self.pak.name, QCheckListItem.CheckBox)
        self.setText(1, size_fmt(pak.size))
        self.setText(2, size_fmt(pak.inst_size))
    
    def paintCell(self, painter, cg, column, width, align):
        c = cg.text()
        if self.mark:
            cg.setColor(QColorGroup.Text, Qt.red)
        QCheckListItem.paintCell(self, painter, cg, column, width, align)
        cg.setColor(QColorGroup.Text, c)
    
    def stateChange(self, bool):
        browser = self.browser
        if bool:
            if self.mark == 0:
                browser._select_pak(self)
            self.mark += 1
        else:
            if self.mark == 1:
                browser._unselect_pak(self)
            self.mark -= 1
        
        for pak in self.pak.depends:
            if browser.packages.has_key(pak):
                browser.packages[pak].stateChange(bool)
        
        browser.list.triggerUpdate()
    
    def compare(self, other, col, ascend):
        if col == 0:
            return QListViewItem.compare(self, other, col, ascend)
        elif col == 1:
            if self.pak.size < other.pak.size:
                return -1
            elif self.pak.size == other.pak.size:
                return 0
            else:
                return 1
        elif col == 2:
            if self.pak.inst_size < other.pak.inst_size:
                return -1
            elif self.pak.inst_size == other.pak.inst_size:
                return 0
            else:
                return 1


class PackageTipper(QToolTip):
    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item:
            self.tip(self.list.itemRect(item), "<b>%s</b><br>%s" % (item.pak.name, item.pak.summary))


class BrowserWidget(QVBox):
    def __init__(self, parent, repo):
        QVBox.__init__(self, parent)
        self.setSpacing(3)
        
        hb = QHBox(self)
        hb.setSpacing(3)
        hb.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        QLabel(_("Repository:"), hb)
        uri = QLineEdit(hb)
        uri.setReadOnly(True)
        uri.setText(repo.base_uri)
        
        info = QLineEdit(self)
        info.setReadOnly(True)
        info.setText(_("Total of %d packages, %s bytes compressed, %s bytes installed.") % (
            len(repo.packages),
            size_fmt(repo.size),
            size_fmt(repo.inst_size))
        )
        
        split = QSplitter(self)
        
        self.comps = QListView(split)
        self.comps.addColumn(_("Component"))
        self.comps.setResizeMode(QListView.AllColumns)
        self.comps.setColumnWidthMode(0, QListView.Maximum)
        self.comps.setSorting(0)
        split.setResizeMode(self.comps, QSplitter.FollowSizeHint)
        
        vb = QVBox(split)
        split.setResizeMode(vb, QSplitter.Stretch)
        self.search = KListViewSearchLine(vb)
        
        self.list = KListView(vb)
        self.list.addColumn(_("Package"))
        self.list.addColumn(_("Archive Size"))
        self.list.addColumn(_("Installed Size"))
        self.list.setResizeMode(QListView.AllColumns)
        self.list.setColumnAlignment(1, Qt.AlignRight)
        self.list.setColumnAlignment(2, Qt.AlignRight)
        self.list.setColumnWidthMode(0, QListView.Maximum)
        self.list.setColumnWidthMode(1, QListView.Maximum)
        self.list.setColumnWidthMode(2, QListView.Maximum)
        self.package_tipper = PackageTipper(self.list.viewport())
        self.package_tipper.list = self.list
        self.search.setListView(self.list)
        
        self.label = QLabel(self)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        
        self.repo = repo
        self.packages = {}
        for name in repo.packages:
            self.packages[name] = Package(self, repo.packages[name])
        self.components = {}
        for name in repo.components:
            self.components[name] = Component(self, repo.components[name])
        self.nr_paks = 0
        self.total = 0
        self.total_zip = 0
        self._update_label()
    
    def get_selection(self):
        comps = []
        item = self.comps.firstChild()
        while item:
            if item.isOn():
                comps.append(item.comp.name)
            item = item.nextSibling()
        
        selpaks = []
        allpaks = []
        item = self.list.firstChild()
        while item:
            if item.mark > 0:
                if item.isOn():
                    selpaks.append(item.pak.name)
                allpaks.append(item.pak.name)
            item = item.nextSibling()
        
        return (comps, selpaks, allpaks)
    
    def set_selection(self, components, packages):
        for name in components:
            item = self.comps.firstChild()
            while item:
                if item.name == name:
                    item.setState(QCheckListItem.On)
                    break
                item = item.nextSibling()
        
        for name in packages:
            item = self.list.firstChild()
            while item:
                if item.name == name:
                    item.setState(QCheckListItem.On)
                    break
                item = item.nextSibling()
    
    def _update_label(self):
        if self.nr_paks == 0:
            self.label.setText(_("No packages selected."))
        else:
            self.label.setText(
                _("%d packages selected, %s bytes archive size, %s bytes installed size.") %
                (self.nr_paks, size_fmt(self.total_zip), size_fmt(self.total)))
    
    def _select_pak(self, pak):
        self.total_zip += pak.pak.size
        self.total += pak.pak.inst_size
        self.nr_paks += 1
        self._update_label()
    
    def _unselect_pak(self, pak):
        self.total_zip -= pak.pak.size
        self.total -= pak.pak.inst_size
        self.nr_paks -= 1
        self._update_label()


class Browser(QDialog):
    def __init__(self, parent, repo, callback):
        QDialog.__init__(self, parent)
        self.callback = callback
        vb = QVBoxLayout(self, 6)
        self.browser = BrowserWidget(self, repo)
        self.browser.setMinimumSize(620, 420)
        vb.addWidget(self.browser)
        but = QPushButton(_("Use selected packages"), self)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        vb.addWidget(but, 0, Qt.AlignRight)
        self.show()
    
    def accept(self):
        comps, sel, all = self.browser.get_selection()
        self.callback(comps, sel, all)
        QDialog.accept(self)
    
    def reject(self):
        self.callback(None, None, None)
        QDialog.reject(self)
