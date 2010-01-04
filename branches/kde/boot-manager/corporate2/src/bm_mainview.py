#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009, TUBITAK/UEKAE
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

import dbus
import time
from handler import CallHandler

BOOT_ACCESS, BOOT_ENTRIES, BOOT_SYSTEMS, BOOT_OPTIONS, BOOT_SET_ENTRY, \
BOOT_SET_TIMEOUT, BOOT_UNUSED, BOOT_REMOVE_UNUSED, BOOT_REMOVE_UNUSED_LAST = xrange(1, 10)

class widgetEntryList(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent

        layout = QGridLayout(self, 1, 1, 6, 6)

        bar = QToolBar("main", None, self)

        but = QToolButton(getIconSet("add"), "", "main", self.slotAddEntry, bar)
        but.setTextLabel(i18n("New Entry"), False)
        but.setUsesTextLabel(True)
        but.setTextPosition(but.BesideIcon)

        but = QToolButton(getIconSet("file_broken"), "", "main", self.slotUnused, bar)
        but.setTextLabel(i18n("Unused Kernels"), False)
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
        layout.addMultiCellWidget(bar, 0, 0, 0, 4)
        self.toolbar = bar

        self.listEntries = EntryView(self)
        layout.addMultiCellWidget(self.listEntries, 1, 1, 0, 4)

        self.checkSaved = QCheckBox(self)
        self.checkSaved.setText(i18n("Remember last booted entry."))
        layout.addWidget(self.checkSaved, 2, 0)

        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer, 2, 1)

        self.labelTimeout = QLabel(self)
        self.labelTimeout.setText(i18n("Timeout:"))
        layout.addWidget(self.labelTimeout, 2, 2)

        self.spinTimeout = QSpinBox(self)
        self.spinTimeout.setMinValue(3)
        self.spinTimeout.setMaxValue(30)
        layout.addWidget(self.spinTimeout, 2, 3)

        self.connect(self.checkSaved, SIGNAL("clicked()"), self.slotCheckSaved)
        self.setTimeoutSlot(True)

        self.init()

    def setTimeoutSlot(self, active):
        if active:
            self.connect(self.spinTimeout, SIGNAL("valueChanged(int)"), self.slotTimeoutChanged)
        else:
            self.disconnect(self.spinTimeout, SIGNAL("valueChanged(int)"), self.slotTimeoutChanged)

    def init(self):
        self.toolbar.setEnabled(True)
        self.listEntries.viewport().setEnabled(True)
        self.checkSaved.setEnabled(True)

    def slotCheckSaved(self):
        def handler():
            self.parent.queryEntries()
        def cancel():
            default = self.parent.options["default"]
            self.checkSaved.setChecked(default == 'saved')
        def error(exception):
            cancel()
        ch = self.parent.callMethod("setOption", "tr.org.pardus.comar.boot.loader.set")
        ch.registerAuthError(error)
        ch.registerDBusError(error)
        ch.registerCancel(cancel)
        ch.registerDone(handler)
        if self.checkSaved.isChecked():
            ch.call("default", "saved")
        else:
            ch.call("default", "0")

    def slotTimeoutChanged(self, value):
        def handler():
            self.spinTimeout.setEnabled(True)
            self.parent.setFocus()
        def cancel():
            self.setTimeoutSlot(False)
            self.spinTimeout.setValue(int(self.parent.options["timeout"]))
            self.setTimeoutSlot(True)
            handler()
        def error(exception):
            self.setTimeoutSlot(False)
            self.spinTimeout.setValue(int(self.parent.options["timeout"]))
            self.setTimeoutSlot(True)
            handler()
        ch = self.parent.callMethod("setOption", "tr.org.pardus.comar.boot.loader.set")
        ch.registerAuthError(error)
        ch.registerDBusError(error)
        ch.registerCancel(cancel)
        ch.registerDone(handler)
        self.spinTimeout.setEnabled(False)
        ch.call("timeout", str(value))

    def slotAddEntry(self):
        self.parent.widgetEditEntry.newEntry()

    def slotUnused(self):
        self.parent.showScreen("Unused")

    def slotHelp(self):
        pass

class widgetEditEntry(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent
        self.systems = self.parent.systems

        self.saved = False
        self.fields = {}

        layout = QGridLayout(self, 1, 1, 11, 6)

        self.labelTitle = QLabel(self)
        self.labelTitle.setText(i18n("Title:"))
        layout.addMultiCellWidget(self.labelTitle, 0, 0, 0, 1)

        self.editTitle = QLineEdit(self)
        self.labelTitle.setMinimumSize(90, 10)
        layout.addMultiCellWidget(self.editTitle, 1, 1, 0, 1)

        self.labelSystem = QLabel(self)
        self.labelSystem.setText(i18n("System:"))
        layout.addMultiCellWidget(self.labelSystem, 2, 2, 0, 1)

        self.listSystem = ComboList(self)
        layout.addWidget(self.listSystem, 3, 0)

        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addItem(spacer, 3, 1)

        self.labelRoot = QLabel(self)
        self.labelRoot.setText(i18n("Root (or UUID):"))
        layout.addMultiCellWidget(self.labelRoot, 4, 4, 0, 1)

        self.editRoot = QLineEdit(self)
        layout.addMultiCellWidget(self.editRoot, 5, 5, 0, 1)

        self.fields["root"] = (self.labelRoot, self.editRoot)

        self.labelKernel = QLabel(self)
        self.labelKernel.setText(i18n("Kernel:"))
        layout.addMultiCellWidget(self.labelKernel, 6, 6, 0, 1)

        self.editKernel = QLineEdit(self)
        layout.addMultiCellWidget(self.editKernel, 7, 7, 0, 1)

        self.fields["kernel"] = (self.labelKernel, self.editKernel)

        self.labelOptions = QLabel(self)
        self.labelOptions.setText(i18n("Kernel Parameters:"))
        layout.addMultiCellWidget(self.labelOptions, 8, 8, 0, 1)

        self.editOptions = QLineEdit(self)
        layout.addMultiCellWidget(self.editOptions, 9, 9, 0, 1)

        self.fields["options"] = (self.labelOptions, self.editOptions)

        self.labelInitrd = QLabel(self)
        self.labelInitrd.setText(i18n("Initial Ramdisk:"))
        layout.addMultiCellWidget(self.labelInitrd, 10, 10, 0, 1)

        self.editInitrd = QLineEdit(self)
        layout.addMultiCellWidget(self.editInitrd, 11, 11, 0, 1)

        self.fields["initrd"] = (self.labelInitrd, self.editInitrd)

        self.checkDefault = QCheckBox(self)
        self.checkDefault.setText(i18n("Set as default boot entry."))
        layout.addMultiCellWidget(self.checkDefault, 12, 12, 0, 1)

        spacer = QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addMultiCell(spacer, 13, 13, 0, 1)

        layout_buttons = QHBoxLayout(layout)
        spacer = QSpacerItem(10, 1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout_buttons.addItem(spacer)

        self.buttonOK = QPushButton(self)
        self.buttonOK.setText(i18n("Save"))
        layout_buttons.addWidget(self.buttonOK)

        self.buttonCancel = QPushButton(self)
        self.buttonCancel.setText(i18n("Cancel"))
        layout_buttons.addWidget(self.buttonCancel)

        layout.addMultiCell(layout_buttons, 14, 14, 0, 1)

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

        if entry.has_key("uuid"):
            entry["root"] = entry["uuid"]

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
        def handler():
            self.parent.widgetEntries.listEntries.setEnabled(True)
        def cancel():
            handler()
        def error(exception):
            handler()

        entries = self.parent.entries
        pardus_entries = []
        pardus_versions = {}
        for entry in entries:
            if entry["os_type"] in ["linux", "xen"] and bool(entry.get("is_pardus_kernel", False)):
                pardus_entries.append(entry)
                version = entry["kernel"].split("kernel-")[1]
                if version not in pardus_versions:
                    pardus_versions[version] = 0
                pardus_versions[version] += 1
        if len(pardus_entries) < 2 and entries[index] in pardus_entries:
            KMessageBox.error(self, i18n("There must be at least one Pardus entry."), i18n("Access Denied"))
            return
        confirm = KMessageBox.questionYesNo(self, i18n("Are you sure you want to remove this entry from the boot loader?"), i18n("Delete Entry"))
        if confirm == KMessageBox.Yes:
            uninstall = "no"
            if entries[index] in pardus_entries:
                entry_version = entries[index]["kernel"].split("kernel-")[1]
                if pardus_versions[entry_version] == 1:
                    confirm_uninstall = KMessageBox.questionYesNo(self, i18n("This is a Pardus kernel entry.\nDo you want to uninstall it from the system?"), i18n("Uninstall Kernel"))
                    if confirm_uninstall == KMessageBox.Yes:
                        uninstall = "yes"

            ch = self.parent.callMethod("removeEntry", "tr.org.pardus.comar.boot.loader.removeentry")
            ch.registerAuthError(error)
            ch.registerDBusError(error)
            ch.registerCancel(cancel)
            ch.registerDone(handler)
            self.parent.widgetEntries.listEntries.setEnabled(False)
            ch.call(index, title, uninstall)

    def resetEntry(self):
        self.entry = None
        systems = self.parent.systems

        self.editTitle.setText("")

        self.listSystem.clear()
        if systems:
            for name in systems:
                label = unicode(systems[name][0])
                self.listSystem.addItem(name, label)

            self.listSystem.setSelected("linux")
            self.slotSystem("Linux")

        for label, (widgetLabel, widgetEdit) in self.fields.iteritems():
            widgetEdit.setText("")

        self.checkDefault.setChecked(False)
        self.buttonOK.setEnabled(True)

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
        self.buttonOK.setEnabled(False)
        default = "no"
        if self.parent.widgetEntries.checkSaved.isChecked():
            default = "saved"
        elif self.checkDefault.isChecked():
            default = "yes"

        systems = self.parent.systems
        os_type = self.listSystem.getSelected()

        args = {
            "title": unicode(self.editTitle.text()),
            "os_type": os_type,
            "root": "",
            "kernel": "",
            "initrd": "",
            "options": "",
            "default": default,
            "index": -1,
        }

        for label in self.fields:
            if label in systems[os_type][1]:
                value = unicode(self.fields[label][1].text())
                args[label] = value

        if self.entry:
            args["index"] = int(self.entry["index"])

        self.saved = True

        def handlerError(exception):
            self.parent.widgetEditEntry.saved = False
            KMessageBox.error(self, unicode(exception.message), i18n("Failed"))
            self.parent.widgetEditEntry.buttonOK.setEnabled(True)
        def handler():
            self.parent.widgetEditEntry.saved = False
            self.parent.queryEntries()
            self.parent.widgetEditEntry.slotExit()
        ch = self.parent.callMethod("setEntry", "tr.org.pardus.comar.boot.loader.set")
        ch.registerDone(handler)
        ch.registerError(handlerError)
        ch.call(args["title"], args["os_type"], args["root"], args["kernel"], args["initrd"], args["options"], args["default"], args["index"])

    def slotExit(self):
        self.resetEntry()
        self.parent.showScreen("Entries")

class widgetUnused(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.parent = parent

       # self.link = comar_link

        layout = QGridLayout(self, 1, 1, 11, 6)

        self.labelTitle = QLabel(self)
        self.labelTitle.setText(i18n("These kernels are installed in the system but doesn't exist in boot loader list:"))
        layout.addWidget(self.labelTitle, 0, 0)

        self.listKernels = QListBox(self)
        self.listKernels.setMinimumSize(100, 200)
        self.listKernels.setSelectionMode(QListBox.Extended)
        layout.addMultiCellWidget(self.listKernels, 1, 4, 0, 0)

        self.buttonAdd = QPushButton(self)
        self.buttonAdd.setText(i18n("Add Boot Entry"))
        self.buttonAdd.setEnabled(False)
        layout.addWidget(self.buttonAdd, 1, 1)

        self.buttonRemove = QPushButton(self)
        self.buttonRemove.setText(i18n("Uninstall"))
        self.buttonRemove.setEnabled(False)
        layout.addWidget(self.buttonRemove, 2, 1)

        spacer = QSpacerItem(10, 1, QSizePolicy.Fixed, QSizePolicy.Expanding)
        layout.addItem(spacer, 3, 1)

        self.buttonOK = QPushButton(self)
        self.buttonOK.setText(i18n("Ok"))
        layout.addWidget(self.buttonOK, 4, 1)

        self.connect(self.buttonAdd, SIGNAL("clicked()"), self.slotAdd)
        self.connect(self.buttonRemove, SIGNAL("clicked()"), self.slotRemove)
        self.connect(self.buttonOK, SIGNAL("clicked()"), self.slotExit)
        self.connect(self.listKernels, SIGNAL("selectionChanged()"), self.slotKernels)

        self.listBusy = False
        self.listUnused()

    def listUnused(self):
        def handler(versions):
            self.listKernels.clear()
            for version in versions:
                if version.strip():
                    self.listKernels.insertItem(version)
            self.slotKernels()
        ch = self.parent.callMethod("listUnused", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()

    def slotKernels(self):
        item = self.listKernels.firstItem()
        versions = []
        while item:
            if item.isSelected():
                versions.append(str(item.text()))
            item = item.next()
        if len(versions):
            self.buttonAdd.setEnabled(True)
            self.buttonRemove.setEnabled(True)
        else:
            self.buttonAdd.setEnabled(False)
            self.buttonRemove.setEnabled(False)

    def slotAdd(self):
        self.buttonAdd.setEnabled(False)
        self.buttonRemove.setEnabled(False)
        self.parent.widgetEditEntry.newEntry()

        version = str(self.listKernels.currentText())
        root = getRoot()
        self.parent.widgetEditEntry.editTitle.setText(version)
        self.parent.widgetEditEntry.editRoot.setText(root)
        if version.endswith("-dom0"):
            self.parent.widgetEditEntry.listSystem.setCurrentText("Xen")
        else:
            self.parent.widgetEditEntry.listSystem.setCurrentText("Linux")
        self.parent.widgetEditEntry.editKernel.setText("/boot/kernel-%s" % version)
        self.parent.widgetEditEntry.editOptions.setText("root=%s" % root)

    def slotRemove(self):
        confirm = KMessageBox.questionYesNo(self, i18n("Do you want to uninstall selected kernel(s) from the system?"), i18n("Uninstall Kernel"))
        if confirm == KMessageBox.Yes:
            self.buttonAdd.setEnabled(False)
            self.buttonRemove.setEnabled(False)
            item = self.listKernels.firstItem()
            versions = []
            while item:
                if item.isSelected():
                    versions.append(str(item.text()))
                item = item.next()
            if len(versions):
                self.listBusy = True
                def handler(isLast=False):
                    if isLast:
                        self.listBusy = False
                        self.listUnused()
                    self.setEnabled(True)
                    self.buttonAdd.setEnabled(True)
                    self.buttonRemove.setEnabled(True)
                def cancel():
                    self.setEnabled(True)
                    self.buttonAdd.setEnabled(True)
                    self.buttonRemove.setEnabled(True)

                for version in versions:
                    ch = self.parent.callMethod("removeUnused", "tr.org.pardus.comar.boot.loader.removeunused")
                    ch.registerDone(handler, version == versions[-1])
                    ch.registerCancel(cancel)
                    self.setEnabled(False)
                    ch.call(version)

    def slotExit(self):
        self.parent.showScreen("Entries")

class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)

        #self.link = None
        self.dia = None

        if not self.openBus():
            sys.exit(1)

        self.entries = []
        self.options = {}
        self.systems = {}
        self.screens = []

        layout = QGridLayout(self, 1, 1, 0, 0)
        self.stack = QWidgetStack(self)
        layout.addWidget(self.stack, 0, 0)

        self.widgetEntries = widgetEntryList(self)
        self.stack.addWidget(self.widgetEntries)
        self.screens.append("Entries")

        self.widgetEditEntry = widgetEditEntry(self)
        self.stack.addWidget(self.widgetEditEntry)
        self.screens.append("EditEntry")

        self.widgetUnused = widgetUnused(self)
        self.stack.addWidget(self.widgetUnused)
        self.screens.append("Unused")

        self.setup()

    def openBus(self):
        try:
            self.busSys = dbus.SystemBus()
            self.busSes = dbus.SessionBus()
        except dbus.DBusException:
            KMessageBox.error(self, i18n("Unable to connect to DBus."), i18n("DBus Error"))
            return False
        return True

    def setup(self):
        self.queryOptions()
        self.querySystems()
        self.queryEntries()
        self.listenSignals()

    def callMethod(self, method, action):
        ch = CallHandler("grub", "Boot.Loader", method,
                         action,
                         self.winId(),
                         self.busSys, self.busSes)
        ch.registerAuthError(self.comarError)
        ch.registerDBusError(self.busError)
        ch.registerCancel(self.cancelError)
        return ch

    def cancelError(self):
        message = i18n("You are not authorized for this operation.")
        KMessageBox.sorry(None, message, i18n("Error"))

    def busError(self, exception):
        if self.dia:
            return
        self.dia = KProgressDialog(None, "lala", i18n("Waiting DBus..."), i18n("Connection to the DBus unexpectedly closed, trying to reconnect..."), True)
        self.dia.progressBar().setTotalSteps(50)
        self.dia.progressBar().setTextEnabled(False)
        self.dia.show()
        start = time.time()
        while time.time() < start + 5:
            if self.openBus():
                self.dia.close()
                self.setup()
                return
            if self.dia.wasCancelled():
                break
            percent = (time.time() - start) * 10
            self.dia.progressBar().setProgress(percent)
            qApp.processEvents(100)
        self.dia.close()
        KMessageBox.sorry(None, i18n("Cannot connect to the DBus! If it is not running you should start it with the 'service dbus start' command in a root console."))
        sys.exit()

    def comarError(self, exception):
        if "Access denied" in exception.message:
            message = i18n("You are not authorized for this operation.")
            KMessageBox.sorry(self, message, i18n("Error"))
        else:
            KMessageBox.error(self, str(exception), i18n("COMAR Error"))

    def listenSignals(self):
        self.busSys.add_signal_receiver(self.handleSignals, dbus_interface="tr.org.pardus.comar.Boot.Loader", member_keyword="signal", path_keyword="path")

    def handleSignals(self, *args, **kwargs):
        path = kwargs["path"]
        signal = kwargs["signal"]
        if not path.startswith("/package/"):
            return
        if signal == "Changed":
            if args[0]== "entry":
                self.queryEntries()
                if self.widgetEditEntry.entry and not self.widgetEditEntry.saved:
                    KMessageBox.information(self, i18n("Bootloader configuration changed by another application."), i18n("Warning"))
                    self.widgetEditEntry.slotExit()
                if not self.widgetUnused.listBusy:
                    self.widgetUnused.listUnused()

    def showScreen(self, label):
        screen = self.screens.index(label)
        self.stack.raiseWidget(screen)

    def queryOptions(self):
        def handler(options):
            for key, value in options.iteritems():
                self.options[key] = value
            # Default entry
            if self.options["default"] == "saved":
                self.widgetEntries.checkSaved.setChecked(True)
            # Timeout
            timeout = int(self.options["timeout"])
            self.widgetEntries.setTimeoutSlot(False)
            self.widgetEntries.spinTimeout.setValue(timeout)
            self.widgetEntries.setTimeoutSlot(True)
        ch = self.callMethod("getOptions", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()

    def querySystems(self):
        def handler(systems):
            self.systems = {}
            for name, info in systems.iteritems():
                label, fields_req, fields_opt = info
                fields = fields_req + fields_opt
                self.systems[name] = (label, fields)
        ch = self.callMethod("listSystems", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()

    def queryEntries(self):
        def handler(entries):
            self.widgetEntries.listEntries.clear()
            self.entries = []
            for entry in entries:
                self.entries.append(entry)

                if entry.has_key("root"):
                    root_or_uuid = entry["root"]
                elif entry.has_key("uuid"):
                    root_or_uuid = entry["uuid"]
                else:
                    root_or_uuid = ""

                self.widgetEntries.listEntries.add(self.widgetEditEntry,
                                                   int(entry["index"]),
                                                   unicode(entry["title"]),
                                                   root_or_uuid,
                                                   bool(entry.get("is_pardus_kernel", False)),
                                                   entry)

        self.widgetEntries.listEntries.setEnabled(True)
        ch = self.callMethod("listEntries", "tr.org.pardus.comar.boot.loader.get")
        ch.registerDone(handler)
        ch.call()
