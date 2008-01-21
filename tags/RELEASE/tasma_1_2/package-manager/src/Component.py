#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *

class Component:
    def __init__(self, name, packages, summary):
        self.name = name
        self.packages = packages
        self.summary = summary

    def remove(self, package):
        self.packages.remove(package)

class ComponentTipper(QToolTip):
    def __init__(self, parent):
        super(ComponentTipper, self).__init__(parent.componentsList.viewport())
        self.components = parent.componentDict
        self.list = parent.componentsList
        self.setWakeUpDelay(500)

    def maybeTip(self, point):
        item = self.list.itemAt(point)
        if item:
            component = self.components[item]
            self.tip(self.list.itemRect(item),
                     u"<b>%s</b> - %s" %
                     (component.name, component.summary))
