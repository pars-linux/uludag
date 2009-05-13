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
from ui_edituser import Ui_EditUserWidget
from ui_editgroup import Ui_EditGroupWidget

# Utilities
from utility import nickGuess

# PolicyKit
import polkit


class EditUserWidget(QtGui.QWidget, Ui_EditUserWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # List of unavailable nicks
        self.nicklist = []

        # Build policy list
        self.buildPolicies()

        self.connect(self.checkAutoId, QtCore.SIGNAL("stateChanged(int)"), self.slotCheckAuto)
        self.connect(self.lineFullname, QtCore.SIGNAL("textEdited(const QString&)"), self.slotFulnameChanged)
        self.connect(self.listGroups, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.slotGroupSelected)
        self.connect(self.checkAdmin, QtCore.SIGNAL("stateChanged(int)"), self.slotAdmin)

    def reset(self):
        self.setId(-1)
        self.setUsername("")
        self.setFullname("")
        self.setHomeDir("")
        self.setShell("")
        self.setPassword()
        self.lineUsername.setEnabled(True)
        self.lineHomeDir.setEnabled(True)

    def buildPolicies(self):
        for action_id in polkit.action_list():
            if action_id.startswith("tr.org.pardus.comar."):
                info = polkit.action_info(action_id)
                item = QtGui.QTreeWidgetItem(self.treeAuthorizations)
                item.setText(0, unicode(info["description"]))

    def isNew(self):
        return self.spinId.isEnabled() or self.checkAutoId.isVisible()

    def getId(self):
        if self.checkAutoId.checkState() == QtCore.Qt.Checked:
            return -1
        return int(self.spinId.value())

    def setId(self, id):
        if id != -1:
            self.checkAutoId.setCheckState(QtCore.Qt.Unchecked)
            self.checkAutoId.hide()
            self.spinId.setEnabled(False)
        else:
            self.checkAutoId.setCheckState(QtCore.Qt.Checked)
            self.checkAutoId.show()
            self.spinId.setEnabled(False)
        self.spinId.setValue(id)

    def setNickList(self, nicklist):
        self.nicklist = nicklist

    def getUsername(self):
        return unicode(self.lineUsername.text())

    def setUsername(self, username):
        self.lineUsername.setText(unicode(username))
        self.lineUsername.setEnabled(False)

    def getFullname(self):
        return unicode(self.lineFullname.text())

    def setFullname(self, fullname):
        self.lineFullname.setText(unicode(fullname))

    def setHomeDir(self, homedir):
        self.lineHomeDir.setText(unicode(homedir))
        self.lineHomeDir.setEnabled(False)

    def getHomeDir(self):
        return unicode(self.lineHomeDir.text())

    def setShell(self, shell):
        self.lineShell.setText(unicode(shell))

    def getShell(self):
        return unicode(self.lineShell.text())

    def setPassword(self):
        self.linePassword.setText("")
        self.linePasswordAgain.setText("")

    def getPassword(self):
        if self.linePassword.isModified() and self.linePassword.text() == self.linePasswordAgain.text():
            return unicode(self.linePassword.text())
        return ""

    def setGroups(self, all_groups, selected_groups):
        self.listGroups.clear()
        self.comboMainGroup.clear()
        for group in all_groups:
            # Groups
            item = QtGui.QListWidgetItem(self.listGroups)
            item.setText(group)
            if group in selected_groups:
                item.setCheckState(QtCore.Qt.Checked)
                # Add selected items to main group combo
                self.comboMainGroup.addItem(group)
                # Wheel group?
                if group == "wheel":
                    self.checkAdmin.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)
        # Select main group
        if selected_groups:
            self.comboMainGroup.setCurrentIndex(self.comboMainGroup.findText(selected_groups[0]))

    def getGroups(self):
        groups = []
        for index in range(self.listGroups.count()):
            item = self.listGroups.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                groups.append(unicode(item.text()))
        # Main group
        main_group = unicode(self.comboMainGroup.currentText())
        groups.remove(main_group)
        groups.insert(0, main_group)
        return groups

    def slotCheckAuto(self, state):
        if state == QtCore.Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)

    def slotFulnameChanged(self, name):
        if self.lineUsername.isEnabled() and not self.lineUsername.isModified():
            self.lineUsername.setText(nickGuess(name, self.nicklist))

    def checkLastItem(self):
        if self.comboMainGroup.count() == 1:
            kdeui.KMessageBox.error(self, kdecore.i18n("There has to be at least one group selected."))
            return False
        return True

    def slotGroupSelected(self):
        item = self.listGroups.currentItem()
        if item.checkState() == QtCore.Qt.Unchecked:
            # You can't remove last item
            if not self.checkLastItem():
                item.setCheckState(QtCore.Qt.Checked)
                return
            # Remove from main group combo
            index = self.comboMainGroup.findText(item.text())
            self.comboMainGroup.removeItem(index)
            # Wheel group?
            if item.text() == "wheel":
                self.checkAdmin.setCheckState(QtCore.Qt.Unchecked)
        else:
            # Add to main group combo
            self.comboMainGroup.addItem(item.text())
            # Wheel group?
            if item.text() == "wheel":
                self.checkAdmin.setCheckState(QtCore.Qt.Checked)

    def slotAdmin(self, state):
        if state == QtCore.Qt.Unchecked:
            # You can't remove last item
            if not self.checkLastItem():
                self.checkAdmin.setCheckState(QtCore.Qt.Checked)
                return
            # Remove from main group combo
            self.comboMainGroup.removeItem(self.comboMainGroup.findText("wheel"))
        else:
            # Add to combo
            if self.comboMainGroup.findText("wheel") < 0:
                self.comboMainGroup.addItem("wheel")
        # Update group list
        for index in range(self.listGroups.count()):
            item = self.listGroups.item(index)
            if item.text() == "wheel":
                # Change check state
                item.setCheckState(state)
                return

class EditGroupWidget(QtGui.QWidget, Ui_EditGroupWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.connect(self.checkAutoId, QtCore.SIGNAL("stateChanged(int)"), self.slotCheckAuto)

    def reset(self):
        self.setId(-1)
        self.setGroupname("")

    def getId(self):
        if self.checkAutoId.checkState() == QtCore.Qt.Checked:
            return -1
        return int(self.spinId.value())

    def setId(self, id):
        if id != -1:
            self.checkAutoId.setCheckState(QtCore.Qt.Unchecked)
            self.checkAutoId.hide()
            self.spinId.setEnabled(False)
        else:
            self.checkAutoId.setCheckState(QtCore.Qt.Checked)
            self.checkAutoId.show()
            self.spinId.setEnabled(False)
        self.spinId.setValue(id)

    def getGroupname(self):
        return unicode(self.lineGroupname.text())

    def setGroupname(self, groupname):
        self.lineGroupname.setText(unicode(groupname))

    def slotCheckAuto(self, state):
        if state == QtCore.Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)
