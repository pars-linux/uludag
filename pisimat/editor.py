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
import re
import os
import tempfile
import sha
from qt import *
from qtext import *

sys.path.append('.')
import pisi.api
import pisi.context
import pisi.uri
import pisi.specfile
from pisi.fetcher import fetch_url

import templates
import config
import utils

class SpecEd(utils.TextEd):
    def __init__(self, path, name):
        utils.TextEd.__init__(self, path, "pspec.xml", utils.HTMLLexer())
        self.setupAPI()
        if not self.loaded:
            data = { "PACKAGE":  name, "NAME": config.name, "EMAIL": config.email, "DATE": "2005-08-06" }
            self.setText(templates.pspec_xml % (data))
    
    def setupAPI(self):
        api = QextScintillaAPIs()
        api.add("Patch")
        api.add("Dependency")
        api.add("AdditionalFile")
        self.myapi = api
        self.setAutoCompletionAPIs(self.myapi)
        self.setAutoCompletionSource(self.AcsAPIs)
        self.setAutoCompletionThreshold(1)
    
    def contextMenuEvent(self, event):
        line = self.lineAt(event.pos())
        if line == -1:
            utils.TextEd.contextMenuEvent(self, event)
            return
        event.accept()


class ActionEd(utils.TextEd):
    def __init__(self, path, name):
        utils.TextEd.__init__(self, path, "actions.py", utils.PythonLexer())
        if not self.loaded:
            data = { "PACKAGE":  name, "NAME": config.name, "EMAIL": config.email }
            self.setText(templates.actions_py % (data))


class PisiOut(QTextEdit):
    pass


class Editor(QMainWindow):
    def __init__(self, path, name):
        QMainWindow.__init__(self)
        self.setMinimumSize(540, 320)
        self.setCaption(name + " - " + path + " - pisimat")
        self.statusBar()
        self.pak_path = path
        self.pak_name = name
        # menu
        bar = self.menuBar()
        file_ = QPopupMenu(self)
        bar.insertItem("&File", file_)
        file_.insertItem("Save", self.save, self.CTRL + self.Key_S)
        file_.insertSeparator()
        file_.insertItem("Close", self.close, self.CTRL + self.Key_Q)
        tools = QPopupMenu(self)
        bar.insertItem("&Tools", tools)
        tools.insertItem("Fetch source", self.tools_fetch)
        pisi = QPopupMenu(self)
        bar.insertItem("&Pisi", pisi)
        pisi.insertItem("Validate PSpec", self.pisi_validate, self.CTRL + self.Key_V)
        pisi.insertSeparator()
        pisi.insertItem("Fetch", self.pisi_fetch, self.CTRL + self.Key_F)
        pisi.insertItem("Unpack", self.pisi_unpack, self.CTRL + self.Key_U)
        pisi.insertItem("Compile", self.pisi_compile, self.CTRL + self.Key_C)
        pisi.insertItem("Build", self.pisi_build, self.CTRL + self.Key_B)
        # editing area
        tab = QTabWidget(self)
        self.tab = tab
        tab.setTabPosition(tab.Bottom)
        self.setCentralWidget(tab)
        # pspec tab
        self.spec_ed = SpecEd(path, name)
        self.connect(self.spec_ed, SIGNAL("textChanged()"), self._spec_tab)
        tab.addTab(self.spec_ed, "pspec.xml")
        # actions tab
        self.action_ed = ActionEd(path, name)
        self.connect(self.action_ed, SIGNAL("textChanged()"), self._action_tab)
        tab.addTab(self.action_ed, "actions.py")
        # blah
        self.pisi_out = PisiOut()
        tab.addTab(self.pisi_out, "Pisi Output")
        # show window
        self.show()
    
    def closeEvent(self, ce):
        if self.spec_ed.textModified or self.action_ed.textModified:
            r = QMessageBox.question(self, "Files are not saved!",
                "Package '%s' is modified.\nDo you want to save it?" % (self.pak_name),
                "&Save", "&Exit without saving", "&Dont exit")
            if r == 2:
                ce.ignore()
                return
            if r == 0:
                self.save()
        ce.accept()
    
    def _spec_tab(self):
        self.tab.changeTab(self.spec_ed, "*pspec.xml")
    
    def _action_tab(self):
        self.tab.changeTab(self.action_ed, "*actions.py")
    
    def tools_fetch(self):
        p = re.compile("<Archive(.*)>(.*)</Archive>")
        data = unicode(self.spec_ed.text())
        m = p.search(data)
        if not m or m.groups()[1] == "":
            QMessageBox.warning(self, "Fetch error", "Archive URI is not specified")
            return
        uri = pisi.uri.URI(m.groups()[1])
        fname = os.path.join(pisi.context.config.archives_dir(), uri.filename())
        if not os.access(fname, os.R_OK):
            try:
                fetch_url(uri, pisi.context.config.archives_dir())
            except:
                QMessageBox.warning(self, "Fetch error", "Cannot fetch URI")
                return
        f = file(fname)
        s = sha.new(f.read())
        digest = s.hexdigest()
        f.close()
        p2 = re.compile("sha1sum=\"(.*)\"")
        p3 = re.compile("sha1sum='(.*)'")
        m2 = p2.search(data, m.start(1), m.end(1))
        m3 = p3.search(data, m.start(1), m.end(1))
        if m2:
            data = data[:m2.start(1)] + digest + data[m2.end(1):]
        elif m3:
            data = data[:m3.start(1)] + digest + data[m3.end(1):]
        else:
            data = data[:m.end(1)] + " sha1sum='" + digest + "'" + data[m.end(1):]
        self.spec_ed.setText(data)
    
    def pisi_validate(self):
        data = unicode(self.spec_ed.text())
        f = tempfile.NamedTemporaryFile()
        s = data.encode("utf-8")
        f.write(s)
        f.flush()
        sf = pisi.specfile.SpecFile()
        try:
            sf.read(f.name)
            self.statusBar().message("pspec.xml is validated by pisi.")
        except Exception, inst:
            self.pisi_out.append("\n==> pspec.xml errors:\n")
            self.pisi_out.append(unicode(inst))
            self.statusBar().message("pspec.xml is invalid!")
            self.tab.setCurrentPage(2)
    
    def pisi_fetch(self):
        pisi.api.build_until(os.path.join(self.pak_path, "pspec.xml"), "unpack")
    
    def pisi_unpack(self):
        pisi.api.build_until(os.path.join(self.pak_path, "pspec.xml"), "buildaction")
    
    def pisi_compile(self):
        pisi.api.build_until(os.path.join(self.pak_path, "pspec.xml"), "installaction")
    
    def pisi_build(self):
        pisi.api.build_until(os.path.join(self.pak_path, "pspec.xml"), "buildpackages")
    
    def save(self):
        self.spec_ed.save_changes()
        self.tab.changeTab(self.spec_ed, "pspec.xml")
        self.action_ed.save_changes()
        self.tab.changeTab(self.action_ed, "actions.py")
