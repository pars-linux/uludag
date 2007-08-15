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
from utility.account import Account
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
        # Accounts:
        if self._wizard.options.has_key("GTalk Key") or self._wizard.options.has_key("Contacts Path") or self._wizard.options.has_key("Thunderbird Profile Path"):
            account = Account()
            # GTalk Accounts:
            if self._wizard.options.has_key("GTalk Key"):
                try:
                    account.getGTalkAccounts(self._wizard.options["GTalk Key"])
                except:
                    self._wizard.progresspage.go(i18n("GTalk accounts cannot be loaded."), self._wizard.progresspage.WARNING, 0)
                else:
                    self._wizard.progresspage.go(i18n("GTalk accounts loaded."), self._wizard.progresspage.OK, 0)
            # MSN Messenger Accounts:
            if self._wizard.options.has_key("Contacts Path"):
                try:
                    account.getMSNAccounts(self._wizard.options["Contacts Path"])
                except:
                    self._wizard.progresspage.go(i18n("MSN accounts cannot be loaded."), self._wizard.progresspage.WARNING, 0)
                else:
                    self._wizard.progresspage.go(i18n("MSN accounts loaded."), self._wizard.progresspage.OK, 0)
            # Thunderbird Accounts:
            if self._wizard.options.has_key("Thunderbird Profile Path"):
                try:
                    account.getTBAccounts(self._wizard.options["Thunderbird Profile Path"])
                except:
                    self._wizard.progresspage.go(i18n("Thunderbird accounts cannot be loaded."), self._wizard.progresspage.WARNING, 0)
                else:
                    self._wizard.progresspage.go(i18n("Thunderbird accounts loaded."), self._wizard.progresspage.OK, 0)
            try:
                account.yaz()
                account.setKopeteAccounts()
                account.setKMailAccounts()
            except Exception, err:
                self._wizard.progresspage.go(err, self._wizard.progresspage.ERROR, 1000)
            else:
                self._wizard.progresspage.go(i18n("Accounts saved."), self._wizard.progresspage.OK, 1000)
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
        if self._wizard.options.has_key("GTalk Key") or self._wizard.options.has_key("Contacts Path") or self._wizard.options.has_key("Thunderbird Profile Path"):
            self._wizard.progresspage.addOperation(i18n("Accounts"), 1000)
        if self._wizard.options.has_key("links"):
            self._wizard.progresspage.addOperation(i18n("Links"), len(self._wizard.options["links"]) * 1000)
        if self._wizard.options.has_key("folders"):
            folders = self._wizard.options["folders"]
            for folder in folders:
                self._wizard.progresspage.addOperation(folder["localname"], folder["size"])
