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
from usermanager.ui_edituser import Ui_EditUserWidget
from usermanager.ui_editgroup import Ui_EditGroupWidget

# Utilities
from usermanager.utility import nickGuess

# PolicyKit
import polkit


class PolicyItem(QtGui.QTreeWidgetItem):
    def __init__(self, parent, text, action_id):
        QtGui.QTreeWidgetItem.__init__(self, parent)
        self.action_id = action_id
        self.type = 0
        self.setText(0, text)
        self.setIcon(0, kdeui.KIcon("security-medium"))

    def getAction(self):
        return self.action_id

    def setType(self, type_):
        self.type = type_
        if type_ == -1:
            self.setIcon(0, kdeui.KIcon("security-low"))
        elif type_ == 0:
            self.setIcon(0, kdeui.KIcon("security-medium"))
        elif type_ == 1:
            self.setIcon(0, kdeui.KIcon("security-high"))

    def getType(self):
        return self.type


class EditUserWidget(QtGui.QWidget, Ui_EditUserWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        # List of unavailable nicks
        self.nicklist = []
        
        #Remove duplicate shells
        self.comboShell.setDuplicatesEnabled(False)

        # Build policy list
        self.buildPolicies()

        # Validators
        #self.lineUsername.setValidator(QtCore.QRegExpValidator(QtCore.QRegExp("[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_]*"), self.lineUsername))
        #self.lineFullname.setValidator(QtCore.QRegExpValidator(QtCore.QRegExp("[^\n:]*"), self.lineFullname))

        # Warning icon
        self.labelSign.setPixmap(kdeui.KIcon("process-stop").pixmap(32, 32))
        self.labelSign.hide()

        # Signals
        self.connect(self.checkAutoId, QtCore.SIGNAL("stateChanged(int)"), self.slotCheckAuto)
        self.connect(self.lineUsername, QtCore.SIGNAL("textEdited(const QString&)"), self.slotUsernameChanged)
        self.connect(self.lineFullname, QtCore.SIGNAL("textEdited(const QString&)"), self.slotFullnameChanged)
        self.connect(self.listGroups, QtCore.SIGNAL("itemClicked(QListWidgetItem*)"), self.slotGroupSelected)
        self.connect(self.treeAuthorizations, QtCore.SIGNAL("currentItemChanged(QTreeWidgetItem*, QTreeWidgetItem*)"), self.slotPolicySelected)
        self.connect(self.radioAuthNo, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.radioAuthDefault, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.radioAuthYes, QtCore.SIGNAL("toggled(bool)"), self.slotPolicyChanged)
        self.connect(self.checkAdmin, QtCore.SIGNAL("stateChanged(int)"), self.slotAdmin)
        self.connect(self.pushAuth, QtCore.SIGNAL("clicked()"), self.slotAuth)
        self.connect(self.pushAdvanced, QtCore.SIGNAL("clicked()"), self.slotOpenAdvanced)

        self.connect(self.lineFullname, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.linePassword, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.linePasswordAgain, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.lineUsername, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.lineHomeDir, QtCore.SIGNAL("textEdited(const QString&)"), self.checkFields)
        self.connect(self.comboShell, QtCore.SIGNAL("currentIndexChanged(int)"), self.slotShellChanged)

    def reset(self):
        self.setId(-1)
        self.setUsername("")
        self.setFullname("")
        self.setHomeDir("")
        self.setPassword()
        self.lineUsername.setEnabled(True)
        self.lineHomeDir.setEnabled(True)
        self.groupBox_2.setVisible(False)

    def buildPolicies(self):
        self.actionItems = {}
        for action_id in polkit.action_list():
            if action_id.startswith("tr.org.pardus.comar."):
                info = polkit.action_info(action_id)
                item = PolicyItem(self.treeAuthorizations, unicode(info["description"]), action_id)
                self.actionItems[action_id] = item

    def getAuthorizations(self):
        grant = []
        revoke = []
        block = []
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            item = self.treeAuthorizations.topLevelItem(index)
            if item.getType() == -1:
                block.append(item.getAction())
            elif item.getType() == 0:
                revoke.append(item.getAction())
            elif item.getType() == 1:
                grant.append(item.getAction())
        return grant, revoke, block

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
        str(self.comboShell.itemData(self.comboShell.currentIndex()).toString())

    def getShell(self):
        return str(self.comboShell.itemData(self.comboShell.currentIndex()).toString())

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

    def setAuthorizations(self, authorizations):
        for action_id in self.actionItems:
            item = self.actionItems[action_id]
            item.setType(0)
        #print "\n Authorizations: %s " %authorizations
        for action_id, scope, description, policy_active, negative in authorizations:
            if action_id in self.actionItems:
                item = self.actionItems[action_id]
                if scope == negative:
                    item.setType(1)
                elif scope == polkit.SCOPE_ALWAYS:
                    item.setType(-1)

    def slotCheckAuto(self, state):
        if state == QtCore.Qt.Checked:
            self.spinId.setEnabled(False)
            self.spinId.setValue(-1)
        else:
            self.spinId.setEnabled(True)

    def slotOpenAdvanced(self):
        if self.groupBox_2.isVisible():
            self.groupBox_2.setVisible(False)
        else:
            self.groupBox_2.setVisible(True)

    def slotAuth(self):
        if self.radioAuthNo.isChecked():
            type_ = -1
        elif self.radioAuthDefault.isChecked():
            type_ = 0
        elif self.radioAuthYes.isChecked():
            type_ = 1
        for index in xrange(self.treeAuthorizations.topLevelItemCount()):
            item = self.treeAuthorizations.topLevelItem(index)
            item.setType(type_)

    def slotFullnameChanged(self, name):
        if self.lineUsername.isEnabled() and not self.lineUsername.isModified():
            self.lineUsername.setText(nickGuess(name, self.nicklist))
            if self.lineHomeDir.isEnabled() and not self.lineHomeDir.isModified():
                self.lineHomeDir.setText("/home/%s" % self.lineUsername.text())

    def slotUsernameChanged(self, name):
        if self.lineHomeDir.isEnabled() and not self.lineHomeDir.isModified():
            self.lineHomeDir.setText("/home/%s" % self.lineUsername.text())

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

    def slotPolicySelected(self, item, previous):
        if not item:
            return
        self.radioAuthNo.setChecked(item.getType() == -1)
        self.radioAuthDefault.setChecked(item.getType() == 0)
        self.radioAuthYes.setChecked(item.getType() == 1)

    def slotPolicyChanged(self, state):
        item = self.treeAuthorizations.currentItem()
        if self.radioAuthNo.isChecked():
            item.setType(-1)
        elif self.radioAuthDefault.isChecked():
            item.setType(0)
        elif self.radioAuthYes.isChecked():
            item.setType(1)

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

    def listShells(self):
        shells = open('/etc/shells','r') 
        line = shells.readline()
        while line :
            line = shells.readline()
            self.comboShell.addItem(line)
        shells.close()

    def slotShellChanged(self):
        index = self.comboShell.currentIndex()

    def checkFields(self, *args):
        err = ""
        i18n = kdecore.i18n

        if self.lineFullname.text() == "" and self.lineUsername.text() == "":
            err = i18n("Start with typing this user's full name.")

        if not err and self.isNew() and self.linePassword.text() == "":
            err = i18n("You should enter a password for this user.")

        if not err:
            pw = unicode(self.linePassword.text())
            if pw != "" and len(pw) < 4:
                err = i18n("Password must be longer.")

            if not err:
                if len(pw) and pw == self.lineFullname.text() or pw == self.lineUsername.text():
                    err = i18n("Don't use your full name or user name as a password.")

        if not err and self.linePassword.text() != self.linePasswordAgain.text():
            err = i18n("Passwords don't match.")

        nick = self.lineUsername.text()

        if not err and nick == "":
            err = i18n("You must enter a user name.")

        if not err and self.isNew() and nick in self.nicklist:
            err = i18n("This user name is used by another user.")

        if not err:
            if len(nick) > 0 and nick[0] >= "0" and nick[0] <= "9":
                err = i18n("User name must not start with a number.")

        if err:
            self.labelWarning.setText(u"<font color=red>%s</font>" % err)
            self.labelSign.show()
            self.emit(QtCore.SIGNAL("buttonStatusChanged(int)"),0)

        else:
            self.labelWarning.setText("")
            self.labelSign.hide()
            self.emit(QtCore.SIGNAL("buttonStatusChanged(int)"),1)

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
