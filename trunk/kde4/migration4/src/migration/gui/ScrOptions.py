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

from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import i18n
from PyKDE4.kdeui import KMessageBox

from migration.gui.ScreenWidget import ScreenWidget
import migration.gui.context as ctx

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Selecting Options")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        #self.ui  =  Ui_optionWidget()
        #self.ui.setupUi(self)
        self.box = QtGui.QGridLayout(self)
        #self.gridlayout.setContentsMargins(1,-1,11,-1)
        #self.sources = ctx.sources
        #self.vbox = QtGui.QVBoxLayout(self)

    def creator(self, sources):

        # Wallpaper:
        if sources.has_key("Wallpaper Path"):
            print "Wallpaper Path"
            self.wallpaperGroup = QtGui.QButtonGroup(self)
            self.wallpaperLayout = QtGui.QHBoxLayout(self.wallpaperGroup)
            self.box.addWidget(self.wallpaperGroup)

            # New (current) Wallpaper:
            self.newLayout = QtGui.QVBoxLayout(None)
            #self.newLayout.setAlignment(Qt.AlignCenter)
            self.wallpaperLayout.addLayout(self.newLayout)

            # Thumbnail:
            self.newThumb = QtGui.QLabel(self.wallpaperGroup)
            self.newLayout.addWidget(self.newThumb)
            if destinations.has_key("Wallpaper Path"):
                newwp = QtGui.QImage(unicode(destinations["Wallpaper Path"]))
                newwp = newwp.smoothScale(100, 100, QImage.ScaleMax)
                pixmap = QtGui.QPixmap(newwp)
                self.newThumb.setPixmap(pixmap)

            # Radio Button:
            self.newRadio = QtGui.QRadioButton(self.wallpaperGroup)
            if destinations.has_key("Wallpaper Path"):
                self.newRadio.setText(i18n("Keep current wallpaper"))
            else:
                self.newRadio.setText(i18n("Don't use wallpaper"))
            self.newRadio.setToolTip(i18n("Does not change your wallpaper."))
            self.newRadio.setChecked(True)
            self.newLayout.addWidget(self.newRadio)

            # Old Wallpaper:
            self.oldLayout = QtGui.QVBoxLayout(None)
            #self.oldLayout.setAlignment(Qt.AlignCenter)
            self.wallpaperLayout.addLayout(self.oldLayout)

            # Thumbnail:
            self.oldThumb = QtGui.QLabel(self.wallpaperGroup)
            oldwp = QtGui.QImage(unicode(sources["Wallpaper Path"]))
            oldwp = oldwp.smoothScale(100, 100, QImage.ScaleMax)
            pixmap = QtGui.QPixmap(oldwp)
            self.oldThumb.setPixmap(pixmap)
            self.oldLayout.addWidget(self.oldThumb)

            # Radio Button:
            self.oldRadio = QtGui.QRadioButton(self.wallpaperGroup)
            self.oldRadio.setObjectName("oldRadio")
            self.oldRadio.setText(i18n("Use my old wallpaper"))
            self.oldRadio.setToolTip(i18n("Copies your old wallpaper to Pardus and sets it as new background image."))
            self.oldLayout.addWidget(self.oldRadio)

        # Bookmarks:
        if sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            print "Firefox Profile Path"

            self.bookmarks = QtGui.QGroupBox("Bookmarks", self)
            self.bookmarks.setTitle(i18n("Bookmarks"))
            self.bookmarks.setAlignment(Qt.AlignLeft)
            self.bookmarksLayout = QtGui.QVBoxLayout(self.bookmarks)
            self.box.addWidget(self.bookmarks)
            self.box.addWidget(self.bookmarks)

            # FF Bookmarks:
            if sources.has_key("Firefox Profile Path"):
                print "Firefox Profile Path"

                self.fireFoxBookmarks = QtGui.QCheckBox(self.bookmarks)
                self.fireFoxBookmarks.setObjectName("FFBookmarks")
                self.fireFoxBookmarks.setText(i18n("Firefox Bookmarks"))
                self.fireFoxBookmarks.setChecked(True)
                self.fireFoxBookmarks.setToolTip(i18n("Copies your old Firefox bookmarks to Firefox under Pardus."))
                self.bookmarksLayout.addWidget(self.fireFoxBookmarks)

            # Opera Bookmarks:
            if sources.has_key("Opera Profile Path"):
                print "Opera Profile Path"

                self.operaBookmarks = QCheckBox(self.bookmarks)
                self.operaBookmarks.setObjectName("OperaBookmarks")
                self.operaBookmarks.setText(i18n("Opera Bookmarks"))
                self.operaBookmarks.setChecked(True)
                self.operaBookmarks.setToolTip(i18n("Copies your old Opera bookmarks to Firefox under Pardus."))
                self.bookmarksLayout.addWidget(self.operaBookmarks)

            # IE Bookmarks:
            if sources.has_key("Favorites Path"):
                print "Internet Explorer favorites"

                self.IEBookmarks = QtGui.QCheckBox(self.bookmarks)
                self.IEBookmarks.setObjectName("IEBookmarks")
                self.IEBookmarks.setText(i18n("Internet Explorer favorites"))
                self.IEBookmarks.setChecked(True)
                self.IEBookmarks.setToolTip(i18n("Copies your old Internet Explorer favorites to Firefox under Pardus."))
                self.bookmarksLayout.addWidget(self.IEBookmarks)


        # Mail Accounts:
        if sources.has_key("Windows Mail Path") or sources.has_key("Thunderbird Profile Path"):
            print "Mail Accounts"

            self.mailAccounts = QtGui.QGroupBox("MailAccounts", self)
            self.mailAccounts.setTitle(i18n("E-Mail and News Accounts"))
            self.mailAccounts.setAlignment(Qt.AlignLeft)
            self.mailAccountsLayout = QtGui.QVBoxLayout(self.mailAccounts)
            self.box.addWidget(self.mailAccounts)

            # Windows Mail Accounts:
            if sources.has_key("Windows Mail Path"):
                print "Windows Mail Path"

                self.winMail = QtGui.QCheckBox(self.mailAccounts)
                self.winMail.setObjectName("WinMail")
                self.winMail.setText(i18n("Windows Mail accounts"))
                self.winMail.setChecked(True)
                self.winMail.setToolTip(i18n("Copies your old mail and newsgroup accounts to KMail and KNode applications."))
                self.mailAccountsLayout.addWidget(self.winMail)

            # Thunderbird Accounts:
            if sources.has_key("Thunderbird Profile Path"):
                print "Thunderbird Profile Path"

                self.TB = QtGui.QCheckBox(self.mailAccounts)
                self.TB.setObjectName("TB")
                self.TB.setText(i18n("Thunderbird accounts"))
                self.TB.setChecked(True)
                self.TB.setToolTip(i18n("Copies your old mail and newsgroup accounts to KMail and KNode applications."))
                self.mailAccountsLayout.addWidget(self.TB)

            # E-Mails:
            self.mail = QtGui.QCheckBox(self.mailAccounts)
            self.mail.setObjectName("mail")
            self.mail.setText(i18n("Copy e-mail messages from e-mail accounts"))
            self.mail.setChecked(True)
            self.mail.setToolTip(i18n("Copies your e-mail messages to KMail from selected applications above."))
            self.mailAccountsLayout.addWidget(self.mail)


        # IM Accounts:
        if sources.has_key("Contacts Path") or sources.has_key("GTalk Key"):
            print "IMAccounts"

            self.IMAccounts = QtGui.QGroupBox("IMAccounts", self)
            self.IMAccounts.setTitle(i18n("Instant Messenger Accounts"))
            self.IMAccounts.self.IMAccounts.layout()
            self.IMAccountsLayout = QVBoxLayout(self.IMAccounts)
            self.vbox.addWidget(self.IMAccounts)

            # MSN Accounts:
            if sources.has_key("Contacts Path"):
                print "MSN Accounts"

                self.MSN = QtGui.QCheckBox(self.IMAccounts)
                self.MSN.setObjectName("MSN")
                self.MSN.setText(i18n("MSN accounts"))
                self.MSN.setChecked(True)
                self.MSN.setToolTip(i18n("Copies your MSN Messenger accounts to Kopete."))
                self.IMAccountsLayout.addWidget(self.MSN)

            # GTalk Accounts:
            if sources.has_key("GTalk Key"):
                print "GTalk"

                self.GTalk = QtGui.QCheckBox(self.IMAccounts)
                self.GTalk.setObjectName("GTalk")
                self.GTalk.setText(i18n("GTalk accounts"))
                self.GTalk.setChecked(True)
                self.GTalk.setToolTip(i18n("Copies your GTalk accounts to Kopete."))
                self.IMAccountsLayout.addWidget(self.GTalk)

            self.IMAccounts.addLayout(self.IMAccountsLayout)

        # Spacer:
        spacer = QtGui.QSpacerItem(1,1, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.box.addItem(spacer)

    def getOptions(self):
        "Returns a dictionary consists of selected options"
        options = {}
        ctx.sources["Copy E-Mails"] = True
        # Add fundamental items:
        for item in ["Partition", "OS Type", "User Name", "Home Path"]:
            options[item] = ctx.sources[item]
        # Add selected optional items:
        items = [("IEBookmarks", "Favorites Path"),
                 ("FFBookmarks", "Firefox Profile Path"),
                 ("OperaBookmarks", "Opera Profile Path"),
                 ("oldRadio", "Wallpaper Path"),
                 ("WinMail", "Windows Mail Path"),
                 ("TB", "Thunderbird Profile Path"),
                 ("mail", "Copy E-Mails"),
                 ("GTalk", "GTalk Key"),
                 ("MSN", "Contacts Path")]
        for widgetname, dictname in items:
            item = self.findChild(QtGui.QWidget, widgetname)
            if item and item.isChecked():
                options[dictname] = ctx.sources[dictname]
        return options

    def shown(self):
        print "ScrOptions.shown() çağrldı..."
        print "ctx.sources:%s" % ctx.sources
        if ctx.sources:
            self.creator(ctx.sources)

    def execute(self):
        if self.getOptions():
            ctx.options = self.getOptions()
            return (True, None)
