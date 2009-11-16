#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *

class Group:
    def __init__(self, name, packages, summary):
        self.name = name
        self.packages = packages
        self.summary = summary

    def remove(self, package):
        self.packages.remove(package)

class GroupTipper(QToolTip):
    def __init__(self, parent):
        super(GroupTipper, self).__init__(parent.groupsList.viewport())
        self.groups = parent.groupDict
        self.list = parent.groupsList
        self.setWakeUpDelay(500)

    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item:
            group = self.groups[item]
            self.tip(self.list.itemRect(item),
                     u"<b>%s</b> - %s" %
                     (group.name, group.summary))
