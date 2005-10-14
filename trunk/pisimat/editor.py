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

import time

def getDate():
    return time.strftime("%Y-%m-%d")


class SpecEd(utils.TextEd):
    def __init__(self, path, name):
        utils.TextEd.__init__(self, path, "pspec.xml", utils.HTMLLexer())
        self.setupAPI()
        if not self.loaded:
            data = { "PACKAGE":  name, "NAME": config.name, "EMAIL": config.email, "DATE": getDate() }
            self.setText(templates.pspec_xml % (data))
    
    def setupAPI(self):
        api = QextScintillaAPIs()
        for item in templates.pspec_tags:
            api.add(item)
        for item in templates.pspec_attributes:
            api.add(item)
        for item in templates.pspec_filetypes:
            api.add(item)
        self.myapi = api
        self.setAutoCompletionAPIs(self.myapi)
        self.setAutoCompletionSource(self.AcsAPIs)
        self.setAutoCompletionThreshold(1)
    
    def contextMenuEvent(self, event):
        line = self.lineAt(event.pos())
        if line == -1:
            utils.TextEd.contextMenuEvent(self, event)
            return
        str = unicode(self.text(line))
        p1 = re.compile("<Path.*fileType='(.*)'.*>")
        p2 = re.compile("<Path.*fileType=\"(.*)\".*>")
        m = p1.search(str)
        if not m:
            m = p2.search(str)
        if not m:
            utils.TextEd.contextMenuEvent(self, event)
            return
        pm = QPopupMenu(self)
        for i, item in enumerate(templates.pspec_filetypes):
            if item != m.groups()[0]:
                pm.insertItem("fileType='%s'" % (item), i)
        i = pm.exec_loop(QCursor.pos())
        if i == -1:
            return
        self.setSelection(line, m.start(1), line, m.end(1))
        self.removeSelectedText()
        self.insertAt(templates.pspec_filetypes[i], line, m.start(1))
        event.accept()


class ActionEd(utils.TextEd):
    def __init__(self, path, name):
        utils.TextEd.__init__(self, path, "actions.py", utils.PythonLexer())
        if not self.loaded:
            data = { "PACKAGE":  name, "NAME": config.name, "EMAIL": config.email }
            self.setText(templates.actions_py % (data))
        self.setupAPI()
    
    def setupAPI(self):
        api = QextScintillaAPIs()
        for item in templates.actions_api:
            api.add(item)
        self.myapi = api
        self.setAutoCompletionAPIs(self.myapi)
        self.setAutoCompletionSource(self.AcsAPIs)
        self.setAutoCompletionThreshold(2)


class PisiOut(QTextEdit):
    pass


class MyThread(QThread):
    def run(self):
        import editor
        editor.glob_ui.out = self.win.pisi_out
        editor.glob_ui.win = self.win
        try:
            pisi.api.build_until(self.path, self.stage)
            self.win.pisi_out.append("\n==> Job finished.\n")
        except Exception, inst:
            self.win.pisi_out.append("\n*** Error:\n" + str(inst) + "\n")


class Editor(QMainWindow):
    def __init__(self, path, name):
        QMainWindow.__init__(self)
        self.setMinimumSize(540, 320)
        self.setCaption(name + " - " + path + " - pisimat")
        sb = self.statusBar()
        self.progress = QProgressBar(100, self)
        sb.addWidget(self.progress)
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
        tools.insertItem("Fill paths", self.tools_paths)
        tools.insertItem("Add release", self.add_release)
        pisi = QPopupMenu(self)
        bar.insertItem("&Pisi", pisi)
        pisi.insertItem("Validate PSpec", self.pisi_validate, self.CTRL + self.Key_V)
        pisi.insertSeparator()
        pisi.insertItem("Fetch", self.pisi_fetch, self.CTRL + self.Key_F)
        pisi.insertItem("Compile", self.pisi_unpack, self.CTRL + self.Key_U)
        pisi.insertItem("Install", self.pisi_compile, self.CTRL + self.Key_C)
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
    
    def add_release(self):
        data = unicode(self.spec_ed.text())
        p = re.compile("<History>")
        m = p.search(data)
        if not m:
            QMessageBox.warning(self, "Add release error", "No <History> tag!")
            return
        dict = {
            "NAME": config.name,
            "EMAIL": config.email,
            "DATE": getDate(),
            "RELEASE": "unknown",
            "VERSION": "unknown"
        }
        verm = re.search("<Version>(.*)</Version>", data)
        relm = re.search("release='(.*)'", data)
        if not relm:
            relm = re.search('release="(.*)"', data)
        if verm:
            dict["VERSION"] = data[verm.start(1):verm.end(1)]
        if relm:
            try:
                dict["RELEASE"] = str(int(data[relm.start(1):relm.end(1)]) + 1)
            except:
                pass
        reltext = templates.pspec_release % dict
        data = data[:m.end()] + reltext + data[m.end():]
        self.spec_ed.setText(data)
    
    def tools_paths(self):
        pb = pisi.api.prepare_for_build(os.path.join(self.pak_path, "pspec.xml"))
        dirname = pb.bctx.pkg_install_dir()
        paths = ""
        for root, dirs, files in os.walk(dirname):
            relroot = root[len(dirname):]
            if relroot != "":
                paths += "\t\t<Path fileType='executable'>%s</Path>\n" % (relroot)
            if relroot.startswith("/usr/share/locale") or relroot.startswith("/usr/share/man") or relroot.startswith("/usr/share/doc"):
                for d in dirs:
                    dirs.remove(d)
        if paths == "":
            return
        p = re.compile(".*<Files>.*\n")
        data = unicode(self.spec_ed.text())
        m = p.search(data)
        if m:
            data = data[:m.end()] + paths + data[m.end():]
            self.spec_ed.setText(data)
        else:
            QMessageBox.warning(self, "Fill error", "No <Files> tag!")
    
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
        self.pisi_out.append("\n==> Fetching...")
        self.tab.setCurrentPage(2)
        a = MyThread()
        self.tatak = a
        a.win = self
        a.path = os.path.join(self.pak_path, "pspec.xml")
        a.stage = "unpack"
        a.start()
    
    def pisi_unpack(self):
        self.pisi_out.append("\n==> Compiling...")
        self.tab.setCurrentPage(2)
        a = MyThread()
        self.tatak = a
        a.win = self
        a.path = os.path.join(self.pak_path, "pspec.xml")
        a.stage = "buildaction"
        a.start()
    
    def pisi_compile(self):
        self.pisi_out.append("\n==> Installing...")
        self.tab.setCurrentPage(2)
        a = MyThread()
        self.tatak = a
        a.win = self
        a.path = os.path.join(self.pak_path, "pspec.xml")
        a.stage = "installaction"
        a.start()
    
    def pisi_build(self):
        self.pisi_out.append("\n==> Building...")
        self.tab.setCurrentPage(2)
        a = MyThread()
        self.tatak = a
        a.win = self
        a.path = os.path.join(self.pak_path, "pspec.xml")
        a.stage = "buildpackages"
        a.start()
    
    def save(self):
        self.spec_ed.save_changes()
        self.tab.changeTab(self.spec_ed, "pspec.xml")
        self.action_ed.save_changes()
        self.tab.changeTab(self.action_ed, "actions.py")


class UI:
    def display(self, msg, color):
        try:
            self.out.append(unicode(msg.encode("utf-8")))
        except:
            print msg
    
    def info(self, msg, verbose=False):
        self.display(msg, "blue")
    
    def debug(self, msg):
        self.display(msg, "black")
    
    def warning(self, msg):
        self.display(msg, "purple")
        
    def error(self, msg):
        self.display("!!! " + msg, "red")
    
    def action(self, msg):
        self.display(msg, "green")
    
    def confirm(self, msg):
        self.display(msg + " auto-confirmed.", "red")
        return True
    
    class Progress:
        def __init__(self, size):
            self.total = size
            self.percent = 0
        
        def update(self, size):
            if not self.total:
                return 100
        
            percent = (size * 100) / self.total
            if percent and self.percent is not percent:
                self.percent = percent
                return percent
            else:
                return 0
    
    def display_progress(self, pd):
        self.win.statusBar().clear()
        self.win.progress.setProgress(pd['percent'])
        if pd['percent'] == 100:
            self.win.progress.hide()


glob_ui = UI()

def setup_pisi():
    pisi.api.init(database=False, options=None, ui=glob_ui)
