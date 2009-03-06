#/usr/bin/python
# -*- coding: utf-8 -*-

"""
Userdialog for Sahip
"""
from PyQt4 import QtCore, QtGui
from copy import deepcopy

from yali4.kahya import kahya

from sahip.sahiplib import User, getShadowed
from sahip.usergui import Ui_UserDialog

import gettext
__trans = gettext.translation('sahip', fallback=True)
_ = __trans.ugettext



class UserDialog(QtGui.QDialog):
    """A QDialog instance inheriting usergui.py"""
    def __init__(self, caller=None, user=None): #*args):
        # Initialization
        QtGui.QDialog.__init__(self, None)
        self.ui = Ui_UserDialog()
        self.ui.setupUi(self)
        
        # Parameters
        self.caller = caller
        self.backupUser = None
        
        if user:                                # If user is specified, we should be editing it.
            self.backupUser = deepcopy(user)    # Back it up in case user presses cancel after modifying.
            self.user = user
            self.editMode = True
        else:                                   # Else create a new user.
            self.user = User()                  # Empty user to be filled in.
            self.editMode = False
            self.backupUser = None              # Indicate this is a new user to slotCancel.
                
        self.currentWarnings = set()            # To keep the warning sentences in.        
        self.slotSwitchToNormal(True)           # Select plain password radio button.
        if user:                                
            self.loadUserInformation(user)      # Load user data if user is specified.
        
            
        self.connectSlots()                     # Connect signal-slot pairs.
        self.loadGroups()                       # Load the group list


        
    def connectSlots(self):
        """Connects signal-slots"""
        # When normal(plain) password radio button is selected:
        QtCore.QObject.connect(self.ui.normal, QtCore.SIGNAL("toggled(bool)"), self.slotSwitchToNormal)
        # When shadowed password radio button is selected:
        QtCore.QObject.connect(self.ui.shadowed, QtCore.SIGNAL("toggled(bool)"), self.slotSwitchToShadowed)
        # OK and Cancel Buttons
        QtCore.QObject.connect(self.ui.OK, QtCore.SIGNAL("clicked()"), self.slotOK)
        QtCore.QObject.connect(self.ui.Cancel, QtCore.SIGNAL("clicked()"), self.slotCancel)
        
        
    
    def slotSwitchToShadowed(self, choosen):
        """When shadowed option selected, enables shadowed LineEdit and
         disables normal LineEdit"""
        if choosen:
            self.ui.shadowedPassword.setEnabled(True)       # Enable shadowed line edit.
            self.shadowPassword()                           # Shadow he content of plain.
            self.ui.normalPassword.setDisabled(True)        # Disable normal line edit.
        
    def slotSwitchToNormal(self, choosen):
        """When plain option selected, enables plain LineEdit and
        disables shadowed LineEdit"""
        if choosen:
            self.ui.normalPassword.setEnabled(True)         # Enable normal line edit.
            self.ui.shadowedPassword.clear()                # Clear shadow line edit.
            self.ui.shadowedPassword.setDisabled(True)      # Disable shadowed line edit.
    
    def slotOK(self):
        """When clicked on OK, gathers information filled in the form,
        validates them and saves accordingly, closing the dialog."""
        self.gatherInformation()
        valid = self.checkAll()
        if valid:
            if self.editMode:
                self.saveUserInformation()
            else:
                self.saveNewUser()
            self.close()
    
        
    def slotCancel(self):
        """Closes the dialog, Restores the user if the OK button is not clicked.""" 
        if self.user.username != None and self.backupUser != None:    # Means self.user is changed.
            self.restoreUser()                          # Then restore backup
        # No restore required if there's no change.
        self.close()                                    # Close the window
        
    
    # --------------------------------------------
    # ----------- Uyarlanacak-----------
    def loadGroups(self):  
        """Loads all groups and checks the default or selected ones """        
        allGroups     = allGroupList()                  # Get the group list from OS
        self.ui.groupList.clear()                       # Clear group list.
        self.ui.groupList.insertItems(0, allGroups)     # Insert all the groups.
        self.ui.groupList.sortItems()                   # Sorts the list in ascending order

        # -------------------------
        # Define which groups to check
        if self.editMode:
            # If a user is specified, check its own groups.
            groupsToCheck = self.user.groups
        else:
            # If no user specified, check the default groups.
            groupsToCheck = kahya().defaultGroups
        
        # ------------------------- 
        # Iterate over the list items to check the selected/default ones.
        count = self.ui.groupList.count()
        for i in range(count):
            item = self.ui.groupList.item(i)
            # Set checkable (checkbox appears next)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)

            # Now check if needed.
            if str(item.text()) in groupsToCheck:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked) # Do not delete this!
       
        
        
        
    # -----------------------------------------------
    def updateWarningMessage(self):
        """Updates the warning message on the GUI with the warning messages."""
        self.ui.warningMessages.setText("<br/>".join(self.currentWarnings))
            
    def loadUserInformation(self, user):
        """Loads the infomation of the user specified into the form."""
        self.user = user
        
        self.ui.username.setText(user.username)
        self.ui.realName.setText(user.realName)
        self.ui.normalPassword.setText(user.normalPassword)
        self.ui.shadowedPassword.setText(user.shadowedPassword)
        
        if user.shadowedPassword:                                           # If shadowed is preferred,
            self.ui.shadowed.setChecked(True)                               # Check the shadowed option.
            self.slotSwitchToShadowed(True)                                 # Enable/disable stuff.
    
    def saveUserInformation(self):
        """Updates the information of a user on the UserHandler
        and AutoLoginHandler."""
        oldUsername = self.backupUser.username        
        # Update user list and autologin box.
        self.caller.UserHandler.updateItem(oldUsername, self.user.username, self.user)
        self.caller.AutoLoginHandler.removeItem(displayText = oldUsername)
        self.caller.AutoLoginHandler.addItem(self.user.username, self.user)
        
    def gatherGroups(self):
        """Sets the user's groups as the ones selected in the list."""
        # Gather the groups information
        userGroups = []
        count = self.ui.groupList.count()
        for i in range(count):                                              # Iterate over items
            item = self.ui.groupList.item(i)            
            if item.checkState() == QtCore.Qt.Checked:                      # If item is checked,
                userGroups.append(str(item.text()))                         # Add it to the list.
        
        self.user.groups = userGroups                                       # Update user's groups.
        
        
    
    def gatherInformation(self):
        """Updates user's information according to the form."""
        self.user.username = str(self.ui.username.text())                   # Update username
        self.user.realName = unicode(self.ui.realName.text())               # Update realname
        self.user.normalPassword = str(self.ui.normalPassword.text())       # Update Normal password
        self.user.shadowedPassword = str(self.ui.shadowedPassword.text())   # Update Shadowed password
        self.gatherGroups()                                                 # Update Groups
        if self.user.shadowedPassword:                                      # If shadowed
            self.user.shadowed = True                                       # Flag as shadowed
            
    def saveNewUser(self):
        """Inserts the recently created user into UserHandler and
        AutoLoginHandler."""
        self.caller.UserHandler.addItem(self.user.username, self.user)
        self.caller.AutoLoginHandler.addItem(self.user.username, self.user)

    def restoreUser(self):
        """Restores self.user's information from backed up user."""
        self.user.username = self.backupUser.username
        self.user.realName = self.backupUser.realName
        self.user.normalPassword = self.backupUser.normalPassword
        self.user.shadowedPassword = self.backupUser.shadowedPassword
        self.user.groups = self.backupUser.groups
        
    def checkUsername(self):
        """Checks if the username is valid or not."""
        if self.user.isUsernameValid():
            return True
        else:
            self.currentWarnings.add(_("Invalid username. Should include only [a-z][A-Z]_[0-9]"))
            return False
    
    def checkRealName(self):
        """Checks if the realName is valid or not."""
        if self.user.isRealNameValid():
            return True
        else:
            self.currentWarnings.add(_("Invalid real name. Can't have newline or : characters."))
            return False
        
    def checkPassword(self):
        """Checks if the password is valid or not."""
        if self.user.isPasswordValid():
            return True
        else:
            self.currentWarnings.add(_("Invalid password. Password should be at least 4 characters."))
            return False
    def checkExistingUser(self):
        """Checks if a user with the same name exists."""
        if (self.editMode and self.backupUser.username != self.user.username) or not self.editMode:
            if self.caller.UserHandler.hasItem(self.user.username) or self.user.username == "root":
                self.currentWarnings.add(_("There's another user with username %s") % self.user.username)
                return False
            else:
                return True
        else:
            # Assume user won't delete or open up another window while editing one user.
            return True
    def checkAll(self):
        """Performs all the checks and updates warning messages label on GUI."""
        self.currentWarnings.clear()
        a = self.checkUsername() 
        b = self.checkExistingUser() 
        c = self.checkRealName()
        d = self.checkPassword()
        if a and b and c and d:
            return True
        else:
            self.ui.warningMessages.setText("\n".join(self.currentWarnings))
            return False
        
    
    def shadowPassword(self):
        """Shadows the password from plain box to the shadowed box."""
        self.ui.shadowedPassword.setText(str(getShadowed(str(self.ui.normalPassword.text()))))
        
    def isShadowSelected(self):
        """Returns if shadowed option is selected."""
        return self.ui.shadowedPassword.isChecked()
    
    
def getListItems(listWidget):
    """Returns the items of a list in a string list format."""
    items = []
    for index in xrange(listWidget.count()):
        items.append(str(listWidget.item(index).text()))
    return items   
    
def allGroupList():
    """Returns all the group names from the system as a list."""
    # TODO: Might be dangerous if the generator system has extra groups.
    groupsIn = []
    f = open("/etc/group")
    for line in f:
        groupName = line.split(":")[0]
        groupsIn.append(groupName)
    return groupsIn
    
    
    
    
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    UserDia = UserDialog(None)
    UserDia.show()
    sys.exit(app.exec_())
    
