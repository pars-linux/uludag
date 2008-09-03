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
from utility import *
from qt import *
from kdeui import *

# i18n
def _(x):
    return unicode(i18n(x))

class DetailWindow(QDialog):
    def __init__(self, parent, package):
        QDialog.__init__(self, parent)
        #self.setMinimumSize(480, 540)
        self.setCaption(package.name)
        self.setIcon(getIconPixmap(package.icon))
        vb = QVBoxLayout(self, 6)
        
        w = QWidget(self)
        vb.addWidget(w)
        
        grid = QGridLayout(w, 5, 2, 3, 3)
        
        lab = QLabel(_("Version:"), w)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        lab = QLabel(_("%s, release %s, build %s") % (package.version, package.release, package.build), w)
        grid.addWidget(lab, 0, 1)
        
        lab = QLabel(_("Component:"), w)
        grid.addWidget(lab, 1, 0, Qt.AlignRight)
        lab = QLabel(package.component, w)
        grid.addWidget(lab, 1, 1)
        
        lab = QLabel(_("Homepage:"), w)
        grid.addWidget(lab, 2, 0, Qt.AlignRight)
        lab = KURLLabel(w)
        self.connect(lab, SIGNAL("leftClickedURL(const QString&)"), self.urlClicked)
        lab.setURL(package.homepage)
        lab.setText(package.homepage)
        grid.addWidget(lab, 2, 1)
        
        lab = QLabel(_("Summary:"), w)
        grid.addWidget(lab, 3, 0, Qt.AlignRight)
        text = QTextEdit(w)
        text.setReadOnly(True)
        text.setText(unicode(package.summary))
        grid.addWidget(text, 3, 1)
        
        lab = QLabel(_("Description:"), w)
        grid.addWidget(lab, 4, 0, Qt.AlignRight)
        text = QTextEdit(w)
        text.setReadOnly(True)
        text.setText(unicode(package.description))
        grid.addWidget(text, 4, 1)
        
        hb = QHBox(self)
        hb.setSpacing(6)
        vb.addWidget(hb)
        
        list1 = QListView(hb)
        list1.addColumn(_("Depends on:"))
        for item in package.depends:
            QListViewItem(list1, item)
        
        list2 = QListView(hb)
        list2.addColumn(_("Depended by:"))
        for item in package.revdeps:
            QListViewItem(list2, item)
    
    def urlClicked(self, url):
        os.system("kfmclient exec '%s'" % url)


class Component(QCheckListItem):
    def __init__(self, browser, comp, packages):
        self.browser = browser
        self.comp = comp
        self.packages = packages
        QCheckListItem.__init__(self, browser.comps, comp, QCheckListItem.CheckBox)
    
    def stateChange(self, bool):
        packages = self.browser.packages
        for name in self.packages:
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
        if self.mark:
            cg = QColorGroup(cg)
            cg.setColor(QColorGroup.Text, Qt.red)
        QCheckListItem.paintCell(self, painter, cg, column, width, align)
    
    def stateChange(self, bool):
        browser = self.browser
        recurse = False
        if bool:
            if self.mark == 0:
                browser._select_pak(self)
                recurse = True
            self.mark += 1
        else:
            if self.mark == 1:
                browser._unselect_pak(self)
                recurse = True
            self.mark -= 1
        
        if recurse:
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
            self.tip(self.list.itemRect(item), "<b>%s</b><br>%s<br><i>(%s)</i>" % (
                item.pak.name, item.pak.summary, item.pak.component)
            )


class SizeLabel(QLabel):
    def __init__(self, parent):
        QLabel.__init__(self, parent)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Sunken)
        self.setMargin(2)
        self.percent = 0
    
    def drawFrame(self, painter):
        QLabel.drawFrame(self, painter)
        rect = self.frameRect()
        x = rect.x()
        dx = rect.width()
        y = rect.y()
        dy = rect.height()
        for cx in range(x, x + dx, dx / 10):
            painter.drawLine(cx, y, cx, y + 3)
            painter.drawLine(cx, y + dy - 5, cx, y + dy - 2)
    
    def drawContents(self, painter):
        rect = self.contentsRect()
        dx = rect.width()
        
        rect.setWidth(dx * self.percent / 100)
        if self.percent < 99:
            painter.fillRect(rect, QBrush(Qt.green))
        else:
            painter.fillRect(rect, QBrush(Qt.red))
        rect.setWidth(dx)
        
        QLabel.drawContents(self, painter)


class BrowserWidget(QVBox):
    def __init__(self, parent, repo, mediasize):
        QVBox.__init__(self, parent)
        self.setSpacing(3)

        self.mediasize = mediasize
        
        info = KActiveLabel(self)
        info.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
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
        vb.setSpacing(3)
        split.setResizeMode(vb, QSplitter.Stretch)
        hb2 = QHBox(vb)
        hb2.setSpacing(3)
        QLabel(_("Search:"), hb2)
        self.search = KListViewSearchLine(hb2)
        
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
        self.connect(self.list, SIGNAL("doubleClicked(QListViewItem *)"), self._bring_detail)
        self.package_tipper = PackageTipper(self.list.viewport())
        self.package_tipper.list = self.list
        self.search.setListView(self.list)
        self.search.setSearchColumns([0])
        
        self.label = SizeLabel(self)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum))
        
        self.repo = repo
        self.packages = {}
        for name in repo.packages:
            self.packages[name] = Package(self, repo.packages[name])
        self.components = {}
        for name in repo.components:
            self.components[name] = Component(self, name, repo.components[name])
        self.nr_paks = 0
        self.total = 0
        self.total_zip = 0
        self._update_label()
    
    def _bring_detail(self, item):
        w = DetailWindow(self, item.pak)
        w.show()
    
    def get_selection(self):
        comps = []
        item = self.comps.firstChild()
        while item:
            if item.isOn():
                comps.append(item.comp)
            item = item.nextSibling()
        
        selpaks = []
        item = self.list.firstChild()
        while item:
            if item.mark > 0:
                if item.isOn():
                    selpaks.append(item.pak.name)
            item = item.nextSibling()
        
        return (comps, selpaks)
    
    def set_selection(self, components, packages):
        for name in components:
            item = self.comps.firstChild()
            while item:
                if item.comp == name:
                    item.setState(QCheckListItem.On)
                    break
                item = item.nextSibling()
        
        for name in packages:
            item = self.list.firstChild()
            while item:
                if item.pak.name == name:
                    item.setState(QCheckListItem.On)
                    break
                item = item.nextSibling()
    
    def _update_label(self):
        if self.nr_paks == 0:
            self.label.setText(_("No packages selected."))
        else:
            if self.mediasize != 0:
                self.label.percent = min(100 * self.total_zip / self.mediasize, 100)
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
    def __init__(self, parent, repo, callback, components, packages, mediasize):
        QDialog.__init__(self, parent)
        self.setCaption(repo.base_uri)
        self.setIcon(getIconPixmap("package"))
        self.callback = callback
        vb = QVBoxLayout(self, 6)
        self.browser = BrowserWidget(self, repo, mediasize)
        self.browser.setMinimumSize(620, 420)
        vb.addWidget(self.browser)
        but = QPushButton(_("Use selected packages"), self)
        self.connect(but, SIGNAL("clicked()"), self.accept)
        vb.addWidget(but, 0, Qt.AlignRight)
        self.browser.set_selection(components, packages)
        self.browser.list.setFocus()
    
    def accept(self):
        comps, sel = self.browser.get_selection()
        self.callback(comps, sel)
        QDialog.accept(self)
    
    def reject(self):
        self.callback(None, None)
        QDialog.reject(self)
