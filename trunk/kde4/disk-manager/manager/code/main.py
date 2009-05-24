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
from ui_main import Ui_MainWidget

# Backend
from backend import Interface

# Config
from config import ANIM_SHOW, ANIM_HIDE, ANIM_TARGET, ANIM_DEFAULT, ANIM_TIME

# Item widget
from item import ItemListWidgetItem, ItemWidget

# Edit widget
from edit import EditWidget


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

        # Fail if no packages provide backend
        self.checkBackend()

        # We don't need a "new" button
        self.hideNew()

        # We don't need a filter
        self.hideFilter()

        # Build item list
        self.buildItemList()

        # Signals
        self.connect(self.comboFilter, QtCore.SIGNAL("currentIndexChanged(int)"), self.slotFilterChanged)
        self.connect(self.pushNew, QtCore.SIGNAL("triggered(QAction*)"), self.slotOpenEdit)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.slotSaveEdit)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.slotCancelEdit)
        self.connect(self.animator, QtCore.SIGNAL("frameChanged(int)"), self.slotAnimate)
        self.connect(self.animator, QtCore.SIGNAL("finished()"), self.slotAnimationFinished)

    def checkBackend(self):
        """
            Check if there are packages that provide required backend.
        """
        if not len(self.iface.getPackages()):
            kdeui.KMessageBox.error(self, kdecore.i18n("There are no packages that provide backend for this application.\nPlease be sure that packages are installed and configured correctly."))
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

    def addItem(self, id_, name="", description=""):
        """
            Adds an item to list.
        """
        icon = "drive-harddisk"
        type_ = "disk"

        # Build widget and widget item
        widget = self.makeItemWidget(id_, name, description, type_, kdeui.KIcon(icon), None)
        widgetItem = ItemListWidgetItem(self.listItems, widget)

        # Delete is unnecessary
        widget.hideDelete()

        # Add to list
        self.listItems.setItemWidget(widgetItem, widget)

        # Check if a filter matches item
        if not self.itemMatchesFilter(widgetItem):
            self.listItems.setItemHidden(widgetItem, True)

    def buildItemList(self):
        """
            Builds item list.
        """
        # Clear list
        self.clearItemList()
        self.device_entries = {}

        for entry in self.iface.entryList():
            if entry.startswith("/dev"):
                self.device_entries[entry] = entry
            elif entry.startswith("LABEL="):
                label = entry.split("LABEL=")[1]
                self.device_entries[self.iface.getDeviceByLabel(label)] = entry

        def handleList(package, exception, args):
            if exception:
                pass
                # TODO: Handle exception
            else:
                devices = args[0]
                for device in devices:
                    # self.addItem(device, device, "")
                    parts = self.iface.partitionList(device)
                    parts.sort()
                    for part in parts:
                        self.addItem(part, part, "")

        self.iface.deviceList(func=handleList)

    def itemMatchesFilter(self, item):
        """
            Checks if item matches selected filter.
        """
        filter = str(self.comboFilter.itemData(self.comboFilter.currentIndex()).toString())
        return True

    def buildFilter(self):
        """
            Builds item filter.
        """
        self.comboFilter.clear()
        self.comboFilter.addItem(kdecore.i18n("All Items"), QtCore.QVariant("all"))

    def buildMenu(self):
        """
            Builds "Add New" button menu.
        """
        # Create menu for "new" button
        menu = QtGui.QMenu(self.pushNew)
        self.pushNew.setMenu(menu)

        # New action
        action_user = QtGui.QAction(kdecore.i18n("Add"), self)
        action_user.setData(QtCore.QVariant("item"))
        menu.addAction(action_user)

    def showEditBox(self, id_, type_=None):
        """
            Shows edit box.
        """
        # Reset fields
        # self.widgetEdit.reset()
        # Show user edit
        self.widgetEdit.show()
        if id_:
            """
            try:
                username, fullname, gid, homedir, shell, groups = self.iface.userInfo(id_)
            except Exception, e: # TODO: Named exception should be raised
                if "Comar.PolicyKit" in e._dbus_error_name:
                    kdeui.KMessageBox.error(self, i18n("Access denied."))
                else:
                    kdeui.KMessageBox.error(self, unicode(e))
                return
            """

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
        pass

    def slotItemEdit(self):
        """
            Edit button clicked, show edit box.
        """
        widget = self.sender()
        from PyKDE4.kdeui import KPageDialog, KPageWidgetItem

        # TODO: Move this into another module ASAP

        dialog = KPageDialog(self);
        dialog.setFaceType(KPageDialog.Tabbed)
        dialog.setCaption(kdecore.i18n("Settings"))

        page_widget = EditWidget(dialog)
        page_item = KPageWidgetItem(page_widget, kdecore.i18n("Settings"))

        if widget.getId() in self.device_entries:
            path, fsType, options = self.iface.getEntry(self.device_entries[widget.getId()])
            page_widget.setAutoMount(True)
            page_widget.setMountPoint(path)
            page_widget.setFilesystem(fsType)
            page_widget.setOptions(options)
        else:
            page_widget.setAutoMount(False)

        dialog.addPage(page_item)
        if dialog.exec_():
            device = widget.getId()
            if widget.getId() in self.device_entries:
                device = self.device_entries[device]
            if page_widget.getAutoMount():
                self.iface.addEntry(device, page_widget.getMountPoint(), page_widget.getFilesystem(), page_widget.getOptions())
            else:
                self.iface.removeEntry(device)

    def slotItemDelete(self):
        """
            Delete button clicked.
        """
        widget = self.sender()

    def slotOpenEdit(self, action):
        """
            New button clicked, show edit box.
        """
        # Get item type to add/
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
        # User.Manager does not emit signals, refresh whole list.
        self.buildItemList()
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
