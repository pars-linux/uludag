#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import os
import sys
import zipfile
import piksemel as iks

from qt import *

packages = {}

def pisi_paks(path):
    paks = []
    for root, dirs, files in os.walk(path):
        for fn in files:
            if fn.endswith(".pisi"):
                paks.append(os.path.join(root, fn))
    return paks


class Package(QCheckListItem):
    def __init__(self, main, parent, filename, metaxml):
        self.main = main
        self.filename = filename
        pak = metaxml.getTag("Package")
        self.name = pak.getTagData("Name")
        QCheckListItem.__init__(self, parent, self.name, QCheckListItem.CheckBox)
        if not packages.has_key(self.name):
            packages[self.name] = self
        self.size = os.stat(filename).st_size
        self.inst_size = int(pak.getTagData("InstalledSize"))
        self.summary = pak.getTagData("Summary")
        self.mark = 0
        self.deps = []
        deps = pak.getTag("RuntimeDependencies")
        if deps:
            for tag in deps.tags():
                self.deps.append(tag.firstChild().data())
    
    def text(self, column):
        return (self.name, str(self.size), str(self.inst_size))[column]
    
    def paintCell(self, painter, cg, column, width, align):
        c = cg.text()
        if self.mark:
            cg.setColor(QColorGroup.Text, Qt.red)
        QCheckListItem.paintCell(self, painter, cg, column, width, align)
        cg.setColor(QColorGroup.Text, c)
    
    def stateChange(self, bool):
        if bool:
            if self.mark == 0:
                self.main.add_pak(self)
            self.mark += 1
            for pak in self.deps:
                if packages.has_key(pak):
                    packages[pak].stateChange(True)
        else:
            if self.mark == 1:
                self.main.rem_pak(self)
            self.mark -= 1
            for pak in self.deps:
                if packages.has_key(pak):
                    packages[pak].stateChange(False)
        
        self.main.list.triggerUpdate()
    
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


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setCaption(u"CD Paket Seçici")
        self.setMinimumSize(620, 420)
        
        vb = QVBox(self)
        vb.setMargin(6)
        vb.setSpacing(3)
        self.setCentralWidget(vb)
        
        self.list = QListView(vb)
        self.list.addColumn("Paket")
        self.list.addColumn(u"Arşiv Boyu")
        self.list.addColumn("Kurulu Boy")
        self.list.setResizeMode(QListView.AllColumns)
        self.list.setColumnAlignment(1, Qt.AlignRight)
        self.list.setColumnAlignment(2, Qt.AlignRight)
        self.list.setColumnWidthMode(0, QListView.Maximum)
        self.list.setColumnWidthMode(1, QListView.Maximum)
        self.list.setColumnWidthMode(2, QListView.Maximum)
        
        hb = QHBox(vb)
        
        self.label = QLabel(hb)
        self.total = 0
        self.total_zip = 0
        self.nr_paks = 0
        self.update_label()
        
        b = QPushButton("Save list...", hb)
        self.connect(b, SIGNAL("clicked()"), self.save_list)
    
    def save_list(self):
        s = QFileDialog.getSaveFileName("package.list")
        f = file(str(s), "w")
        item = self.list.firstChild()
        while item:
            if item.mark > 0:
                f.write("%s\n" % item.filename)
            item = item.nextSibling()
        f.close()
    
    def use_path(self, path):
        for pak in pisi_paks(path):
            self.parse_pisi(pak)
    
    def update_label(self):
        if self.nr_paks == 0:
            self.label.setText(u"Paket seçili değil.")
        else:
            self.label.setText(u"%d paket, %d byte arşiv, %d byte kurulu yer." % (self.nr_paks, self.total, self.total_zip))
    
    def add_pak(self, pak):
        self.total += pak.size
        self.total_zip += pak.inst_size
        self.nr_paks += 1
        self.update_label()
    
    def rem_pak(self, pak):
        self.total -= pak.size
        self.total_zip -= pak.inst_size
        self.nr_paks -= 1
        self.update_label()
    
    def parse_pisi(self, path):
        zip = zipfile.ZipFile(path, 'r')
        for info in zip.infolist():
            if info.filename == "metadata.xml":
                data = zip.read(info.filename)
                doc = iks.parseString(data)
                Package(self, self.list, path, doc)


def main():
    app = QApplication([])
    app.connect(app, SIGNAL("lastWindowClosed()"), app, SLOT("quit()"))
    w = MainWindow()
    w.show()
    w.use_path(sys.argv[1])
    app.exec_loop()

if __name__ == "__main__":
    main()
