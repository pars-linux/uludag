#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
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

import kdedesigner
from boot_manager import formMain

import comar

class widgetMain(formMain):
    def __init__(self, parent):
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)

        formMain.__init__(self, parent)
        self.listEntries.setSorting(-1)
        self.listOptions.setSorting(-1)
        self.listCommands.setSorting(-1)

        self.link.ask_notify('System.Boot.changed', id=1)
        self.link.call('System.Boot.listOptions', id=2)
        self.link.call('System.Boot.listEntries', id=3)

        self.connect(self.listEntries, SIGNAL('currentChanged(QListViewItem *)'), self.slotClickEntries)

    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == 'notify':
            self.link.call('System.Boot.listOptions', id=2)
            self.link.call('System.Boot.listEntries', id=3)
        else:
            if reply.id == 2: # listOptions
                self.listOptions.clear()
                item = None
                for option in reply.data.split('\n'):
                    key, value = option.split()
                    if item:
                        item = KListViewItem(self.listOptions, item)
                    else:
                        item = KListViewItem(self.listOptions)
                    item.setText(0, key)
                    item.setText(1, unicode(value))
            elif reply.id == 3: # listEntries
                self.listEntries.clear()
                self.listCommands.clear()
                index = 0
                item = None
                for entry in reply.data.split('\n'):
                    if item:
                        item = KListViewItem(self.listEntries, item)
                    else:
                        item = KListViewItem(self.listEntries)
                    item.setText(0, unicode(entry))
                    item.entry_index = index
                    index += 1
            elif reply.id == 4: # getEntry
                self.listCommands.clear()
                item = None
                for cmd in reply.data.split("\n\n"):
                    key, options, value = cmd.split("\n")
                    if options == " ":
                        options = ""
                    if value == " ":
                        value = ""
                    if item:
                        item = KListViewItem(self.listCommands, item)
                    else:
                        item = KListViewItem(self.listCommands)
                    item.setText(0, "%s (%s) = %s" % (key, options, unicode(value)))

    def slotClickEntries(self, item):
        if not item:
            return
        self.link.call('System.Boot.getEntry', {'index': item.entry_index}, id=4)
