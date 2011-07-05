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
from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KIconLoader, KIcon

from migration.gui.ScreenWidget import ScreenWidget
from migration.gui import context as ctx
from migration.utils.account import *
from migration.utils.bookmark import *
from migration.utils import wallpaper
from migration.utils import files
import time
import logging

class ProgressPage(QtGui.QWidget):
    #ProgressLayout Column Counter
    column = 3
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        #self.vbox = QtGui.QVBoxLayout(self)
        self.layout = QtGui.QGridLayout(self)
        # Top Label:
        self.label = QtGui.QLabel(self)
        self.label.setText(i18n("Please wait while applying changes..."))
        #self.label.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(self.label, 0, 0)

        # Progress Bar Grid Layout:
        #self.progresslayout = QtGui.QGridLayout(self)
        #self.vbox.addLayout(self.progresslayout)

        # Progress 1:
        self.label1 = QtGui.QLabel(self)
        self.label1.setText(i18n("Prepare: "))
        self.layout.addWidget(self.label1, 1, 0)
        self.progressbar1 = QtGui.QProgressBar(self)
        self.layout.addWidget(self.progressbar1, 1, 1)

        # Progress 2:
        self.label2 = QtGui.QLabel(self)
        self.label2.setText(i18n("Apply: "))
        self.layout.addWidget(self.label2, 2, 0)
        self.progressbar2 = QtGui.QProgressBar(self)
        self.layout.addWidget(self.progressbar2, 2, 1)

        # Operation Lines:
        #self.operationlines = QtGui.QVBoxLayout()
        #self.layout.addLayout(self.operationlines,)
        spacer = QtGui.QSpacerItem(5, 5, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.layout.addItem(spacer)
        self.progressLayout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.progressLayout, 3, 0)

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
        operation = Operation(self, name, steps)
        self.progressLayout.addWidget(operation)
        self.operations.append(operation)
        self.steps2 += steps

    def message(self, event):
        self.warning = QtGui.QMessageBox.warning(self, i18n("Warning!"), event, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)

#    def customEvent(self, event):
#        # Show Warning Box:
#        if event.type() == 1000:
#            self.warning = QtGui.QMessageBox.warning(self, i18n("Warning!"), event.message, QtGui.QMessageBox.Ok, QtGui.QMessageBox.Cancel, QtGui.QMessageBox.NoButton)

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

class Operation(QtGui.QWidget):

    def __init__(self, parent, title, steps):
        QtGui.QWidget.__init__(self, parent)
        self.horizantalLayout = QtGui.QHBoxLayout(self)
        self.title = title
        self.steps = steps
        self.mother = parent
        self.progress = 0
        self.warnings = 0
        self.errors = 0
        self.OKs = 0
        self.icon = QtGui.QLabel(self)
        self.icon.show()
        self.icon.setMinimumSize(QtCore.QSize(30, 30))
        self.icon.setMaximumSize(QtCore.QSize(30, 30))
        self.horizantalLayout.addWidget(self.icon)
        self.text = QtGui.QLabel(self)
        self.text.setText(title)
        self.text.show()
        self.horizantalLayout.addWidget(self.text)

    def start(self):
        pix = KIconLoader().loadIcon("1rightarrow", KIconLoader.Toolbar)
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
                pix = KIconLoader().loadIcon("dialog-cancel", KIconLoader.Toolbar)
            elif self.warnings > 0:
                pix = KIconLoader().loadIcon("emblem-important", KIconLoader.Toolbar)
            else:
                pix = KIconLoader().loadIcon("dialog-ok-apply", KIconLoader.Toolbar)
            self.icon.setPixmap(pix)
            return True
        else:
            return False

def warning(progresspage, _msg):
    "Shows a warning box and waits until box closes. This method should be used to become thread-safe"
    progresspage.warning = None
    #event = WarningEvent(message)
    #QtCore.QCoreApplication.postEvent(progresspage, event)
    # Wait until messagebox returns
    #while progresspage.warning == None:
    #    time.sleep(0.2)
    progresspage.message(_msg)
    return progresspage.warning


class WarningEvent(QtCore.QEvent):
    def __init__(self, message):
        QtCore.QEvent.__init__(self, 1000)
        self.message = message
    def getMessage(self):
        return message

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Applying Changes")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.progresspage = ProgressPage(self)
        self.vbox = QtGui.QVBoxLayout(self)
        self.vbox.addWidget(self.progresspage)

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

        print "Wallpaper:makeProgress eklendi!"

        # Firefox:
        if ctx.options.has_key("Firefox Profile Path"):
            try:
                bookmark.getFFBookmarks(ctx.options["Firefox Profile Path"])
            except:
                logging.warning(i18n("Firefox bookmarks could not be loaded."))
            else:
                logging.info(i18n("Firefox bookmarks loaded."))
            self.progresspage.makeProgress(10)

        print "Firefox:makeProgress eklendi!"

        # Opera:
        if ctx.options.has_key("Opera Profile Path"):
            try:
                bookmark.getOperaBookmarks(ctx.options["Opera Profile Path"])
            except:
                logging.warning(i18n("Opera bookmarks could not be loaded."))
            else:
                logging.info(i18n("Opera bookmarks loaded."))
            self.progresspage.makeProgress(10)

        print "Opera:makeProgress eklendi!"

        # Internet Explorer:
        if ctx.options.has_key("Favorites Path"):
            try:
                bookmark.getIEBookmarks(ctx.options["Favorites Path"])
            except:
                logging.warning(i18n("Internet Explorer favorites could not be loaded."))
            else:
                logging.info(i18n("Internet Explorer favorites loaded."))
            self.progresspage.makeProgress(10)


        print "IE:makeProgress eklendi!"

        # Bookmarks:
        size = bookmark.size()
        print "bookmark.size():%d" % size
        if size > 0:
            lockfile = os.path.join(ctx.destinations["Firefox Profile Path"], "lock")
            while os.path.lexists(lockfile):
                print "warning giriliyor..."
                if warning(self.progresspage, i18n("Firefox is open. Please close it first to continue...")) == QtGui.QMessageBox.Cancel:
                    #print "burayı geçti mi?"
                    break
            self.progresspage.addOperation(i18n("Bookmarks"), size)

        print "Bookmark:makeProgress eklendi!"

        # Windows Mail:
        if ctx.options.has_key("Windows Mail Path"):
            try:
                account.getOEAccounts(ctx.options["Windows Mail Path"])
            except:
                logging.warning(i18n("Windows Mail accounts could not be loaded."))
            else:
                logging.info(i18n("Windows Mail accounts loaded."))

            self.progresspage.makeProgress(15)

        print "WindowsMail:makeProgress eklendi!"

        # Thunderbird:
        if ctx.options.has_key("Thunderbird Profile Path"):
            try:
                account.getTBAccounts(ctx.options["Thunderbird Profile Path"])
            except:
                logging.warning(i18n("Thunderbird accounts could be loaded."))
            else:
                logging.info(i18n("Thunderbird accounts loaded."))
            self.progresspage.makeProgress(15)

        print "Thunderbird:makeProgress eklendi!"

        # MSN Messenger Accounts:
        if ctx.options.has_key("Contacts Path"):
            try:
                account.getMSNAccounts(ctx.options["Contacts Path"])
            except:
                logging.warning(i18n("MSN accounts could be loaded."))
            else:
                logging.info(i18n("MSN accounts loaded."))
            self.progresspage.makeProgress(5)

        print "MSN:makeProgress eklendi!"

        # GTalk Accounts:
        if ctx.options.has_key("GTalk Key"):
            try:
                account.getGTalkAccounts(ctx.options["GTalk Key"])
            except:
                logging.warning(i18n("GTalk accounts could not be loaded."))
            else:
                logging.info(i18n("GTalk accounts loaded."))
            self.progresspage.makeProgress(5)

        print "GTalk:makeProgress eklendi!"

        # Mail Accounts:
        size = account.accountSize(["POP3", "IMAP", "SMTP"])
        if size > 0:
            # TODO: Control KMail to be closed
            self.progresspage.addOperation(i18n("E-Mail Accounts"), size)

        print "Mail Accounts:makeProgress eklendi!"

        # E-Mails:
        if ctx.options.has_key("Copy E-Mails"):
            size = account.mailSize()
            if size > 0:
                self.progresspage.addOperation(i18n("E-Mail Messages"), size)

        print "E-mails:makeProgress eklendi!"

        # News Accounts:
        size = account.accountSize(["NNTP"])
        if size > 0:
            # TODO: Control KNode to be closed
            self.progresspage.addOperation(i18n("News Accounts"), size)

        print "New Accounts:makeProgress eklendi!"

        # IM Accounts:
        size = account.accountSize(["Jabber", "MSN"])
        if size > 0:
            # TODO: Control Kopete to be closed
            self.progresspage.addOperation(i18n("Instant Messenger Accounts"), size)

        print "IM Accounts:makeProgress eklendi!"

        # Files:
        #print "ctx.fileOptions:%s" % ctx.fileOptions
        #for k,v in ctx.fileOptions.items():
        #     print "ctx.fileOptions[%s]=%s" %(k,v)
        #ctx.options.update(ctx.filesOptions)
        if ctx.filesOptions:
            if ctx.filesOptions.has_key("links"):
                self.progresspage.makeProgress(3)
                self.progresspage.addOperation(i18n("Desktop Links"), len(ctx.filesOptions["links"]) * 1000)
            if ctx.filesOptions.has_key("folders"):
                # Existance of directory:
                if not os.path.isdir(ctx.filesOptions["copy destination"]):
                    try:
                        os.makedirs(ctx.filesOptions["copy destination"])
                    except:
                        warning(self.progresspage , unicode(i18n("Folder '%s' could not be created, please choose another folder!")) % ctx.filesOptions["copy destination"])
                        return
                # Write access:
                if not os.access(ctx.filesOptions["copy destination"], os.W_OK):
                    warning(self.progresspage, unicode(i18n("You don't have permission to write to folder '%s', please choose another folder!")) % ctx.filesOptions["copy destination"])
                    return
                # File size:
                for folder in ctx.filesOptions["folders"]:
                    size = files.totalSize(folder["files"])
                    self.progresspage.addOperation(folder["localname"], size)
                self.progresspage.makeProgress(20)
            # Control total size
            free = files.freeSpace(os.path.expanduser("~"))
            if self.progresspage.steps2 > free:
                arguments = {"size":self.progresspage.steps2 / 1024 / 1024, "free":free / 1024 / 1024}
                warning(self.progresspage, unicode(i18n("Total size of files you've selected is %(size)d MB, but you have only %(free)d MB of free space!")) % arguments)
                return

        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.progresspage.progressLayout.addItem(spacerItem)
        # Applying Changes:
        # Wallpaper:
        if ctx.options.has_key("Wallpaper Path"):
            size = os.path.getsize(ctx.options["Wallpaper Path"])
            try:
                wall.setWallpaper(ctx.options["Wallpaper Path"])
            except Exception, err:
                self.progresspage.go(err, ctx.ERROR, size)
            else:
                self.progresspage.go(i18n("Wallpaper changed."), ctx.OK, size)

        print "Wallpaper: apply!"

        # Bookmarks:
        size = bookmark.size()
        if size > 0:
            try:
                print "ctx.destinations[\"Firefox Profile Path\"]:%s" % ctx.destinations["Firefox Profile Path"]
                bookmark.setFFBookmarks(ctx.destinations["Firefox Profile Path"])
            except Exception, err:
                self.progresspage.go(err, ctx.ERROR, size)
            else:
                self.progresspage.go(i18n("Bookmarks saved."), ctx.OK, size)

        print "BookMark: apply!"

        # Mail Accounts:
        size = account.accountSize(["POP3", "IMAP", "SMTP"])
        if size > 0:
            try:
                account.setKMailAccounts()
            except Exception, err:
                self.progresspage.go(err, ctx.ERROR, size)
            else:
                self.progresspage.go(i18n("Mail Accounts saved."), ctx.OK, size)

        print "Mail: apply!"
        # E-Mails:
        if ctx.options.has_key("Copy E-Mails"):
            size = account.mailSize()
            if size > 0:
                try:
                    account.addKMailMessages(self.progresspage)
                except Exception, err:
                    self.progresspage.go(err, ctx.ERROR, size)
                else:
                    self.progresspage.go(i18n("Accounts saved."), ctx.OK, 0)

        print "E-mails: apply!"
        # News Accounts:
        size = account.accountSize(["NNTP"])
        if size > 0:
            try:
                account.setKNodeAccounts()
            except Exception, err:
                self.progresspage.go(err, ctx.ERROR, size)
            else:
                self.progresspage.go(i18n("News Accounts saved."), ctx.OK, size)

        print "News: apply!"
        # IM Accounts:
        size = account.accountSize(["Jabber", "MSN"])
        if size > 0:
            try:
                account.setKopeteAccounts()
            except Exception, err:
                self.progresspage.go(err, ctx.ERROR, size)
            else:
                self.progresspage.go(i18n("Instant Messenger Accounts saved."), ctx.OK, size)

        print "IM: apply!"
        # Links:
        if ctx.filesOptions:
            if ctx.filesOptions.has_key("links"):
                links = ctx.filesOptions["links"]
                for link in links:
                    files.createLink(link)
                    self.progresspage.go(unicode(i18n("Link '%s' created.")) % link["localname"], ctx.OK, 1000)

            print "LINKS: apply!"
            # Folders:
            if ctx.filesOptions.has_key("folders"):
                folders = ctx.filesOptions["folders"]
                for folder in folders:
                    foldername = os.path.join(ctx.filesOptions["copy destination"], folder["localname"])
                    files.copyFolder(folder, ctx.filesOptions["copy destination"], self.progresspage)

        print "Folders: apply!"
        # The end:
        if self.progresspage.progressbar2.value() == 0:
            self.progresspage.label.setText(unicode(i18n("Nothing done, because no option selected. You can close the wizard...")))
        else:
            self.progresspage.label.setText(unicode(i18n("All operations completed. You can close the wizard...")))

    def shown(self):
        self.run()

    def execute(self):
        return (True,None)
