#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

from utility import *
from ui_elements import *

import comar

BOOT_NOTIFY, BOOT_ENTRIES, BOOT_OPTIONS = xrange(1, 4)

class widgetEntryList(QWidget):
    def __init__(self, parent, comar_link):
        QWidget.__init__(self, parent)
        self.parent = parent
        
        self.link = comar_link
        
        layout = QGridLayout(self, 1, 1, 11, 6)
        
        self.listEntries = QListBox(self)
        layout.addWidget(self.listEntries, 0, 0)
        
        self.iconBox = IconBox(self)
        
        self.pushAdd = IconButton(self.iconBox, i18n("Add"), "edit_add")
        self.iconBox.addWidget(self.pushAdd)
        
        self.pushEdit = IconButton(self.iconBox, i18n("Edit"), "edit")
        self.pushEdit.setEnabled(False)
        self.iconBox.addWidget(self.pushEdit)
        
        self.pushDelete = IconButton(self.iconBox, i18n("Delete"), "editdelete")
        self.pushDelete.setEnabled(False)
        self.iconBox.addWidget(self.pushDelete)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.iconBox.addWidget(spacer)
        layout.addWidget(self.iconBox, 1, 0)
        
        self.connect(self.listEntries, SIGNAL("doubleClicked(QListBoxItem*)"), self.slotEditEntry)
        self.connect(self.listEntries, SIGNAL("selectionChanged(QListBoxItem*)"), self.slotClickEntry)
        self.connect(self.pushEdit, SIGNAL("clicked()"), self.slotEditEntry)
    
    def slotClickEntry(self, item=None):
        if item:
            self.pushEdit.setEnabled(True)
            self.pushDelete.setEnabled(True)
        else:
            self.pushEdit.setEnabled(False)
            self.pushDelete.setEnabled(False)
    
    def slotEditEntry(self):
        item = self.listEntries.selectedItem()
        if item:
            entry = self.parent.entries[item.entry_index]
            self.parent.widgetEditEntry.editEntry(*entry)


class widgetEditEntry(QWidget):
    def __init__(self, parent, comar_link):
        QWidget.__init__(self, parent)
        self.parent = parent
        
        self.link = comar_link
        
        layout = QGridLayout(self, 1, 1, 11, 6)
        
        self.pushExit = QPushButton(self)
        self.pushExit.setText(i18n("Exit"))
        layout.addWidget(self.pushExit, 0, 0)
        
        self.connect(self.pushExit, SIGNAL("clicked()"), self.slotExit)
        
        self.resetEntry()
    
    def editEntry(self, index, title, commands):
        self.index = index
        self.title = title
        self.commands = commands
        self.pushExit.setText("Editing '%s' (%s). Click to exit." % (title, index))
        self.parent.stack.raiseWidget(1)
    
    def updateEntryIndex(self, index=None):
        if self.parent.stack.visibleWidget() != self:
            return
        if index:
            self.index = index
            self.pushExit.setText("Editing '%s' (%s). Click to exit." % (self.title, index))
        else:
            # Entry removed by another application
            KMessageBox.error(self, i18n("Entry removed! Closing edit dialog."), i18n("Failed"))
            self.slotExit()
    
    def resetEntry(self):
        self.index = None
        self.title = None
        self.commands = None
    
    def slotExit(self):
        self.resetEntry()
        self.parent.stack.raiseWidget(0)

class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        layout = QGridLayout(self, 1, 1, 0, 0, "formMainLayout")
        self.stack = QWidgetStack(self)
        layout.addWidget(self.stack, 0, 0)
        
        self.widgetEntries = widgetEntryList(self, self.link)
        self.stack.addWidget(self.widgetEntries)
        
        self.widgetEditEntry = widgetEditEntry(self, self.link)
        self.stack.addWidget(self.widgetEditEntry)
        
        self.default = -1
        self.entries = []
        
        self.link.ask_notify("Boot.Loader.changed", id=BOOT_NOTIFY)
        self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
        self.link.call("Boot.Loader.listOptions", id=BOOT_OPTIONS)

    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == "notify":
            self.default = -1
            self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
            self.link.call("Boot.Loader.listOptions", id=BOOT_OPTIONS)
        elif reply.command == "result":
            if reply.id == BOOT_ENTRIES:
                self.widgetEntries.listEntries.clear()
                self.widgetEntries.slotClickEntry()
                self.entries = []
                for entry in reply.data.split("\n\n\n"):
                    index, title, commands = parseGrubCommand(entry)
                    root, os_type = getEntryDetails(commands)
                    self.entries.append([index, title, commands])
                    item = Entry(self.widgetEntries.listEntries, title, grubDeviceName(root), os_type, index==self.default, index)
                if self.widgetEditEntry.index:
                    # Edit dialog is in use, lookup entry in list and get (new) index of entry.
                    for index, title, commands in self.entries:
                        if title == self.widgetEditEntry.title and commands == self.widgetEditEntry.commands:
                            self.widgetEditEntry.updateEntryIndex(index)
                            return
                    # If entry isn't in the list, it's removed or updated by another application.
                    self.widgetEditEntry.updateEntryIndex(None)
            elif reply.id == BOOT_OPTIONS:
                index = 0
                for option in reply.data.split("\n"):
                    key, value = option.split()
                    if key == "default":
                        index = int(value)
                self.default = index
                #item = self.listEntries.item(index)
                #if item:
                #    item.checked = True
                #    self.listEntries.updateItem(index)
        elif reply.command == "fail":
            KMessageBox.error(self, "%s failed: %s" % (reply.id, reply.data), i18n("Failed"))
