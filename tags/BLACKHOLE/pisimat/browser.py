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

import sys
from qt import *
import os

sys.path.append('.')
import pisi.specfile

import editor

class PSpec(QListViewItem):
    def __init__(self, parent, path):
        sf = pisi.specfile.SpecFile()
        sf.read(os.path.join(path, "pspec.xml"))
        QListViewItem.__init__(self, parent)
        self.path = path
        self.name = sf.source.name
        self.version = sf.source.version
        self.packager = sf.source.packager.name
        self.summary = sf.source.summary
    
    def text(self, column):
        return (self.name, self.version, self.packager, self.summary)[column]


class Browser(QListView):
    def __init__(self, *args):
        QListView.__init__(self, *args)
        self.addColumn("Package")
        self.addColumn("Version")
        self.addColumn("Packager")
        self.addColumn("Summary")
        self.connect(self, SIGNAL("doubleClicked(QListViewItem *, const QPoint &, int)"), self._doubleclick)
        self.winlist = []
    
    def _doubleclick(self, a, b):
        pak = self.get_selected()
        if pak:
            ed = editor.Editor(pak.path, pak.name)
            self.winlist.append(ed)
    
    def collect_pspecs(self, dirname):
        # clear old entries
        self.clear()
        # populate the list
        for root, dirs, files in os.walk(dirname):
            if "pspec.xml" in files:
                try:
                    PSpec(self, root)
                    # found a package, dont go deeper
                    for d in dirs:
                        dirs.remove(d)
                except Exception, inst:
                    print "Broken package", root
                    print inst
            # dont walk into the versioned stuff
            if ".svn" in dirs:
                dirs.remove(".svn")
    
    def get_selected(self):
        return self.selectedItem()
