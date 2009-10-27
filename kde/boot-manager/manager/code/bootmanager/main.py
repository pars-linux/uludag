#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009 TUBITAK/UEKAE
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

# PyKDE
from PyKDE4 import kdeui
from PyKDE4 import kdecore

# UI
from bootmanager.ui_main import Ui_MainWidget

# Backend
from bootmanager.backend import Interface

# Config
from bootmanager.config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME

# Utils
from bootmanager.utility import getDiskByUUID

# Item widget
from bootmanager.item import ItemListWidgetItem, ItemWidget

# Edit widget
from bootmanager.edit import EditWidget

# Options widget
from bootmanager.options import OptionsWidget


class MainWidget(QtGui.QWidget, Ui_MainWidget):
    def __init__(self, parent, embed=False):
        QtGui.QWidget.__init__(self, parent)

        if embed:
            self.setupUi(parent)
        else:
            self.setupUi(self)

        # Animation
        self.animator = QtCore.QTimeLine(ANIM_TIME, self)
        self.animationLast = ANIM_HIDE

        # Initialize heights of animated widgets
        self.slotAnimationFinished()

        # Backend
        self.iface = Interface()
        self.iface.listenSignals(self.signalHandler)

        # Fail if no packages provide backend
        self.checkBackend()

        # Set options widget
        self.widgetOptions = OptionsWidget(self)
        self.verticalItemsLayout.insertWidget(-1, self.widgetOptions)

        # Build item list
        self.buildItemList()

        # Edit widget
        layout = QtGui.QVBoxLayout(self.frameWidget)
        self.widgetEdit = EditWidget(self.frameWidget)
        layout.addWidget(self.widgetEdit)

        # Build menu
        self.buildMenu()

        # Build filter
        self.buildFilter()

        # Signals
        self.connect(self.comboFilter, QtCore.SIGNAL("currentIndexChanged(int)"), self.slotFilterChanged)
        self.connect(self.pushNew, QtCore.SIGNAL("triggered(QAction*)"), self.slotOpenEdit)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.slotSaveEdit)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.slotCancelEdit)
        self.connect(self.animator, QtCore.SIGNAL("frameChanged(int)"), self.slotAnimate)
        self.connect(self.animator, QtCore.SIGNAL("finished()"), self.slotAnimationFinished)
        self.connect(self.widgetOptions, QtCore.SIGNAL("timeoutChanged(int)"), self.slotTimeoutChanged)

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            kdeui.KMessageBox.error(self, kdecore.i18n("There are no packages that provide backend for this application.\nPlease make sure that packages are installed and configured correctly."))
            return False
        return True

    def hideNew(self):
        """
            Hides new button.
        """
        self.pushNew.hide()

    def hideFilter(self):
        """
            Hide filter.
        """
        self.comboFilter.hide()

    def clearItemList(self):
        """
            Clears item list.
        """
        self.listItems.clear()

    def makeItemWidget(self, id_, title="", description="", type_=None, icon=None, state=None):
        """
            Makes an item widget having given properties.
        """
        widget = ItemWidget(self.listItems, id_, title, description, type_, icon, state)

        self.connect(widget, QtCore.SIGNAL("stateChanged(int)"), self.slotItemState)
        self.connect(widget, QtCore.SIGNAL("editClicked()"), self.slotItemEdit)
        self.connect(widget, QtCore.SIGNAL("deleteClicked()"), self.slotItemDelete)

        return widget

    def addItem(self, id_, name="", description="", os_type="", default=False):
        """
            Adds an item to list.
        """
        icon = kdeui.KIcon("tux")
        type_ = os_type

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, type_, icon, default)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

        # Check if a filter matches item
        if not self.itemMatchesFilter(widgetItem):
            self.listItems.setItemHidden(widgetItem, True)

    def buildItemList(self):
        """
            Builds item list.
        """
        # Options
        self.options = self.iface.getOptions()
        self.widgetOptions.setTimeout(self.options.get("timeout", "0"))

        # Clear list
        self.clearItemList()
        self.systems = self.iface.getSystems()
        self.entries = []

        def handleList(package, exception, args):
            if exception:
                pass
                # TODO: Handle exception
            else:
                self.entries = args[0]
                for index, entry in enumerate(self.entries):
                    if "root" in entry:
                        root = entry["root"]
                    elif "uuid" in entry:
                        root = getDiskByUUID(entry["uuid"])
                    else:
                        root = ""
                    default = False
                    if self.options.get("default", "0") == str(index):
                        default = True
                    self.addItem(entry["index"], entry["title"], root, entry["os_type"], default)
        self.iface.getEntries(func=handleList)

    def itemMatchesFilter(self, item):
        """
            Checks if item matches selected filter.
        """
        filter = str(self.comboFilter.itemData(self.comboFilter.currentIndex()).toString())
        if filter != "all":
            if filter != item.getType():
                return False
        return True

    def buildFilter(self):
        """
            Builds item filter.
        """
        self.comboFilter.clear()
        self.comboFilter.addItem(kdecore.i18n("All Items"), QtCore.QVariant("all"))

        for name, (label, mandatory, optional) in self.systems.iteritems():
            self.comboFilter.addItem(label, QtCore.QVariant(name))

    def buildMenu(self):
        """
            Builds "Add New" button menu.
        """
        # Create menu for "new" button
        menu = QtGui.QMenu(self.pushNew)
        self.pushNew.setMenu(menu)

        # Actions
        for name, (label, mandatory, optional) in self.systems.iteritems():
            action_user = QtGui.QAction(label, self)
            action_user.setData(QtCore.QVariant(name))
            menu.addAction(action_user)

    def showEditBox(self, id_, type_=None):
        """
            Shows edit box.
        """
        self.widgetEdit.show()
        self.widgetEdit.reset()

        self.widgetEdit.setType(type_)

        if type_ in self.systems:
            fields = self.systems[type_][1] + self.systems[type_][2]
            if "root" not in fields:
                self.widgetEdit.hideDisk()
            if "kernel" not in fields:
                self.widgetEdit.hideKernel()
            if "initrd" not in fields:
                self.widgetEdit.hideRamdisk()
            if "options" not in fields:
                self.widgetEdit.hideOptions()

        if id_ != None:
            entry = self.entries[int(id_)]
            self.widgetEdit.setId(int(id_))
            self.widgetEdit.setTitle(entry["title"])
            if "root" in entry:
                self.widgetEdit.setDisk(entry["root"])
            elif "uuid" in entry:
                self.widgetEdit.setDisk(entry["uuid"])
            if "kernel" in entry:
                self.widgetEdit.setKernel(entry["kernel"])
            if "initrd" in entry:
                self.widgetEdit.setRamdisk(entry["initrd"])
            if "options" in entry:
                self.widgetEdit.setOptions(entry["options"])

        if self.animationLast == ANIM_HIDE:
            self.animationLast = ANIM_SHOW
            # Set range
            self.animator.setFrameRange(ANIM_TARGET, self.height() - ANIM_TARGET)
            # Go go go!
            self.animator.start()

    def hideEditBox(self):
        """
            Hides edit box.
        """
        if self.animationLast == ANIM_SHOW:
            self.animationLast = ANIM_HIDE
            # Set range
            self.animator.setFrameRange(self.frameEdit.height(), ANIM_TARGET)
            # Go go go!
            self.animator.start()

    def slotFilterChanged(self, index):
        """
            Filter is changed, refresh item list.
        """
        for i in range(self.listItems.count()):
            widgetItem = self.listItems.item(i)
            if self.itemMatchesFilter(widgetItem):
                self.listItems.setItemHidden(widgetItem, False)
            else:
                self.listItems.setItemHidden(widgetItem, True)

    def slotItemState(self, state):
        """
            Item state changed.
        """
        widget = self.sender()
        def handler(package, exception, args):
            if exception:
                self.buildItemList()
        self.iface.setOption("default", widget.getId(), func=handler)

    def slotItemEdit(self):
        """
            Edit button clicked, show edit box.
        """
        widget = self.sender()
        self.showEditBox(widget.getId(), widget.getType())

    def slotItemDelete(self):
        """
            Delete button clicked.
        """
        widget = self.sender()
        if kdeui.KMessageBox.questionYesNo(self, kdecore.i18n("Do you want to delete '%1'?", widget.getTitle())) == kdeui.KMessageBox.Yes:
            def handler(package, exception, args):
                pass
            self.iface.removeEntry(widget.getId(), widget.getTitle(), False, func=handler)

    def slotOpenEdit(self, action):
        """
            New button clicked, show edit box.
        """
        # Get item type to add
        type_ = str(action.data().toString())
        self.showEditBox(None, type_)

    def slotCancelEdit(self):
        """
            Cancel clicked on edit box, show item list.
        """
        self.hideEditBox()

    def slotSaveEdit(self):
        """ 
            Save clicked on edit box, save item details then show item list.
        """
        try:
            widget = self.widgetEdit
            if widget.isNew():
                self.iface.setEntry(widget.getTitle(), widget.getType(), widget.getDisk(), widget.getKernel(), widget.getRamdisk(), widget.getOptions(), "no", -1)
            else:
                self.iface.setEntry(widget.getTitle(), widget.getType(), widget.getDisk(), widget.getKernel(), widget.getRamdisk(), widget.getOptions(), "no", widget.getId())
        except Exception, e: # TODO: Named exception should be raised
            if "Comar.PolicyKit" in e._dbus_error_name:
                kdeui.KMessageBox.error(self, kdecore.i18n("Access denied."))
            else:
                kdeui.KMessageBox.error(self, unicode(e))
            return
        # Hide edit box
        self.hideEditBox()

    def slotAnimate(self, frame):
        """
            Animation frame changed.
        """
        self.frameEdit.setMaximumHeight(frame)
        self.frameList.setMaximumHeight(self.height() - frame)
        self.update()

    def slotAnimationFinished(self):
        """
            Animation is finished.
        """
        if self.animationLast == ANIM_SHOW:
            self.frameEdit.setMaximumHeight(ANIM_DEFAULT)
            self.frameList.setMaximumHeight(ANIM_TARGET)
        else:
            self.frameEdit.setMaximumHeight(ANIM_TARGET)
            self.frameList.setMaximumHeight(ANIM_DEFAULT)

    def slotButtonStatusChanged(self, status):
        if status:
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        else:
            self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)

    def slotTimeoutChanged(self, timeout):
        def handler(package, exception, args):
            if exception:
                self.widgetOptions.setTimeout(self.options["timeout"])
            else:
                self.options["timeout"] = timeout
        self.iface.setOption("timeout", str(timeout), func=handler)

    def signalHandler(self, package, signal, args):
        self.buildItemList()
