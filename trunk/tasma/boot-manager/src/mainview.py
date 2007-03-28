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
from ui_elements import *

import comar

class widgetMain(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)
        
        layout = QGridLayout(self, 1, 1, 11, 6, "formMainLayout")
        self.listEntries = QListBox(self)
        layout.addWidget(self.listEntries, 0, 0)
        
        self.default = -1
        
        self.link.ask_notify('System.Boot.changed', id=1)
        self.link.call('System.Boot.listEntries', id=2)
        self.link.call('System.Boot.listOptions', id=3)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == 'notify':
            self.default = -1
            self.link.call('System.Boot.listEntries', id=2)
            self.link.call('System.Boot.listOptions', id=3)
        elif reply.command == 'result':
            if reply.id == 2: # listEntries
                self.listEntries.clear()
                index = 0
                for entry in reply.data.split('\n'):
                    item = Entry(self.listEntries, entry, checked=index==self.default, index=index)
                    self.link.call('System.Boot.getEntry', {'index': index}, id=4)
                    index += 1
            elif reply.id == 3: # listOptions
                index = 0
                for option in reply.data.split('\n'):
                    key, value = option.split()
                    if key == "default":
                        index = int(value)
                self.default = index
                item = self.listEntries.item(index)
                if item:
                    item.checked = True
                    self.listEntries.updateItem(index)
            elif reply.id == 4: # getEntry
                index = None
                os_type = "Unknown"
                root = ""
                for cmd in reply.data.split("\n\n"):
                    key, options, value = cmd.split("\n")
                    if options == " ":
                        options = ""
                    if value == " ":
                        value = ""
                    if key == "index":
                        index = int(value)
                    elif key == "kernel":
                        if "root" in value:
                            os_type = "Linux"
                        if value.startswith("("):
                            root = value.split(")")[0] + ")"
                    elif key == "root":
                        root = value
                    elif key == "rootnoverify":
                        root = value
                    elif key == "makeactive":
                        os_type = "Windows"
                item = self.listEntries.item(index)
                item.description = grubDeviceName(root)
                if os_type == "Linux" and root == grubDevice(getRoot()):
                    os_type = "Pardus"
                item.setOs(os_type)
                self.listEntries.updateItem(index)
