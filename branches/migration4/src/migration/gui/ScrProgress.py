#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyKDE4.kdecore import KGlobal, i18n

from migration.gui.ScreenWidget import ScreenWidget
from migration.gui import context as ctx 
from migration.utils import account
from migration.utils import bookmark
from migration.utils import wallpaper
from migration.utils import files
import logging

class ProgressPage(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.vbox = QtGui.QVBoxLayout(self)
        # Top Label:
        self.label = QtGui.QLabel(self)
        self.label.setText(i18n("Please wait while applying changes..."))
        self.label.setAlignment(Qt.AlignLeft)
        self.vbox.addWidget(self.label)
        # Progress Bar Grid Layout:
        self.progresslayout = QtGui.QGridLayout(self)
        self.vbox.addLayout(self.progresslayout)
        # Progress 1:
        self.label1 = QtGui.QLabel(self)
        self.label1.setText(i18n("Prepare: "))
        self.progresslayout.addWidget(self.label1, 0, 0)
        self.progressbar1 = QtGui.QProgressBar(self)
        self.progresslayout.addWidget(self.progressbar1, 0, 1)
        # Progress 2:
        self.label2 = QtGui.QLabel(self)
        self.label2.setText(i18n("Apply: "))
        self.progresslayout.addWidget(self.label2, 1, 0)
        self.progressbar2 = QtGui.QProgressBar(self)
        self.progresslayout.addWidget(self.progressbar2, 1, 1)
        # Operation Lines:
        self.operationlines = QtGui.QVBoxLayout()
        self.vbox.addLayout(self.operationlines)
        spacer = QtGui.QSpacerItem(5, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.vbox.addItem(spacer)
        # Progress Variables:
        self.steps1 = 0
        self.steps2 = 0
        self.progress1 = 0
        self.progress2 = 0
        self.active = 0
        self.operations = []
        self.updateProgress()

    def updateProgress(self):
        "Updates status of progress bars"
        if self.steps1 == 0:
            self.progressbar1.setValue(0)
        else:
            self.progressbar1.setValue(100 * self.progress1 / self.steps1)
        if self.steps2 == 0:
            self.progressbar2.setValue(0)
        else:
            self.progressbar2.setValue(100 * self.progress2 / self.steps2)
    def addProgress(self, number, bar=1):
        "Adds steps to progress bars"
        if bar == 1:
            self.steps1 += number
        else:
            self.steps2 += number
        self.updateProgress()
    def makeProgress(self, number, bar=1):
        "Makes progress bar step"
        if bar == 1:
            self.progress1 += number
        else:
            self.progress2 += number
        self.updateProgress()    
    def addOperation(self, name, steps):
        "Adds a new operation to the progress page"
        op = Operation(self, name, steps)
        self.oplines.addLayout(op)
        self.operations.append(op)
        self.steps2 += steps
    def customEvent(self, event):
        # Show Warning Box:
        if event.type() == 65456:
            self.warning = QtGui.QMessageBox.warning(self, i18n("Warning!"), event.message, QMessageBox.Ok, QMessageBox.Cancel, QMessageBox.NoButton)
    def go(self, log, stat, steps):
        "increments progressbar, logs changes and modify icons"
        activeop = self.operations[self.active]
        if activeop.progress + steps > activeop.steps:
            self.makeProgress(activeop.steps - activeop.progress, 2)
        else:
            self.makeProgress(steps, 2)
        if activeop.go(log, stat, steps):
            self.active += 1
            if self.active < len(self.operations):
                self.operations[self.active].start()
            else:
                self.active -= 1

class Operation(QtGui.QHBoxLayout):
    def __init__(self, parent, title, steps):
        QtGui.QHBoxLayout.__init__(self, None)
        self.title = title
        self.steps = steps
        self.mother = parent
        self.progress = 0
        self.warnings = 0
        self.errors = 0
        self.OKs = 0
        self.icon = QLabel(parent)
        self.icon.show()
        self.icon.setMinimumSize(QtGui.QSize(30, 30))
        self.icon.setMaximumSize(QtGui.QSize(30, 30))
        self.addWidget(self.icon)
        self.text = QtGui.QLabel(parent)
        self.text.setText(title)
        self.text.show()
        self.addWidget(self.text)
    def start(self):
        pix = KGlobal.iconLoader().loadIcon("1rightarrow", KIcon.Toolbar)
        self.icon.setPixmap(pix)
    def go(self, log, stat, steps):
        self.progress += steps
        if stat == ctx.OK:
            if log:
                logging.info(log)
            self.OKs += 1
        elif stat == ctx.WARNING:
            if log:
                logging.warning(log)
            self.warnings += 1
        elif stat == ctx.ERROR:
            if log:
                logging.error(log)
            self.errors += 1
        if self.progress >= self.steps:
            if self.errors > 0:
                pix = KGlobal.iconLoader().loadIcon("cancel", KIcon.Toolbar)
            elif self.warnings > 0:
                pix = KGlobal.iconLoader().loadIcon("messagebox_warning", KIcon.Toolbar)
            else:
                pix = KGlobal.iconLoader().loadIcon("apply", KIcon.Toolbar)
            self.icon.setPixmap(pix)
            return True
        else:
            return False

def warning(progresspage, message):
    "Shows a warning box and waits until box closes. This method should be used to become thread-safe"
    progresspage.warning = None
    event = WarningEvent(message)
    QApplication.postEvent(progresspage, event)
    # Wait until messagebox returns
    while progresspage.warning == None:
        time.sleep(0.2)
    return progresspage.warning


class WarningEvent(QtCore.QEvent):
    def __init__(self, message):
        QtCore.QEvent.__init__(self, 65456)
        self.message = message
    def getMessage(self):
        return message

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Applying Changes")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.progresspage = ProgressPage(self)


    def run(self):
        if ctx.options.has_key("Wallpaper Path"):
            self.progresspage.addProgress(3, 1)
        if ctx.options.has_key("Firefox Profile Path"):
            self.progresspage.addProgress(10, 1)
        if ctx.options.has_key("Opera Profile Path"):
            self.progresspage.addProgress(10, 1)
        if ctx.options.has_key("Favorites Path"):
            self.progresspage.addProgress(10, 1)
        if ctx.options.has_key("GTalk Key"):
            self.progresspage.addProgress(5, 1)
        if ctx.options.has_key("Contacts Path"):
            self.progresspage.addProgress(5, 1)
        if ctx.options.has_key("Thunderbird Profile Path"):
            self.progresspage.addProgress(15, 1)
        if ctx.options.has_key("Windows Mail Path"):
            self.progresspage.addProgress(15, 1)
        if ctx.options.has_key("links"):
            self.progresspage.addProgress(3, 1)
        if ctx.options.has_key("folders"):
            self.progresspage.addProgress(20, 1)
        # Initialization:
        account = Account()
        bookmark = Bookmark()
        # Control Settings and Set Second Progress Bar:
        # Wallpaper:
        if ctx.options.has_key("Wallpaper Path"):
            size = os.path.getsize(ctx.options["Wallpaper Path"])
            self.progresspage.addOperation(i18n("Wallpaper"), size)
            self.progresspage.makeProgress(3)

        # Firefox:
        if ctx.options.has_key("Firefox Profile Path"):
            try:
                bookmark.getFFBookmarks(ctx.options["Firefox Profile Path"])
            except:
                logging.warning(i18n("Firefox bookmarks cannot be loaded."))
            else:
                logging.info(i18n("Firefox bookmarks loaded."))
            self.progresspage.makeProgress(10)

        # Opera:
        if ctx.options.has_key("Opera Profile Path"):
            try:
                bookmark.getOperaBookmarks(ctx.options["Opera Profile Path"])
            except:
                logging.warning(i18n("Opera bookmarks cannot be loaded."))
            else:
                logging.info(i18n("Opera bookmarks loaded."))
            self.progresspage.makeProgress(10)

        # Internet Explorer:
        if ctx.options.has_key("Favorites Path"):
            try:
                bookmark.getIEBookmarks(ctx.options["Favorites Path"])
            except:
                logging.warning(i18n("Internet Explorer favorites cannot be loaded."))
            else:
                logging.info(i18n("Internet Explorer favorites loaded."))
            self.progresspage.makeProgress(10)

        # Bookmarks:
        size = bookmark.size()
        if size > 0:
            lockfile = os.path.join(ctx.destinations["Firefox Profile Path"], "lock")
            while os.path.lexists(lockfile):
                if warning(self.progresspage, i18n("Firefox is open. Please close it first to continue...")) == 2:
                    return

            self.progresspage.addOperation(i18n("Bookmarks"), size)

        # Windows Mail:
        if ctx.options.has_key("Windows Mail Path"):
            try:
                account.getOEAccounts(ctx.options["Windows Mail Path"])
            except:
                logging.warning(i18n("Windows Mail accounts cannot be loaded."))
            else:
                logging.info(i18n("Windows Mail accounts loaded."))
            self.progresspage.makeProgress(15)
        # Thunderbird:
        if ctx.options.has_key("Thunderbird Profile Path"):
            try:
                account.getTBAccounts(ctx.options["Thunderbird Profile Path"])
            except:
                logging.warning(i18n("Thunderbird accounts cannot be loaded."))
            else:
                logging.info(i18n("Thunderbird accounts loaded."))
            self.progresspage.makeProgress(15)
        # MSN Messenger Accounts:
        if ctx.options.has_key("Contacts Path"):
            try:
                account.getMSNAccounts(ctx.options["Contacts Path"])
            except:
                logging.warning(i18n("MSN accounts cannot be loaded."))
            else:
                logging.info(i18n("MSN accounts loaded."))
            self.progresspage.makeProgress(5)
        # GTalk Accounts:
        if ctx.options.has_key("GTalk Key"):
            try:
                account.getGTalkAccounts(ctx.options["GTalk Key"])
            except:
                logging.warning(i18n("GTalk accounts cannot be loaded."))
            else:
                logging.info(i18n("GTalk accounts loaded."))
            self.progresspage.makeProgress(5)
        # Mail Accounts:
        size = account.accountSize(["POP3", "IMAP", "SMTP"])
        if size > 0:
            # TODO: Control KMail to be closed
            self.progresspage.addOperation(i18n("E-Mail Accounts"), size)
        # E-Mails:
        if ctx.options.has_key("Copy E-Mails"):
            size = account.mailSize()
            if size > 0:
                self.progresspage.addOperation(i18n("E-Mail Messages"), size)
        # News Accounts:
        size = account.accountSize(["NNTP"])
        if size > 0:
            # TODO: Control KNode to be closed
            self.progresspage.addOperation(i18n("News Accounts"), size)
        # IM Accounts:
        size = account.accountSize(["Jabber", "MSN"])
        if size > 0:
            # TODO: Control Kopete to be closed
            self.progresspage.addOperation(i18n("Instant Messenger Accounts"), size)
        # Files:
        ctx.options.update(ctx.filespage.options)
        if ctx.options.has_key("links"):
            self.progresspage.makeProgress(3)
            self.progresspage.addOperation(i18n("Desktop Links"), len(ctx.options["links"]) * 1000)
        if ctx.options.has_key("folders"):
            # Existance of directory:
            if not os.path.isdir(ctx.options["copy destination"]):
                try:
                    os.makedirs(ctx.options["copy destination"])
                except:
                    warning(self.progresspage , unicode(i18n("Folder '%s' cannot be created, please choose another folder!")) % ctx.options["copy destination"])
                    return
            # Write access:
            if not os.access(ctx.options["copy destination"], os.W_OK):
                warning(self.progresspage, unicode(i18n("You don't have permission to write to folder '%s', please choose another folder!")) % ctx.options["copy destination"])
                return
            # File size:
            for folder in ctx.options["folders"]:
                size = utility.files.totalSize(folder["files"])
                self.progresspage.addOperation(folder["localname"], size)
            self.progresspage.makeProgress(20)
        # Control total size
        free = utility.files.freeSpace(os.path.expanduser("~"))
        if self.progresspage.steps2 > free:
            arguments = {"size":self.progresspage.steps2 / 1024 / 1024, "free":free / 1024 / 1024}
            warning(self.progresspage, unicode(i18n("Total size of files you've chosen is %(size)d MB, but you have only %(free)d MB of free space!")) % arguments)
            return
        # Applying Changes:
        # Wallpaper:
        if ctx.options.has_key("Wallpaper Path"):
            size = os.path.getsize(ctx.options["Wallpaper Path"])
            try:
                utility.wall.setWallpaper(ctx.options["Wallpaper Path"])
            except Exception, err:
                self.progresspage.go(err, self.progresspage.ERROR, size)
            else:
                self.progresspage.go(i18n("Wallpaper changed."), self.progresspage.OK, size)
        # Bookmarks:
        size = bookmark.size()
        if size > 0:
            try:
                bookmark.setFFBookmarks(wizard.destinations["Firefox Profile Path"])
            except Exception, err:
                self.progresspage.go(err, self.progresspage.ERROR, size)
            else:
                self.progresspage.go(i18n("Bookmarks saved."), self.progresspage.OK, size)
        # Mail Accounts:
        size = account.accountSize(["POP3", "IMAP", "SMTP"])
        if size > 0:
            try:
                account.setKMailAccounts()
            except Exception, err:
                self.progresspage.go(err, self.progresspage.ERROR, size)
            else:
                self.progresspage.go(i18n("Mail Accounts saved."), self.progresspage.OK, size)
        # E-Mails:
        if ctx.options.has_key("Copy E-Mails"):
            size = account.mailSize()
            if size > 0:
                try:
                    account.addKMailMessages(self.progresspage)
                except Exception, err:
                    self.progresspage.go(err, self.progresspage.ERROR, size)
                else:
                    self.progresspage.go(i18n("Accounts saved."), self.progresspage.OK, 0)
        # News Accounts:
        size = account.accountSize(["NNTP"])
        if size > 0:
            try:
                account.setKNodeAccounts()
            except Exception, err:
                self.progresspage.go(err, self.progresspage.ERROR, size)
            else:
                self.progresspage.go(i18n("News Accounts saved."), self.progresspage.OK, size)
        # IM Accounts:
        size = account.accountSize(["Jabber", "MSN"])
        if size > 0:
            try:
                account.setKopeteAccounts()
            except Exception, err:
                self.progresspage.go(err, self.progresspage.ERROR, size)
            else:
                self.progresspage.go(i18n("Instant Messenger Accounts saved."), self.progresspage.OK, size)
        # Links:
        if ctx.options.has_key("links"):
            links = ctx.options["links"]
            for link in links:
                files.createLink(link)
                self.progresspage.go(unicode(i18n("Link '%s' created.")) % link["localname"], self.progresspage.OK, 1000)
        # Folders:
        if ctx.options.has_key("folders"):
            folders = ctx.options["folders"]
            for folder in folders:
                foldername = os.path.join(ctx.options["copy destination"], folder["localname"])
                files.copyFolder(folder, ctx.options["copy destination"], self.progresspage)
        # The end:
        if self.progresspage.progressbar2.progress() == 0:
            self.progresspage.label.setText(i18n("Nothing done, because no option selected. You can close the wizard..."))
        else:
            self.progresspage.label.setText(i18n("All operations completed. You can close the wizard..."))
    def shown(self):
        pass

    def execute(self):
        self.run()
