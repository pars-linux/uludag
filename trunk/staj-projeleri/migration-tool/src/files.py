#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import os
import shutil
import filecmp

from qt import *

from dirview import *

class FilesPage(QWidget):
    def __init__(self, parent, sources, destinations):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self, 11, 6, "layout")
        
        self.nothing = QRadioButton(self, "nothing")
        self.nothing.setText(u"Do Nothing")
        self.nothing.setChecked(True)
        self.layout.addWidget(self.nothing)
        
        self.link = QRadioButton(self, "link")
        self.link.setText(u"Put links to my desktop")
        self.layout.addWidget(self.link)
        
        layout1 = QHBoxLayout(None, 0, 6, "layout1")
        
        self.copy = QRadioButton(self, "copy")
        self.copy.setText(u"Copy files to directory:")
        layout1.addWidget(self.copy)
        
        dst = os.path.join(destinations["Home Path"], "Desktop")
        self.destination = QLineEdit(dst, self, "destination")
        self.destination.setEnabled(False)
        layout1.addWidget(self.destination)
        self.layout.addLayout(layout1)
        self.connect(self.copy, SIGNAL("toggled(bool)"), self.destination.setEnabled)
        
        self.group = QButtonGroup(None)
        self.group.insert(self.nothing)
        self.group.insert(self.link)
        self.group.insert(self.copy)
        
        folders = []
        self.folders=[]
        acceptList = [("Personal Path", u"Belgelerim"),
                      ("Desktop Path", u"Masaüstü"),
                      ("My Music Path", u"Müzik"),
                      ("My Pictures Path", u"Resim"),
                      ("My Video Path", u"Video")]
        for key, text in acceptList:
            if sources.has_key(key):
                path = sources[key]
                folders.append((text, path))
        # Check if one dir includes another:
        for index, (text, path) in enumerate(folders):
            unique = True
            for index2, (text2, path2) in enumerate(folders):
                # If this is a child, skip
                if path.find(path2) == 0 and index != index2:
                    unique = False
                    break
            if unique:
                self.folders.append((text, path))
        # Bi de boşları eklememek gerek
        self.dirview = DirView(self, sources["Home Path"], self.folders)
        self.dirview.setEnabled(False)
        self.layout.addWidget(self.dirview)
        self.connect(self.copy, SIGNAL("toggled(bool)"), self.dirview.setEnabled)
    
    def steps(self):
        if self.nothing.isChecked():
            return 0
        elif self.link.isChecked():
            return len(self.folders)
        else:
            size = 0
            for root in self.dirview.roots:
                files = root.selectedFiles()
                size += totalSize(files)
            def base(path):
                if not os.path.exists(path):
                    return base(os.path.dirname(path))
                return path
            # Check file size:
            target = os.path.join(unicode(self.destination.text()), unicode(root.text()))
            stat = os.statvfs(base(target))
            free = stat.f_bavail * stat.f_bsize
            if size >= free:
                QMessageBox.warning(self, u"Dikkat!", u"Seçtiğiniz dosyaların toplam boyutu %d MB, ancak sizin %d MB yeriniz var!"\
                 % (size / 1024 / 1024, free / 1024 / 1024), QMessageBox.Ok, QMessageBox.NoButton, QMessageBox.NoButton)
                return -1
            # Check write access:
            if not os.access(base(target), os.W_OK):
                QMessageBox.warning(self, u"Dikkat!", u"'%s' dizinine yazma hakkınız yok, farklı bir dizin seçin!" % base(target),
                QMessageBox.Ok, QMessageBox.NoButton, QMessageBox.NoButton)
                return -1
            return size
    
    def migrate(self, printwarning, printlog):
        if self.nothing.isChecked():
            pass
        elif self.link.isChecked():
            desktopfile = """
            [Desktop Entry]
            Encoding=UTF-8
            Icon=%s
            Type=Link
            URL=%s
            """
            for name, path in self.folders:
                dest = os.path.join(os.path.expanduser("~/Desktop"), "%s.desktop" % name)
                icons = {u"Belgelerim":"folder",
                         u"Masaüstü":"desktop",
                         u"Müzik":"folder_sound",
                         u"Resim":"folder_image",
                         u"Video":"folder_video"}
                dest = findName(dest)
                link = open(dest, "w")
                link.write(desktopfile % (icons[name] ,path))
                printlog("link '%s' created" % unicode(dest), 1)
                link.close()
        else:
            for root in self.dirview.roots:
                files = root.selectedFiles()        # FIXME: ikinci arama
                target = os.path.join(unicode(self.destination.text()), unicode(root.text()))
                for src in files:
                    dst = src.replace(root.name, target, 1)
                    copy(src, dst, printwarning, printlog)

def totalSize(fileList):
    "Calculates total size of a list which includes files and dirs"
    size = 0
    for item in fileList:
        if os.path.basename(item) in DirViewItem.ignoreList:
            continue
        if os.path.isfile(item):
            size += os.path.getsize(item)
        elif os.path.isdir(item):
            size += totalSize(map(lambda x: os.path.join(item, x), os.listdir(item)))
    return size

def findName(path):
    "Find a unique filename using path. If there are no file in path, don't change it."
    if not os.path.exists(path):
        return (path)
    base, ext = os.path.splitext(path)
    middle = 1
    while os.path.exists(base + "_" + str(middle) + ext):
        middle += 1
    return (base + "_" + str(middle) + ext)

def makedir(path):
    "Makes a directory and returns its name."
    # If parent not exists, create it first
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        dirname = makedir(dirname)
        path = os.path.join(dirname, os.path.basename(path))    # If parent name changed
    # If there is a file, find another name:
    if os.path.isfile(path):
        ext = 1
        while os.path.isfile(path + "_" + str(ext)):
            ext += 1
        path = (path + "_" + str(ext))
    # If directory already exists, return it
    if os.path.isdir(path):
        return path
    # If directory doesn't exists, create and return
    elif not os.path.exists(path):
        os.mkdir(path)
        return path
    else:
        raise IOError, "Directory '%s' cannot be created" % path

def copy(src, dst, printwarning, printlog):
    "Copies src to dst, considering some exceptions"
    # If it's an ignored file, do nothing
    if os.path.basename(src) in DirViewItem.ignoreList:
        return
    if os.path.isfile(src):
        dirname = os.path.dirname(dst)
        dirname = makedir(dirname)
        dst = os.path.join(dirname, os.path.basename(dst))
        # If there is already a file in dst, compare files.
        if os.path.isfile(dst):
            # If they are same, do nothing
            if filecmp.cmp(src, dst):
                printwarning("file '%s' is already exists, skipped" % unicode(src), os.path.getsize(dst))
                return
            # If they are differenf files, find another name and copy file
            else:
                dst = findName(dst)
        shutil.copy2(src, dst)
        printlog("file '%s' copied" % unicode(src), os.path.getsize(dst))
    elif os.path.isdir(src):
        dst = makedir(dst)
        files = os.listdir(src)
        for item in files:
            newdst = os.path.join(dst, item)
            newsrc = os.path.join(src, item)
            copy(newsrc, newdst, printwarning, printlog)
    else:
        raise IOError, "'%s' does not exists" % src
