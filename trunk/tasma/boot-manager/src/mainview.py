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

BOOT_ACCESS, BOOT_ENTRIES, BOOT_OPTIONS, BOOT_SYSTEMS, BOOT_OPTION_VALUES = xrange(1, 6)

class widgetEntryList(QWidget):
    def __init__(self, parent, comar_link):
        QWidget.__init__(self, parent)
        self.parent = parent
        
        self.link = comar_link
        
        layout = QGridLayout(self, 1, 1, 11, 6)
        
        self.listEntries = QListBox(self)
        self.listEntries.setEnabled(False)
        layout.addWidget(self.listEntries, 0, 0)
        
        self.iconBox = IconBox(self)
        
        self.pushAdd = IconButton(self.iconBox, i18n("Add"), "edit_add")
        QToolTip.add(self.pushAdd, i18n("Add new entry"))
        self.pushAdd.setEnabled(False)
        self.iconBox.addWidget(self.pushAdd)
        
        self.pushEdit = IconButton(self.iconBox, i18n("Edit"), "edit")
        QToolTip.add(self.pushEdit, i18n("Edit entry"))
        self.pushEdit.setEnabled(False)
        self.iconBox.addWidget(self.pushEdit)
        
        self.pushDelete = IconButton(self.iconBox, i18n("Delete"), "editdelete")
        QToolTip.add(self.pushDelete, i18n("Delete entry"))
        self.pushDelete.setEnabled(False)
        self.iconBox.addWidget(self.pushDelete)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.iconBox.addWidget(spacer)
        layout.addWidget(self.iconBox, 1, 0)
        
        self.connect(self.listEntries, SIGNAL("doubleClicked(QListBoxItem*)"), self.slotEditEntry)
        self.connect(self.listEntries, SIGNAL("selectionChanged(QListBoxItem*)"), self.slotClickEntry)
        self.connect(self.pushAdd, SIGNAL("clicked()"), self.slotAddEntry)
        self.connect(self.pushEdit, SIGNAL("clicked()"), self.slotEditEntry)
        self.connect(self.pushDelete, SIGNAL("clicked()"), self.slotDeleteEntry)
    
    def init(self):
        if self.parent.can_access:
            self.listEntries.setEnabled(True)
            self.pushAdd.setEnabled(True)
    
    def slotClickEntry(self, item=None):
        if item and self.parent.can_access:
            self.pushEdit.setEnabled(True)
            self.pushDelete.setEnabled(True)
        else:
            self.pushEdit.setEnabled(False)
            self.pushDelete.setEnabled(False)
    
    def slotAddEntry(self):
        self.parent.widgetEditEntry.newEntry()
    
    def slotEditEntry(self):
        if not self.parent.can_access:
            return
        item = self.listEntries.selectedItem()
        if item:
            entry = self.parent.entries[item.entry_index]
            self.parent.widgetEditEntry.editEntry(entry)
    
    def slotDeleteEntry(self):
        item = self.listEntries.selectedItem()
        if item:
            confirm = KMessageBox.questionYesNo(self, i18n("Are you sure you want to remove this entry?"), i18n("Delete Entry"))
            if confirm == KMessageBox.Yes:
                args = {
                    "index": item.entry_index,
                }
                self.link.call("Boot.Loader.removeEntry", args)


class widgetEditEntry(QWidget):
    def __init__(self, parent, comar_link):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.systems = self.parent.systems
        
        self.link = comar_link
        self.fields = {}
        
        layout = QGridLayout(self, 1, 1, 11, 6)
        
        self.labelTitle = QLabel(self)
        self.labelTitle.setText(i18n("Title"))
        layout.addWidget(self.labelTitle, 0, 0)
        
        self.editTitle = QLineEdit(self)
        layout.addMultiCellWidget(self.editTitle, 0, 0, 1, 2)
        
        self.labelSystem = QLabel(self)
        self.labelSystem.setText(i18n("System"))
        layout.addWidget(self.labelSystem, 1, 0)
        
        self.listSystem = QComboBox(self)
        layout.addWidget(self.listSystem, 1, 1)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer, 1, 2)
        
        self.labelRoot = QLabel(self)
        self.labelRoot.setText(i18n("Root"))
        layout.addWidget(self.labelRoot, 2, 0)
        
        self.editRoot = QLineEdit(self)
        layout.addMultiCellWidget(self.editRoot, 2, 2, 1, 2)
        
        self.fields["root"] = (self.labelRoot, self.editRoot)
        
        self.labelKernel = QLabel(self)
        self.labelKernel.setText(i18n("Kernel"))
        layout.addWidget(self.labelKernel, 3, 0)
        
        self.editKernel = QLineEdit(self)
        layout.addMultiCellWidget(self.editKernel, 3, 3, 1, 2)
        
        self.fields["kernel"] = (self.labelKernel, self.editKernel)
        
        self.labelOptions = QLabel(self)
        self.labelOptions.setText(i18n("Kernel Options"))
        layout.addWidget(self.labelOptions, 4, 0)
        
        self.editOptions = QLineEdit(self)
        layout.addMultiCellWidget(self.editOptions, 4, 4, 1, 2)
        
        self.fields["options"] = (self.labelOptions, self.editOptions)
        
        self.labelInitrd = QLabel(self)
        self.labelInitrd.setText(i18n("Init Ramdrive"))
        layout.addWidget(self.labelInitrd, 5, 0)
        
        self.editInitrd = QLineEdit(self)
        layout.addMultiCellWidget(self.editInitrd, 5, 5, 1, 2)
        
        self.fields["initrd"] = (self.labelInitrd, self.editInitrd)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addMultiCell(spacer, 6, 6, 0, 1)
        
        self.buttonOK = QPushButton(self)
        self.buttonOK.setText(i18n("Save"))
        layout.addWidget(self.buttonOK, 7, 0)
        
        self.buttonCancel = QPushButton(self)
        self.buttonCancel.setText(i18n("Cancel"))
        layout.addWidget(self.buttonCancel, 7, 1)
        
        self.connect(self.listSystem, SIGNAL("activated(const QString &)"), self.slotSystem)
        self.connect(self.buttonOK, SIGNAL("clicked()"), self.slotSave)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), self.slotExit)
        
        self.resetEntry()
    
    def newEntry(self):
        self.resetEntry()
    
    def editEntry(self, entry):
        self.resetEntry()
        self.entry = entry
        
        self.editTitle.setText(unicode(entry["title"]))
        self.listSystem.setCurrentText(entry["os_type"])
        
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            if label in entry:
                widgetEdit.setText(unicode(entry[label]))
        
        self.slotSystem(entry["os_type"])
        self.parent.stack.raiseWidget(1)
    
    def resetEntry(self):
        self.entry = None
        systems = self.parent.systems.keys()
        systems.sort()
        
        self.editTitle.setText("")
        
        self.listSystem.clear()
        if systems:
            for system in systems:
                self.listSystem.insertItem(system)
            self.slotSystem(systems[0])
        
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            widgetEdit.setText("")
        
        self.parent.stack.raiseWidget(1)
    
    def slotSystem(self, name):
        systems = self.parent.systems
        fields = systems[str(name)]
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            if label in fields:
                widgetLabel.show()
                widgetEdit.show()
            else:
                widgetLabel.hide()
                widgetEdit.hide()
    
    def slotSave(self):
        args = {
            "os_type": str(self.listSystem.currentText()),
            "title": unicode(self.editTitle.text()),
            "root": str(self.editRoot.text()),
            "kernel": str(self.editKernel.text()),
            "options": unicode(self.editOptions.text()),
            "initrd": str(self.editInitrd.text()),
        }
        if self.entry:
            method = "Boot.Loader.updateEntry"
            args["index"] = self.entry["index"]
        else:
            method = "Boot.Loader.addEntry"
        self.link.call(method, args)
        self.slotExit()
    
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
        
        self.default = -1
        self.entries = []
        self.options = {}
        self.systems = {}
        self.can_access = False
        
        layout = QGridLayout(self, 1, 1, 0, 0)
        self.stack = QWidgetStack(self)
        layout.addWidget(self.stack, 0, 0)
        
        self.widgetEntries = widgetEntryList(self, self.link)
        self.stack.addWidget(self.widgetEntries)
        
        self.widgetEditEntry = widgetEditEntry(self, self.link)
        self.stack.addWidget(self.widgetEditEntry)
        
        self.link.ask_notify("Boot.Loader.changed")
        self.link.can_access("Boot.Loader.updateEntry", id=BOOT_ACCESS)
        self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
        self.link.call("Boot.Loader.listOptions", id=BOOT_OPTIONS)
        self.link.call("Boot.Loader.listSystems", id=BOOT_SYSTEMS)

    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == "notify":
            self.widgetEntries.listEntries.setEnabled(False)
            self.widgetEntries.slotClickEntry()
            if reply.data == "entry":
                self.default = -1
                self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
                self.link.call("Boot.Loader.listOptions", id=BOOT_OPTIONS)
                if self.widgetEditEntry.entry:
                    KMessageBox.information(self, i18n("Bootloader configuration changed by another application."), i18n("Warning"))
                    self.widgetEditEntry.slotExit()
        elif reply.command == "result":
            if reply.id == BOOT_ACCESS:
                self.can_access = True
                self.widgetEntries.init()
            elif reply.id == BOOT_ENTRIES:
                self.widgetEntries.listEntries.clear()
                self.widgetEntries.slotClickEntry()
                self.entries = []
                for entry in reply.data.split("\n\n"):
                    entry = dict([x.split(" ", 1) for x in entry.split("\n")])
                    index = int(entry["index"])
                    pardus = entry["os_type"] == "linux" and getRoot() == entry["root"]
                    self.entries.append(entry)
                    item = Entry(self.widgetEntries.listEntries, unicode(entry["title"]), deviceDescription(entry["root"]), entry["os_type"], pardus, index==self.default, index)
                self.widgetEntries.listEntries.setEnabled(True)
            elif reply.id == BOOT_SYSTEMS:
                self.systems = {}
                for system in reply.data.split("\n"):
                    label, fields = system.split(" ", 1)
                    self.systems[label] = fields.split(",")
            elif reply.id == BOOT_OPTIONS:
                for option in reply.data.split("\n"):
                    self.link.call("Boot.Loader.getOption", {"key": option}, id=BOOT_OPTION_VALUES)
            elif reply.id == BOOT_OPTION_VALUES:
                key, value = reply.data.split(" ", 1)
                if key == "default":
                    self.default = int(value)
                #item = self.listEntries.item(index)
                #if item:
                #    item.checked = True
                #    self.listEntries.updateItem(index)
        elif reply.command == "fail":
            KMessageBox.error(self, "%s failed: %s" % (reply.id, reply.data), i18n("Failed"))
