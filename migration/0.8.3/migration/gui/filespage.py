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
    def __init__(self, parent, sources):
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout(self, 11, 6, "layout")
        
        self.nothing = QRadioButton(self, "nothing")
        self.nothing.setText(i18n("Do Nothing"))
        self.layout.addWidget(self.nothing)
        
        self.link = QRadioButton(self, "link")
        self.link.setText(i18n("Put links to my desktop"))
        self.link.setChecked(True)
        self.layout.addWidget(self.link)
        
        layout1 = QHBoxLayout(None, 0, 6, "layout1")
        
        self.copy = QRadioButton(self, "copy")
        self.copy.setText(i18n("Copy files to directory:"))
        layout1.addWidget(self.copy)
        
        dst = os.path.expanduser("~/Desktop")
        self.destination = QLineEdit(dst, self, "destination")
        self.destination.setEnabled(False)
        layout1.addWidget(self.destination)
        self.layout.addLayout(layout1)
        self.connect(self.copy, SIGNAL("toggled(bool)"), self.destination.setEnabled)
        
        self.group = QButtonGroup(None)
        self.group.insert(self.nothing)
        self.group.insert(self.link)
        self.group.insert(self.copy)
                
        self.dirview = DirView(self)
        self.dirview.setEnabled(False)
        self.layout.addWidget(self.dirview)
        self.connect(self.copy, SIGNAL("toggled(bool)"), self.dirview.setEnabled)
        
        # Add folders:
        folders = []
        acceptList = [("Personal Path", "My Documents", i18n("My Documents")),
                      ("Desktop Path", "Desktop", i18n("Desktop")),
                      ("My Music Path", "My Music", i18n("My Music")),
                      ("My Pictures Path", "My Pictures", i18n("My Pictures")),
                      ("My Video Path", "My Video", i18n("My Video"))]
        for key, name, localname in acceptList:
            if sources.has_key(key):
                path = sources[key]
                folders.append((path, name, unicode(localname)))
        # Check if one dir includes another:
        for index, (path, name, localname) in enumerate(folders):
            unique = True
            for index2, (path2, name2, localname2) in enumerate(folders):
                # If this is a child, skip
                if path.find(path2) == 0 and index != index2:
                    unique = False
                    break
            if unique:
                DirViewRoot(self.dirview, path, name, localname)
    
    def getOptions(self):
        options = {}
        if self.link.isChecked():
            links = []
            child = self.dirview.firstChild()
            while child:
                links.append({"path":child.path, "name":child.name, "localname":child.localname})
                child = child.nextSibling()
            options["links"] = links
        elif self.copy.isChecked():
            folders = []
            child = self.dirview.firstChild()
            while child:
                if child.state() != QCheckListItem.Off:
                    files = child.selectedFiles()
                    folders.append({"name":child.name, "localname":child.localname, "source":child.path, "files":files})
                child = child.nextSibling()
            options["folders"] = folders
            options["copy destination"] = unicode(self.destination.text())
        return options
