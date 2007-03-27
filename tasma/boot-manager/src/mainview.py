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

import comar

class Entry(QListBoxItem):
    def __init__(self, parent, title, description=""):
        QListBoxItem.__init__(self, parent)
        self.title = title
        self.description = description
        self.f1 = QFont()
        self.f2 = QFont()
        self.f1.setBold(True)
        self.f1.setPointSize(self.f1.pointSize() + 1)
        #self.pix = QPixmap(locate("data", "net_kga/net-down.png"))
        self.pix = QPixmap("/usr/share/icons/Tulliana-2.0/48x48/apps/penguin.png")
    
    def paint(self, painter):
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        painter.setPen(Qt.black)
        painter.setFont(self.f1)
        painter.drawText(48 + 3, 10 + fm.ascent(), self.title)
        painter.setFont(self.f2)
        painter.setPen(Qt.gray)
        painter.drawText(48 + 3, 10 + fm.height() + 3 + fm2.ascent(), self.description)
        painter.drawPixmap(3, 3, self.pix)
    
    def height(self, box):
        fm = QFontMetrics(self.f1)
        fm2 = QFontMetrics(self.f2)
        return 3 + fm.height() + 3 + fm2.height() + 3 + fm2.height() + 3
    
    def width(self, box):
        return 100

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
        
        self.link.ask_notify('System.Boot.changed', id=1)
        self.link.call('System.Boot.listEntries', id=2)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.command == 'notify':
            self.link.call('System.Boot.listEntries', id=2)
        elif reply.command == 'result':
            if reply.id == 2: # listEntries
                self.listEntries.clear()
                index = 0
                for entry in reply.data.split('\n'):
                    item = Entry(self.listEntries, entry)
                    self.link.call('System.Boot.getEntry', {'index': index}, id=4)
                    item.entry_index = index
                    index += 1
            elif reply.id == 4: # getEntry
                index = None
                root = ""
                for cmd in reply.data.split("\n\n"):
                    key, options, value = cmd.split("\n")
                    if options == " ":
                        options = ""
                    if value == " ":
                        value = ""
                    if key == "index":
                        index = int(value)
                    if key == "kernel" and value.startswith("("):
                        root = value.split(")")[0] + ")"
                    elif key == "root":
                        root = value
                if root:
                    item = self.listEntries.item(index)
                    item.description = grubDeviceName(root)
                    self.listEntries.updateItem(index)
