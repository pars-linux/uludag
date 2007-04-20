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

BOOT_NOTIFY, BOOT_ENTRIES, BOOT_OPTIONS, BOOT_ENTRY_LIST, \
BOOT_ENTRY_DIALOG, BOOT_SET_ENTRY  = xrange(1, 7)

class dialogEditEntry(QDialog):
    def __init__(self, parent, title, commands):
        QDialog.__init__(self, parent)
        
        self.title = title
        self.commands = commands
        
        layout = QGridLayout(self, 1, 1, 11, 6, "formMainLayout")
        
        self.labelTitle = QLabel(self)
        self.labelTitle.setText(i18n("<b>Title</b>"))
        self.labelTitle.setMaximumSize(QSize(100, 32767))
        layout.addWidget(self.labelTitle, 0, 0)
        
        self.editTitle = QLineEdit(self)
        self.editTitle.setText(title)
        layout.addMultiCellWidget(self.editTitle, 0, 0, 1, 4)
        
        self.buttonOK = QPushButton(self)
        self.buttonOK.setText(i18n("OK"))
        self.buttonOK.setDefault(True)
        layout.addWidget(self.buttonOK, 1, 3)
        
        self.buttonCancel = QPushButton(self)
        self.buttonCancel.setText(i18n("Cancel"))
        layout.addWidget(self.buttonCancel, 1, 4)
        
        self.connect(self.buttonOK, SIGNAL("clicked()"), self.accept)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), self.reject)
        
        self.resize(QSize(350, 100).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)
    
    def accept(self):
        if self.editTitle.isModified():
            self.title = unicode(self.editTitle.text())
            QDialog.accept(self)
        else:
            QDialog.reject(self)

class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        layout = QGridLayout(self, 1, 1, 11, 6, "formMainLayout")
        
        self.listEntries = QListBox(self)
        layout.addWidget(self.listEntries, 0, 0)
        
        self.default = -1
        
        self.link.ask_notify("Boot.Loader.changed", id=BOOT_NOTIFY)
        self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
        self.link.call("Boot.Loader.listOptions", id=BOOT_OPTIONS)
        
        self.dialogEntry = None
        
        self.connect(self.listEntries, SIGNAL("doubleClicked(QListBoxItem*)"), self.slotEditEntry)
    
    def slotEditEntry(self, item):
        if item:
            self.listEntries.setEnabled(False)
            self.link.call("Boot.Loader.getEntry", {"index": item.entry_index}, id=BOOT_ENTRY_DIALOG)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == "notify":
            self.default = -1
            self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
            self.link.call("Boot.Loader.listOptions", id=BOOT_OPTIONS)
            if self.dialogEntry:
                KMessageBox.error(self, i18n("Boot loader configuration update by another application."), i18n("Warning"))
                self.dialogEntry.reject()
        elif reply.command == "result":
            if reply.id == BOOT_ENTRIES:
                self.listEntries.clear()
                index = 0
                for entry in reply.data.split("\n"):
                    item = Entry(self.listEntries, entry, checked=index==self.default, index=index)
                    self.link.call("Boot.Loader.getEntry", {"index": index}, id=BOOT_ENTRY_LIST)
                    index += 1
            elif reply.id == BOOT_OPTIONS:
                index = 0
                for option in reply.data.split("\n"):
                    key, value = option.split()
                    if key == "default":
                        index = int(value)
                self.default = index
                item = self.listEntries.item(index)
                if item:
                    item.checked = True
                    self.listEntries.updateItem(index)
            elif reply.id == BOOT_ENTRY_LIST:
                index, title, commands = parseGrubCommand(reply.data)
                if "root"in commands:
                    root = commands["root"][1]
                elif "rootnoverify"in commands:
                    root = commands["rootnoverify"][1]
                if "kernel" in commands:
                    value = commands["kernel"][1]
                    if value.startswith("("):
                        root = value.split(")")[0] + ")"
                    if "root" in value:
                        os_type = "Linux"
                elif "makeactive" in commands:
                    os_type = "Windows"
                else:
                    os_type = "Unknown"
                if os_type == "Linux" and root == grubDevice(getRoot()):
                    os_type = "Pardus"
                item = self.listEntries.item(index)
                item.description = grubDeviceName(root)
                item.setOs(os_type)
                self.listEntries.updateItem(index)
            elif reply.id == BOOT_ENTRY_DIALOG:
                index, title, commands = parseGrubCommand(reply.data)
                self.dialogEntry = dialogEditEntry(self, title, commands)
                if self.dialogEntry.exec_loop():
                    title = dialog.title
                    commands = formatGrubCommand(dialog.commands)
                    self.link.call("Boot.Loader.updateEntry", {"index": index, "title": title, "commands": commands}, id=BOOT_SET_ENTRY)
                else:
                    self.dialogEntry = None
                    self.listEntries.setEnabled(True)
            elif reply.id == BOOT_SET_ENTRY:
                self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
                self.listEntries.setEnabled(True)
        elif reply.command == "fail":
            KMessageBox.error(self, "%s failed: %s" % (reply.id, reply.data), i18n("Failed"))
            self.listEntries.setEnabled(True)
