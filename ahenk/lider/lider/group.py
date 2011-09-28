#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Group dialog
"""

# Qt4 modules
from PyQt4 import QtGui
from PyQt4 import QtCore

# Generated UI module
from lider.ui_group import Ui_dialogGroup
from lider.helpers import i18n

i18n = i18n.i18n

class DialogGroup(QtGui.QDialog, Ui_dialogGroup):
    """
        Dialog for groups.

        Usage:
            dialog = DialogGroup(form)
            dialog.set_name("test1")
            if dialog.exec_():
                ...
    """

    def __init__(self, parent=None):
        """
            Constructor for dialog.

            Arguments:
                parent: Parent object
        """
        QtGui.QDialog.__init__(self, parent)

        # Members
        self.members = {}

        # People
        self.people = {}

        # Attach generated UI
        self.setupUi(self)

        # Name must be alphanumeric only
        validator = QtGui.QRegExpValidator(QtCore.QRegExp('^[a-zA-Z0-9_-]+$'), self)
        self.editName.setValidator(validator)

        # Events
        self.connect(self.pushAdd, QtCore.SIGNAL("clicked()"), self.__slotAddMember)
        self.connect(self.pushDelete, QtCore.SIGNAL("clicked()"), self.__slotRemoveMember)

    def get_name(self):
        """
            Returns name.
        """
        return str(self.editName.text())

    def set_name(self, user):
        """
            Sets user name.
        """
        self.editName.setText(user)
        self.editName.setEnabled(False)

    def get_description(self):
        """
            Returns LDAP attribute name.
        """
        return str(self.editDescription.text())

    def set_description(self, description):
        """
            Sets description.
        """
        self.editDescription.setText(unicode(description))

    def set_members(self, members):
        """
            Sets group members.
        """
        self.listMembers.clear()
        self.members = {}
        for member in members:
            name = member.split(",")[0].split("=")[1]
            self.members[name] = member
            self.listMembers.addItem(name)

    def set_people(self, people):
        """
            Sets available people
        """
        self.listPeople.clear()
        self.people = {}
        for person in people:
            name = person.split(",")[0].split("=")[1]
            if name in self.members:
                continue
            self.people[name] = person
            self.listPeople.addItem(name)

    def get_members(self):
        """
            Returns list of members.
        """
        members = []
        for index in range(self.listMembers.count()):
            item = self.listMembers.item(index)
            name = unicode(item.text())
            members.append(self.members[name])
        return members

    def __slotAddMember(self):
        """
        """
        index = self.listPeople.currentRow()
        if index >= 0:
            item = self.listPeople.takeItem(index)
            name = unicode(item.text())
            self.members[name] = self.people[name]
            self.listMembers.addItem(item)

    def __slotRemoveMember(self):
        """
        """
        index = self.listMembers.currentRow()
        if index >= 0:
            item = self.listMembers.takeItem(index)
            name = unicode(item.text())
            self.people[name] = self.members[name]
            self.listPeople.addItem(item)

    def accept(self):
        if not len(self.editName.text()):
            QtGui.QMessageBox.warning(self, i18n("Group"), i18n("Group name is missing"))
        elif len(self.get_members()) < 1:
            QtGui.QMessageBox.warning(self, i18n("Group"), i18n("There has to be at least one member."))
        else:
            QtGui.QDialog.accept(self)
