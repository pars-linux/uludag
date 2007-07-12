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

# KDE-Qt Modules
from qt import *
from kdecore import *
from kdeui import *

# General Modules
import os

# Special Modules
import utility.wall
import utility.files
from utility.bookmark import Bookmark
from gui.progresspage import ProgressPage

class ApplyThread:
    "responsible for applying selected options and updating progress page in a thread"
    def __init__(self, wizard):
        self._wizard = wizard
    
    def run(self):
        self.prepare()
        # Wallpaper:
        if self._wizard.options.has_key("Wallpaper Path"):
            size = os.path.getsize(self._wizard.options["Wallpaper Path"])
            try:
                utility.wall.setWallpaper(self._wizard.options["Wallpaper Path"])
            except Exception, err:
                self._wizard.progresspage.go(err, self._wizard.progresspage.ERROR, size)
            else:
                self._wizard.progresspage.go(i18n("Wallpaper changed."), self._wizard.progresspage.OK, size)
        # Bookmarks:
        if self._wizard.options.has_key("Firefox Profiles Path") or self._wizard.options.has_key("Favorites Path"):
            bm = utility.bookmark.Bookmark()
            if self._wizard.options.has_key("Firefox Profile Path"):
                try:
                    bm.getFFBookmarks(self._wizard.options["Firefox Profile Path"])
                except:
                    self._wizard.progresspage.go(i18n("Firefox bookmarks cannot be loaded."), self._wizard.progresspage.WARNING, 0)
                else:
                    self._wizard.progresspage.go(i18n("Firefox bookmarks loaded."), self._wizard.progresspage.OK, 0)
            if self._wizard.options.has_key("Favorites Path"):
                try:
                    bm.getIEBookmarks(self._wizard.options["Favorites Path"])
                except:
                    self._wizard.progresspage.go(i18n("Internet Explorer favorites cannot be loaded."), self._wizard.progresspage.WARNING, 0)
                else:
                    self._wizard.progresspage.go(i18n("Internet Explorer favorites loaded."), self._wizard.progresspage.OK, 0)
            try:
                bm.setFFBookmarks(self._wizard.destinations["Firefox Profile Path"])
            except Exception, err:
                self._wizard.progresspage.go(err, self._wizard.progresspage.ERROR, 1000)
            else:
                self._wizard.progresspage.go(i18n("Bookmarks saved."), self._wizard.progresspage.OK, 1000)
        # Links:
        if self._wizard.options.has_key("links"):
            links = self._wizard.options["links"]
            for link in links:
                utility.files.createLink(link)
                self._wizard.progresspage.go(unicode(i18n("Link '%s' created.")) % link["localname"], self._wizard.progresspage.OK, 1000)
        # Folders:
        if self._wizard.options.has_key("folders"):
            folders = self._wizard.options["folders"]
            for folder in folders:
                foldername = os.path.join(self._wizard.options["copy destination"], folder["localname"])
                utility.files.copyFolder(folder, self._wizard.options["copy destination"], self._wizard.progresspage)
        # The end:
        if self._wizard.progresspage.progressbar.progress() == 0:
            self._wizard.progresspage.label.setText(i18n("Nothing done, because no option selected. You can close the wizard..."))
        elif self._wizard.progresspage.warning:
            self._wizard.progresspage.label.setText(i18n("All operations completed. You can close the wizard..."))
        else:
            self._wizard.progresspage.label.setText(i18n("All operations completed. You can close the wizard..."))
        self._wizard.setFinishEnabled(self._wizard.progresspage, True)
    
    def prepare(self):
        # Add items:
        if self._wizard.options.has_key("Wallpaper Path"):
            self._wizard.progresspage.addOperation(i18n("Wallpaper"), os.path.getsize(self._wizard.options["Wallpaper Path"]))
        if self._wizard.options.has_key("Firefox Profile Path") or self._wizard.options.has_key("Favorites Path"):
            self._wizard.progresspage.addOperation(i18n("Bookmarks"), 1000)
        if self._wizard.options.has_key("links"):
            self._wizard.progresspage.addOperation(i18n("Links"), len(self._wizard.options["links"]) * 1000)
        if self._wizard.options.has_key("folders"):
            folders = self._wizard.options["folders"]
            for folder in folders:
                self._wizard.progresspage.addOperation(folder["localname"], folder["size"])
