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

from migration.gui.ScreenWidget import ScreenWidget
import migration.gui.context as ctx

class Widget(QtGui.QWidget, ScreenWidget):
    title = i18n("Selecting Options")
    desc = i18n("Welcome to Migration Tool Wizard :)")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.sources = ctx.sources
        print "ctx.sources:%s" % ctx.sources
        #self.creator(self.sources)

    def creator(self, sources):
        self.vbox = QtGui.QVBoxLayout()
        
        # Wallpaper:
        if sources.has_key("Wallpaper Path"):
            self.wallpaperGroup = QtGui.QButtonGroup(self, "wpGroup")
            self.wallpaperLayout = QtGui.QHBoxLayout()
            self.vbox.addWidget(self.wallpaperGroup)
            # New (current) Wallpaper:
            self.newLayout = QtGui.QVBoxLayout(None)
            self.newLayout.setAlignment(Qt.AlignCenter)
            self.wallpaperLayout.addLayout(self.newLayout)
            # Thumbnail:
            self.newThumb = QtGui.QLabel(self.wpGroup, "newThumb")
            self.newLayout.addWidget(self.newThumb)
            if destinations.has_key("Wallpaper Path"):
                newwp = QtGui.QImage(unicode(destinations["Wallpaper Path"]))
                newwp = newwp.smoothScale(100, 100, QImage.ScaleMax)
                pixmap = QtGui.QPixmap(newwp)
                self.newThumb.setPixmap(pixmap)
            # Radio Button:
            self.newRadio = QtGui.QRadioButton(self.wpGroup, "newRadio")
            if destinations.has_key("Wallpaper Path"):
                self.newRadio.setText(i18n("Keep current wallpaper"))
            else:
                self.newRadio.setText(i18n("Don't use wallpaper"))
            QtGui.QToolTip.add(self.newRadio, i18n("Does not change your wallpaper."))
            self.newRadio.setChecked(True)
            self.newLayout.addWidget(self.newRadio)
            # Old Wallpaper:
            self.oldLayout = QtGui.QVBoxLayout(None)
            self.oldLayout.setAlignment(Qt.AlignCenter)
            self.wpLayout.addLayout(self.oldLayout)
            # Thumbnail:
            self.oldThumb = QtGui.QLabel(self.wpGroup, "oldThumb")
            oldwp = QtGui.QImage(unicode(sources["Wallpaper Path"]))
            oldwp = oldwp.smoothScale(100, 100, QImage.ScaleMax)
            pixmap = QtGui.QPixmap(oldwp)
            self.oldThumb.setPixmap(pixmap)
            self.oldLayout.addWidget(self.oldThumb)
            # Radio Button:
            self.oldRadio = QtGui.QRadioButton(self.wpGroup, "oldRadio")
            self.oldRadio.setText(i18n("Use my old wallpaper"))
            QtGui.QToolTip.add(self.oldRadio, i18n("Copies your old wallpaper to Pardus and sets it as new background image."))
            self.oldLayout.addWidget(self.oldRadio)
        
         # Bookmarks:
        if sources.has_key("Firefox Profile Path") or sources.has_key("Favorites Path"):
            self.bookmarks = QtGui.QGroupBox(self, "Bookmarks")
            self.bookmarks.setTitle(i18n("Bookmarks"))
            self.bookmarks.setAlignment(Qt.AlignLeft)
            self.bookmarksLayout = QtGui.QVBoxLayout(self.bookmarks.layout())
            self.vbox.addWidget(self.bookmarks)
            
            # FF Bookmarks:
            if sources.has_key("Firefox Profile Path"):
                self.fireFoxBookmarks = QtGui.QCheckBox(self.bookmarks, "fireFoxBookmarks")
                self.fireFoxBookmarks.setText(i18n("Firefox Bookmarks"))
                self.fireFoxBookmarks.setChecked(True)
                QtGui.QToolTip.add(self.fireFoxBookmarks, i18n("Copies your old Firefox bookmarks to Firefox under Pardus."))
                self.bookmarksLayout.addWidget(self.fireFoxBookmarks)
            
            # Opera Bookmarks:
            if sources.has_key("Opera Profile Path"):
                self.operaBookmarks = QCheckBox(self.bookmarks, "operaBookmarks")
                self.operaBookmarks.setText(i18n("Opera Bookmarks"))
                self.operaBookmarks.setChecked(True)
                QtGui.QToolTip.add(self.operaBookmarks, i18n("Copies your old Opera bookmarks to Firefox under Pardus."))
                self.bookmarksLayout.addWidget(self.operaBookmarks)
            
            # IE Bookmarks:
            if sources.has_key("Favorites Path"):
                self.IEBookmarks = QtGui.QCheckBox(self.Bookmarks, "IEBookmarks")
                self.IEBookmarks.setText(i18n("Internet Explorer favorites"))
                self.IEBookmarks.setChecked(True)
                QtGui.QToolTip.add(self.IEBookmarks, i18n("Copies your old Internet Explorer favorites to Firefox under Pardus."))
                self.bookmarksLayout.addWidget(self.IEBookmarks)
                
         # Mail Accounts:
        if sources.has_key("Windows Mail Path") or sources.has_key("Thunderbird Profile Path"):
            self.mailAccounts = QtGui.QGroupBox(self, "MailAccounts")
            self.mailAccounts.setTitle(i18n("E-Mail and News Accounts"))
            self.mailAccounts.setAlignment(Qt.AlignLeft)
            self.mailAccountsLayout = QtGui.QVBoxLayout(self.mailAccounts.layout())
            self.vbox.addWidget(self.mailAccounts)
            
            # Windows Mail Accounts:
            if sources.has_key("Windows Mail Path"):
                self.winMail = QtGui.QCheckBox(self.mailAccounts, "WinMail")
                self.winMail.setText(i18n("Windows Mail accounts"))
                self.winMail.setChecked(True)
                QtGui.QToolTip.add(self.winMail, i18n("Copies your old mail and newsgroup accounts to KMail and KNode applications."))
                self.mailAccountsLayout.addWidget(self.winMail)
            
            # Thunderbird Accounts:
            if sources.has_key("Thunderbird Profile Path"):
                self.TB = QtGui.QCheckBox(self.MailAccounts, "TB")
                self.TB.setText(i18n("Thunderbird accounts"))
                self.TB.setChecked(True)
                QToolTip.add(self.TB, i18n("Copies your old mail and newsgroup accounts to KMail and KNode applications."))
                self.MailAccountsLayout.addWidget(self.TB)
            
            # E-Mails:
            self.mail = QtGui.QCheckBox(self.mailAccounts, "mail")
            self.mail.setText(i18n("Copy e-mail messages from e-mail accounts"))
            self.mail.setChecked(True)
            QtGui.QToolTip.add(self.mail, i18n("Copies your e-mail messages to KMail from selected applications above."))
            self.mailAccountsLayout.addWidget(self.mail)
                
        # IM Accounts:
        if sources.has_key("Contacts Path") or sources.has_key("GTalk Key"):
            self.IMAccounts = QtGui.QGroupBox(self, "IMAccounts")
            self.IMAccounts.setTitle(i18n("Instant Messenger Accounts"))
            self.IMAccounts.self.IMAccounts.layout()
            self.IMAccountsLayout = QVBoxLayout(self)
            self.vbox.addWidget(self.IMAccounts)
            # MSN Accounts:
            if sources.has_key("Contacts Path"):
                self.MSN = QtGui.QCheckBox(self.IMAccounts, "MSN")
                self.MSN.setText(i18n("MSN accounts"))
                self.MSN.setChecked(True)
                QtGui.QToolTip.add(self.MSN, i18n("Copies your MSN Messenger accounts to Kopete."))
                self.IMAccountsLayout.addWidget(self.MSN)
            # GTalk Accounts:
            if sources.has_key("GTalk Key"):
                self.GTalk = QtGui.QCheckBox(self.IMAccounts, "GTalk")
                self.GTalk.setText(i18n("GTalk accounts"))
                self.GTalk.setChecked(True)
                QtGui.QToolTip.add(self.GTalk, i18n("Copies your GTalk accounts to Kopete."))
                self.IMAccountsLayout.addWidget(self.GTalk)
        # Spacer:
        spacer = QtGui.QSpacerItem(1,1,QSizePolicy.Minimum,QSizePolicy.Expanding)
        self.vbox.addItem(spacer)
        
    def getOptions(self):
        "Returns a dictionary consists of selected options"
        options = {}
        self.sources["Copy E-Mails"] = True
        # Add fundamental items:
        for item in ["Partition", "OS Type", "User Name", "Home Path"]:
            options[item] = self.sources[item]
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
            item = self.child(widgetname)
            if item and item.isChecked():
                options[dictname] = self.sources[dictname]
        return options

    def shown(self):
        pass

    def execute(self):
        ctx.options = self.getOptions()