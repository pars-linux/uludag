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

BOOT_ACCESS, BOOT_ENTRIES, BOOT_SYSTEMS = xrange(1, 4)

class widgetEntryList(QWidget):
    def __init__(self, parent, comar_link):
        QWidget.__init__(self, parent)
        self.parent = parent
        
        self.link = comar_link
        
        layout = QGridLayout(self, 1, 1, 6, 6)

        bar = QToolBar("main", None, self)
        
        but = QToolButton(getIconSet("add"), "", "main", self.slotAddEntry, bar)
        but.setTextLabel(i18n("New Entry"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        
        lab = QToolButton(bar)
        lab.setEnabled(False)
        bar.setStretchableWidget(lab)
        
        but = QToolButton(getIconSet("help"), "", "main", self.slotHelp, bar)
        but.setTextLabel(i18n("Help"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)
        layout.addWidget(bar, 0, 0)
        
        self.listEntries = EntryView(self)
        self.listEntries.setEnabled(False)
        layout.addWidget(self.listEntries, 1, 0)
        
    def init(self):
        if self.parent.can_access:
            self.listEntries.setEnabled(True)
    
    def slotAddEntry(self):
        self.parent.widgetEditEntry.newEntry()
    
    def slotHelp(self):
        pass

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
        
        self.checkDefault = QCheckBox(self)
        self.checkDefault.setText(unicode("Default boot entry"))
        layout.addMultiCellWidget(self.checkDefault, 6, 6, 0, 1)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addMultiCell(spacer, 7, 7, 0, 1)
        
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
        
        if "default" in entry:
            self.checkDefault.setChecked(True)
        
        self.slotSystem(entry["os_type"])
        self.parent.stack.raiseWidget(1)
    
    def deleteEntry(self, index):
        confirm = KMessageBox.questionYesNo(self, i18n("Are you sure you want to remove this entry?"), i18n("Delete Entry"))
        if confirm == KMessageBox.Yes:
            self.parent.widgetEntries.listEntries.setEnabled(False)
            args = {
                "index": index,
            }
            self.link.call("Boot.Loader.removeEntry", args)
    
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

        self.checkDefault.setChecked(False)
        
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
        self.parent.widgetEntries.listEntries.setEnabled(False)
        default = "no"
        if self.checkDefault.isChecked():
            default = "yes"
        args = {
            "os_type": str(self.listSystem.currentText()),
            "title": unicode(self.editTitle.text()),
            "root": str(self.editRoot.text()),
            "kernel": str(self.editKernel.text()),
            "options": unicode(self.editOptions.text()),
            "initrd": str(self.editInitrd.text()),
            "default": default,
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
        self.link.call("Boot.Loader.listSystems", id=BOOT_SYSTEMS)

    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == "notify":
            self.widgetEntries.listEntries.setEnabled(False)
            if reply.data == "entry":
                self.default = -1
                self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
                if self.widgetEditEntry.entry:
                    KMessageBox.information(self, i18n("Bootloader configuration changed by another application."), i18n("Warning"))
                    idgetEditEntry.slotExit()
        elif reply.command == "result":
            if reply.id == BOOT_ACCESS:
                self.can_access = True
                self.widgetEntries.init()
            elif reply.id == BOOT_ENTRIES:
                self.widgetEntries.listEntries.clear()
                self.entries = []
                for entry in reply.data.split("\n\n"):
                    entry = dict([x.split(" ", 1) for x in entry.split("\n")])
                    index = int(entry["index"])
                    pardus = entry["os_type"] == "linux" and getRoot() == entry["root"]
                    self.entries.append(entry)
                    item = self.widgetEntries.listEntries.add(self.widgetEditEntry, index, unicode(entry["title"]), deviceDescription(entry["root"]),  pardus, entry)
                self.widgetEntries.listEntries.setEnabled(True)
            elif reply.id == BOOT_SYSTEMS:
                self.systems = {}
                for system in reply.data.split("\n"):
                    label, fields = system.split(" ", 1)
                    self.systems[label] = fields.split(",")
        elif reply.command == "fail":
            KMessageBox.error(self, "%s failed: %s" % (reply.id, reply.data), i18n("Failed"))
