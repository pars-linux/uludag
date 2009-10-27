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
import thread
import time
import logging

# Special Modules
import utility.wall
import utility.files
from utility.bookmark import Bookmark
from utility.account import Account
from gui.progresspage import ProgressPage

def run(wizard):
    # Set First Progress Bar Steps:
    if wizard.options.has_key("Wallpaper Path"):
        wizard.progresspage.addProgress(3, 1)
    if wizard.options.has_key("Firefox Profile Path"):
        wizard.progresspage.addProgress(10, 1)
    if wizard.options.has_key("Favorites Path"):
        wizard.progresspage.addProgress(10, 1)
    if wizard.options.has_key("GTalk Key"):
        wizard.progresspage.addProgress(5, 1)
    if wizard.options.has_key("Contacts Path"):
        wizard.progresspage.addProgress(5, 1)
    if wizard.options.has_key("Thunderbird Profile Path"):
        wizard.progresspage.addProgress(15, 1)
    if wizard.options.has_key("Windows Mail Path"):
        wizard.progresspage.addProgress(15, 1)
    if wizard.options.has_key("links"):
        wizard.progresspage.addProgress(3, 1)
    if wizard.options.has_key("folders"):
        wizard.progresspage.addProgress(20, 1)
    
    
    # Initialization:
    account = Account()
    bookmark = Bookmark()
    
    
    # Control Settings and Set Second Progress Bar:
    # Wallpaper:
    if wizard.options.has_key("Wallpaper Path"):
        size = os.path.getsize(wizard.options["Wallpaper Path"])
        wizard.progresspage.addOperation(i18n("Wallpaper"), size)
        wizard.progresspage.makeProgress(3)
    # Firefox:
    if wizard.options.has_key("Firefox Profile Path"):
        try:
            bookmark.getFFBookmarks(wizard.options["Firefox Profile Path"])
        except:
            logging.warning(i18n("Firefox bookmarks cannot be loaded."))
        else:
            logging.info(i18n("Firefox bookmarks loaded."))
        wizard.progresspage.makeProgress(10)
    # Internet Explorer:
    if wizard.options.has_key("Favorites Path"):
        try:
            bookmark.getIEBookmarks(wizard.options["Favorites Path"])
        except:
            logging.warning(i18n("Internet Explorer favorites cannot be loaded."))
        else:
            logging.info(i18n("Internet Explorer favorites loaded."))
        wizard.progresspage.makeProgress(10)
    # Bookmarks:
    size = bookmark.size()
    if size > 0:
        lockfile = os.path.join(wizard.destinations["Firefox Profile Path"], "lock")
        while os.path.lexists(lockfile):
            if warning(wizard, i18n("Firefox is open. Please close it first to continue...")) == 2:
                wizard.back()
                return
        wizard.progresspage.addOperation(i18n("Bookmarks"), size)
    # Windows Mail:
    if wizard.options.has_key("Windows Mail Path"):
        try:
            account.getOEAccounts(wizard.options["Windows Mail Path"])
        except:
            logging.warning(i18n("Windows Mail accounts cannot be loaded."))
        else:
            logging.info(i18n("Windows Mail accounts loaded."))
        wizard.progresspage.makeProgress(15)
    # Thunderbird:
    if wizard.options.has_key("Thunderbird Profile Path"):
        try:
            account.getTBAccounts(wizard.options["Thunderbird Profile Path"])
        except:
            logging.warning(i18n("Thunderbird accounts cannot be loaded."))
        else:
            logging.info(i18n("Thunderbird accounts loaded."))
        wizard.progresspage.makeProgress(15)
    # MSN Messenger Accounts:
    if wizard.options.has_key("Contacts Path"):
        try:
            account.getMSNAccounts(wizard.options["Contacts Path"])
        except:
            logging.warning(i18n("MSN accounts cannot be loaded."))
        else:
            logging.info(i18n("MSN accounts loaded."))
        wizard.progresspage.makeProgress(5)
    # GTalk Accounts:
    if wizard.options.has_key("GTalk Key"):
        try:
            account.getGTalkAccounts(wizard.options["GTalk Key"])
        except:
            logging.warning(i18n("GTalk accounts cannot be loaded."))
        else:
            logging.info(i18n("GTalk accounts loaded."))
        wizard.progresspage.makeProgress(5)
    # Mail Accounts:
    size = account.accountSize(["POP3", "IMAP", "SMTP"])
    if size > 0:
        # TODO: Control KMail to be closed
        wizard.progresspage.addOperation(i18n("E-Mail Accounts"), size)
    # E-Mails:
    if wizard.options.has_key("Copy E-Mails"):
        size = account.mailSize()
        if size > 0:
            wizard.progresspage.addOperation(i18n("E-Mail Messages"), size)
    # News Accounts:
    size = account.accountSize(["NNTP"])
    if size > 0:
        # TODO: Control KNode to be closed
        wizard.progresspage.addOperation(i18n("News Accounts"), size)
    # IM Accounts:
    size = account.accountSize(["Jabber", "MSN"])
    if size > 0:
        # TODO: Control Kopete to be closed
        wizard.progresspage.addOperation(i18n("Instant Messenger Accounts"), size)
    # Files:
    wizard.options.update(wizard.filespage.getOptions())
    if wizard.options.has_key("links"):
        wizard.progresspage.makeProgress(3)
        wizard.progresspage.addOperation(i18n("Desktop Links"), len(wizard.options["links"]) * 1000)
    if wizard.options.has_key("folders"):
        # Existance of directory:
        if not os.path.isdir(wizard.options["copy destination"]):
            try:
                os.makedirs(wizard.options["copy destination"])
            except:
                warning(wizard, unicode(i18n("Folder '%s' cannot be created, please choose another folder!")) % wizard.options["copy destination"])
                wizard.back()
                return
        # Write access:
        if not os.access(wizard.options["copy destination"], os.W_OK):
            warning(wizard, unicode(i18n("You don't have permission to write to folder '%s', please choose another folder!")) % wizard.options["copy destination"])
            wizard.back()
            return
        # File size:
        for folder in wizard.options["folders"]:
            size = utility.files.totalSize(folder["files"])
            wizard.progresspage.addOperation(folder["localname"], size)
        wizard.progresspage.makeProgress(20)
    # Control total size
    free = utility.files.freeSpace(os.path.expanduser("~"))
    if wizard.progresspage.steps2 > free:
        arguments = {"size":wizard.progresspage.steps2 / 1024 / 1024, "free":free / 1024 / 1024}
        warning(wizard,unicode(i18n("Total size of files you've chosen is %(size)d MB, but you have only %(free)d MB of free space!")) % arguments)
        wizard.back()
        return
    
    
    # Applying Changes:
    # Wallpaper:
    if wizard.options.has_key("Wallpaper Path"):
        size = os.path.getsize(wizard.options["Wallpaper Path"])
        try:
            utility.wall.setWallpaper(wizard.options["Wallpaper Path"])
        except Exception, err:
            wizard.progresspage.go(err, wizard.progresspage.ERROR, size)
        else:
            wizard.progresspage.go(i18n("Wallpaper changed."), wizard.progresspage.OK, size)
    # Bookmarks:
    size = bookmark.size()
    if size > 0:
        try:
            bookmark.setFFBookmarks(wizard.destinations["Firefox Profile Path"])
        except Exception, err:
            wizard.progresspage.go(err, wizard.progresspage.ERROR, size)
        else:
            wizard.progresspage.go(i18n("Bookmarks saved."), wizard.progresspage.OK, size)
    # Mail Accounts:
    size = account.accountSize(["POP3", "IMAP", "SMTP"])
    if size > 0:
        try:
            account.setKMailAccounts()
        except Exception, err:
            wizard.progresspage.go(err, wizard.progresspage.ERROR, size)
        else:
            wizard.progresspage.go(i18n("Mail Accounts saved."), wizard.progresspage.OK, size)
    # E-Mails:
    if wizard.options.has_key("Copy E-Mails"):
        size = account.mailSize()
        if size > 0:
            try:
                account.addKMailMessages(wizard.progresspage)
            except Exception, err:
                wizard.progresspage.go(err, wizard.progresspage.ERROR, size)
            else:
                wizard.progresspage.go(i18n("Accounts saved."), wizard.progresspage.OK, 0)
    # News Accounts:
    size = account.accountSize(["NNTP"])
    if size > 0:
        try:
            account.setKNodeAccounts()
        except Exception, err:
            wizard.progresspage.go(err, wizard.progresspage.ERROR, size)
        else:
            wizard.progresspage.go(i18n("News Accounts saved."), wizard.progresspage.OK, size)
    # IM Accounts:
    size = account.accountSize(["Jabber", "MSN"])
    if size > 0:
        try:
            account.setKopeteAccounts()
        except Exception, err:
            wizard.progresspage.go(err, wizard.progresspage.ERROR, size)
        else:
            wizard.progresspage.go(i18n("Instant Messenger Accounts saved."), wizard.progresspage.OK, size)
    # Links:
    if wizard.options.has_key("links"):
        links = wizard.options["links"]
        for link in links:
            utility.files.createLink(link)
            wizard.progresspage.go(unicode(i18n("Link '%s' created.")) % link["localname"], wizard.progresspage.OK, 1000)
    # Folders:
    if wizard.options.has_key("folders"):
        folders = wizard.options["folders"]
        for folder in folders:
            foldername = os.path.join(wizard.options["copy destination"], folder["localname"])
            utility.files.copyFolder(folder, wizard.options["copy destination"], wizard.progresspage)
    
    
    # The end:
    if wizard.progresspage.progressbar2.progress() == 0:
        wizard.progresspage.label.setText(i18n("Nothing done, because no option selected. You can close the wizard..."))
    else:
        wizard.progresspage.label.setText(i18n("All operations completed. You can close the wizard..."))
    wizard.setFinishEnabled(wizard.progresspage, True)


def warning(wizard, message):
    "Shows a warning box and waits until box closes. This method should be used to become thread-safe"
    wizard.progresspage.warning = None
    event = WarningEvent(message)
    QApplication.postEvent(wizard.progresspage, event)
    # Wait until messagebox returns
    while wizard.progresspage.warning == None:
        time.sleep(0.2)
    return wizard.progresspage.warning


class WarningEvent(QCustomEvent):
    def __init__(self, message):
        QCustomEvent.__init__(self, 65456)
        self.message = message
    def getMessage(self):
        return message

