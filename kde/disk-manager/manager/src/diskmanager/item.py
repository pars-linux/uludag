#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2011 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PyQt
from PyQt4 import QtCore
from PyQt4 import QtGui

# Pds vs Kde Stuff
import context as ctx

if ctx.Pds.session == ctx.pds.Kde4:
    from PyKDE4.kdeui import KIcon
else:
    from diskmanager.context import KIcon

# UI
from diskmanager.ui_item import Ui_ItemWidget

class ItemListWidgetItem(QtGui.QListWidgetItem):

    def __init__(self, parent, widget):
        QtGui.QListWidgetItem.__init__(self, parent)
        self.widget = widget
        self.setSizeHint(QtCore.QSize(300, 48))

    def getId(self):
        return self.widget.getId()

    def getType(self):
        return self.widget.getType()

class ItemWidget(QtGui.QWidget, Ui_ItemWidget):

    def __init__(self, parent, id_, title="", description="", type_=None, icon=None, state=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.id = id_
        self.type = type_

        self.setTitle(title)
        self.setDescription(description)

        if icon:
            self.setIcon(icon)
        else:
            self.labelIcon.hide()

        self.setState(state)

        # Buttons
        self.pushEdit.setIcon(KIcon("preferences-other"))
        self.pushDelete.setIcon(KIcon("edit-delete"))

        # Signals
        self.connect(self.checkState, QtCore.SIGNAL("clicked()"), lambda: self.emit(QtCore.SIGNAL("stateChanged(int)"), self.checkState.checkState()))
        self.connect(self.pushEdit, QtCore.SIGNAL("clicked()"), lambda: self.emit(QtCore.SIGNAL("editClicked()")))
        self.connect(self.pushDelete, QtCore.SIGNAL("clicked()"), lambda: self.emit(QtCore.SIGNAL("deleteClicked()")))

    def mouseDoubleClickEvent(self, event):
        self.pushEdit.animateClick(100)

    def getId(self):
        return self.id

    def getType(self):
        return self.type

    def setTitle(self, title):
        self.labelTitle.setText(unicode(title))

    def getTitle(self):
        return unicode(self.labelTitle.text())

    def setDescription(self, description):
        self.labelDescription.setText(unicode(description))

    def getDescription(self):
        return unicode(self.labelDescription.text())

    def setIcon(self, icon):
        self.labelIcon.setPixmap(icon.pixmap(32, 32))

    def getState(self):
        return self.checkState.checkState()

    def setState(self, state):
        
        return self.checkState.setCheckState(QtCore.Qt.Checked if state else QtCore.Qt.Unchecked)

    def hideEdit(self):
        self.pushEdit.hide()

    def hideDelete(self):
        self.pushDelete.hide()

