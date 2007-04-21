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
from khtml import *

import locale
import os

def I18N_NOOP(str):
    return str

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)

class HelpDialog(QDialog):
    def __init__(self, name, title, parent=None):
        QDialog.__init__(self, parent)
        self.setCaption(title)
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500, 600)
        self.layout.addWidget(self.htmlPart.view(), 1, 1)

        lang = locale.setlocale(locale.LC_MESSAGES)
        if '_' in lang:
            lang = lang.split('_', 1)[0]
        url = locate('data', '%s/help/%s/main_help.html' % (name, lang))
        if not os.path.exists(url):
            url = locate('data', '%s/help/en/main_help.html' % name)
        self.htmlPart.openURL(KURL(url))

def getRoot():
    import os
    for mount in os.popen("/bin/mount").readlines():
        mount_items = mount.split()
        if mount_items[2] == "/":
            return mount_items[0]

def grubDevice(dev):
    dev = dev.split("/")[2]
    return "(hd%s,%s)" % (ord(dev[2:3]) - ord("a"), int(dev[3:]) - 1)

def grubDeviceName(dev):
    disk, part = dev[3:-1].split(",")
    disk = int(disk) + 1
    part = int(part) + 1
    return i18n("Disk %1, Partition %2").arg(disk).arg(part)

def parseGrubCommand(command_str):
    index = None
    title = ""
    commands = []
    for cmd in command_str.split("\n\n"):
        key, options, value = cmd.split("\n")
        if options == " ":
            options = ""
        if value == " ":
            value = ""
        if key == "index":
            index = int(value)
        elif key == "title":
            title = value
        else:
            commands.append([key, options, value])
    return index, title, commands

def formatGrubCommand(command_lst):
    commands = []
    for key, opts, value in command_lst:
        if not opts:
            opts = " "
        if not value:
            value = " "
        commands.append("%s\n%s\n%s" % (key, opts, value))
    return "\n\n".join(commands)
