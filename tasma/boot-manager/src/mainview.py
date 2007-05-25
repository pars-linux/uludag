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

BOOT_ACCESS, BOOT_ENTRIES, BOOT_SYSTEMS, BOOT_OPTIONS, BOOT_SET_ENTRY = xrange(1, 6)

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
        but.hide()
        layout.addWidget(bar, 0, 0)
        
        self.listEntries = EntryView(self)
        self.listEntries.setEnabled(False)
        layout.addWidget(self.listEntries, 1, 0)
        
        self.checkSaved = QCheckBox(self)
        self.checkSaved.setText(i18n("Remember last booted entry."))
        layout.addWidget(self.checkSaved, 2, 0)
        
        self.connect(self.checkSaved, SIGNAL("clicked()"), self.slotCheckSaved)
        
    def init(self):
        if self.parent.can_access:
            self.listEntries.setEnabled(True)
    
    def slotCheckSaved(self):
        if self.checkSaved.isChecked():
            self.link.call("Boot.Loader.setOptions", {"default": "saved"})
        else:
            self.link.call("Boot.Loader.setOptions", {"default": "0"})
    
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
        self.saved = False
        self.fields = {}
        
        layout = QGridLayout(self, 1, 1, 11, 6)
        
        self.labelTitle = QLabel(self)
        self.labelTitle.setText(i18n("Title:"))
        self.labelTitle.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout.addWidget(self.labelTitle, 0, 0)
        
        self.editTitle = QLineEdit(self)
        self.labelTitle.setMinimumSize(90, 10)
        layout.addMultiCellWidget(self.editTitle, 0, 0, 1, 2)
        
        self.labelSystem = QLabel(self)
        self.labelSystem.setText(i18n("System:"))
        self.labelSystem.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout.addWidget(self.labelSystem, 1, 0)
        
        self.listSystem = QComboBox(self)
        layout.addWidget(self.listSystem, 1, 1)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer, 1, 2)
        
        self.labelRoot = QLabel(self)
        self.labelRoot.setText(i18n("Root:"))
        self.labelRoot.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout.addWidget(self.labelRoot, 2, 0)
        
        self.editRoot = QLineEdit(self)
        layout.addMultiCellWidget(self.editRoot, 2, 2, 1, 2)
        
        self.fields["root"] = (self.labelRoot, self.editRoot)
        
        self.labelKernel = QLabel(self)
        self.labelKernel.setText(i18n("Kernel:"))
        self.labelKernel.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout.addWidget(self.labelKernel, 3, 0)
        
        self.editKernel = QLineEdit(self)
        layout.addMultiCellWidget(self.editKernel, 3, 3, 1, 2)
        
        self.fields["kernel"] = (self.labelKernel, self.editKernel)
        
        self.labelOptions = QLabel(self)
        self.labelOptions.setText(i18n("Kernel Parameters:"))
        self.labelOptions.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout.addWidget(self.labelOptions, 4, 0)
        
        self.editOptions = QLineEdit(self)
        layout.addMultiCellWidget(self.editOptions, 4, 4, 1, 2)
        
        self.fields["options"] = (self.labelOptions, self.editOptions)
        
        self.labelInitrd = QLabel(self)
        self.labelInitrd.setText(i18n("Initial Ramdisk:"))
        self.labelInitrd.setAlignment(QLabel.AlignVCenter | QLabel.AlignRight)
        layout.addWidget(self.labelInitrd, 5, 0)
        
        self.editInitrd = QLineEdit(self)
        layout.addMultiCellWidget(self.editInitrd, 5, 5, 1, 2)
        
        self.fields["initrd"] = (self.labelInitrd, self.editInitrd)
        
        self.checkDefault = QCheckBox(self)
        self.checkDefault.setText(i18n("Set as default boot entry."))
        layout.addMultiCellWidget(self.checkDefault, 6, 6, 1, 2)
        
        spacer = QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addMultiCell(spacer, 8, 8, 0, 1)
        
        layout_buttons = QHBoxLayout(layout)
        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout_buttons.addItem(spacer)
        
        self.buttonOK = QPushButton(self)
        self.buttonOK.setText(i18n("Save"))
        layout_buttons.addWidget(self.buttonOK)
        
        self.buttonCancel = QPushButton(self)
        self.buttonCancel.setText(i18n("Cancel"))
        layout_buttons.addWidget(self.buttonCancel)
        
        layout.addMultiCell(layout_buttons, 9, 9, 1, 2)
        
        self.connect(self.listSystem, SIGNAL("activated(const QString &)"), self.slotSystem)
        self.connect(self.buttonOK, SIGNAL("clicked()"), self.slotSave)
        self.connect(self.buttonCancel, SIGNAL("clicked()"), self.slotExit)
        
        self.resetEntry()
    
    def newEntry(self):
        self.resetEntry()
        self.parent.showScreen("EditEntry")
    
    def editEntry(self, entry):
        self.resetEntry()
        self.entry = entry
        systems = self.parent.systems
        
        self.checkDefault.setChecked(False)
        
        self.editTitle.setText(unicode(entry["title"]))
        
        self.listSystem.setCurrentText(unicode(systems[entry["os_type"]][0]))
        self.slotSystem(unicode(systems[entry["os_type"]][0]))
        
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            if label in entry:
                widgetEdit.setText(unicode(entry[label]))
        
        if self.parent.widgetEntries.checkSaved.isChecked():
            self.checkDefault.hide()
        else:
            self.checkDefault.show()
        
        if "default" in entry and entry["default"] != "saved":
            self.checkDefault.setChecked(True)
        
        self.parent.showScreen("EditEntry")
    
    def deleteEntry(self, index, title):
        confirm = KMessageBox.questionYesNo(self, i18n("Are you sure you want to remove this entry?"), i18n("Delete Entry"))
        if confirm == KMessageBox.Yes:
            self.parent.widgetEntries.listEntries.setEnabled(False)
            args = {
                "index": index,
                "title": title,
            }
            self.link.call("Boot.Loader.removeEntry", args)
    
    def resetEntry(self):
        self.entry = None
        systems = self.parent.systems
        
        self.editTitle.setText("")
        
        self.listSystem.clear()
        if systems:
            keys = systems.keys()
            other = False
            if "other" in keys:
                other = True
                keys.remove("other")
            keys.sort()
            for name in keys:
                label = unicode(systems[name][0])
                self.listSystem.insertItem(label)
            if other:
                label = unicode(systems["other"][0])
                self.listSystem.insertItem(label)
            self.slotSystem("Linux")
        
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            widgetEdit.setText("")
        
        self.checkDefault.setChecked(False)
    
    def slotSystem(self, label):
        systems = self.parent.systems
        for name, (sys_label, fields) in systems.iteritems():
            if unicode(sys_label) == label:
                break
        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            if label in fields:
                widgetLabel.show()
                widgetEdit.show()
            else:
                widgetLabel.hide()
                widgetEdit.hide()
    
    def showError(self, message):
        KMessageBox.information(self, message, i18n("Error"))
    
    def slotSave(self):
        default = "no"
        if self.parent.widgetEntries.checkSaved.isChecked():
            default = "saved"
        elif self.checkDefault.isChecked():
            default = "yes"
        
        systems = self.parent.systems
        os_type = "other"
        for name, (sys_label, fields) in systems.iteritems():
            if unicode(sys_label) == unicode(self.listSystem.currentText()):
                os_type = name
                break
        
        args = {
            "os_type": os_type,
            "title": unicode(self.editTitle.text()),
            "default": default,
        }
        
        for label in self.fields:
            if label in systems[os_type][1]:
                value = unicode(self.fields[label][1].text())
                args[label] = value
        
        if self.entry:
            args["index"] = self.entry["index"]
        
        self.saved = True
        self.link.call("Boot.Loader.setEntry", args, id=BOOT_SET_ENTRY)
    
    def slotExit(self):
        self.resetEntry()
        self.parent.showScreen("Entries")

class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        self.entries = []
        self.options = {}
        self.systems = {}
        self.screens = []
        self.can_access = False
        
        layout = QGridLayout(self, 1, 1, 0, 0)
        self.stack = QWidgetStack(self)
        layout.addWidget(self.stack, 0, 0)
        
        self.widgetEntries = widgetEntryList(self, self.link)
        self.stack.addWidget(self.widgetEntries)
        self.screens.append("Entries")
        
        self.widgetEditEntry = widgetEditEntry(self, self.link)
        self.stack.addWidget(self.widgetEditEntry)
        self.screens.append("EditEntry")
        
        self.link.ask_notify("Boot.Loader.changed")
        self.link.can_access("Boot.Loader.setEntry", id=BOOT_ACCESS)
        self.link.call("Boot.Loader.getOptions", id=BOOT_OPTIONS)
        self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
        self.link.call("Boot.Loader.listSystems", id=BOOT_SYSTEMS)
    
    def showScreen(self, label):
        screen = self.screens.index(label)
        self.stack.raiseWidget(screen)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == "notify":
            self.widgetEntries.listEntries.setEnabled(False)
            if reply.data in ["entry", "option"]:
                self.link.call("Boot.Loader.listEntries", id=BOOT_ENTRIES)
                if self.widgetEditEntry.entry and not self.widgetEditEntry.saved:
                    KMessageBox.information(self, i18n("Bootloader configuration changed by another application."), i18n("Warning"))
                    self.widgetEditEntry.slotExit()
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
                    item = self.widgetEntries.listEntries.add(self.widgetEditEntry, index, unicode(entry["title"]), entry["root"],  pardus, entry)
                self.widgetEntries.listEntries.setEnabled(True)
            elif reply.id == BOOT_SYSTEMS:
                self.systems = {}
                for system in reply.data.split("\n"):
                    name, value = system.split(" ", 1)
                    label, fields = value.split(",", 1)
                    self.systems[name] = (label, fields.split(","))
            elif reply.id == BOOT_OPTIONS:
                for option in reply.data.split("\n"):
                    key, value = option.split(" ", 1)
                    self.options[key] = value
                if self.options["default"] == "saved":
                    self.widgetEntries.checkSaved.setChecked(True)
            elif reply.id == BOOT_SET_ENTRY:
                self.widgetEditEntry.saved = False
                self.widgetEntries.listEntries.setEnabled(False)
                self.widgetEditEntry.slotExit()
        elif reply.command == "fail":
            if reply.id == BOOT_SET_ENTRY:
                self.widgetEditEntry.saved = False
                KMessageBox.error(self, unicode(reply.data), i18n("Failed"))
            else:
                KMessageBox.error(self, "%s failed: %s" % (reply.id, unicode(reply.data)), i18n("Failed"))
