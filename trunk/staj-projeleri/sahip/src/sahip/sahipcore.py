#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The utils library for Sahip. Includes some Handlers and the User Class."""


from string import ascii_letters, digits
from PyQt4 import QtGui

import gettext
__trans = gettext.translation('sahip', fallback=True)
_ = __trans.ugettext

    
class WidgetHandler:
    """Handler for add/remove object operations for a Qt4 Widget.
    Use it when you need to store more information in a Widget.
    Information can be any object: String or Object type.
    """
    
    def __init__(self, widget, sorted=True):
        """Initializes the WidgetHandler class with the given widget and the sorting option"""
        self.dict = {}
        self.widget = widget
        self.sorted = sorted

        
    def getInformation(self, displayText):
        """Returns the information corresponding to the given displayText."""
        return self.dict.get(displayText)
    
    def getInformationList(self):
        return self.dict.values()
    
    def getDisplayText(self, information):
        """Returns displayText corresponding to the given information."""
        for displayText in self.dict:
            if self.dict.get(displayText) == information:
                return displayText
        return None
        
    def getDisplayTextList(self):
        """Returns all the displayTexts belonging to the handler"""
        return self.dict.keys()
    
    def addItem(self, displayText, information):
        """Adds a new item to the widget, with key displayText and value information pair.""" 
        self.dict[displayText] = information
        self.widget.addItem(displayText)
        if self.sorted:
            self.sort()
            
    def addItems(self, itemTuple):
        """Receives parameter itemTuple in the form of ((display1, info1), (display2, info2), ... ) and adds them"""
        for subTuple in itemTuple:
            self.addItem(subTuple[0], subTuple[1])
        if self.sorted:
            self.sort()
    
            
    def clear(self):
        """Clears the internal dictionary and the contents of the widget."""
        self.widget.clear()
        self.dict = {}

class ListHandler(WidgetHandler):
    """Handler for specifically QListWidget. Has special list functionality implementations."""
    def __init__(self, listWidget, sorted=True):
        """Initializes the List Handler with given List Widget and sorting option."""
        WidgetHandler.__init__(self, listWidget, sorted)
            
    def removeCurrentItem(self):
        """Removes the current selected item from both the widget and the internal dictionary.
        Returns the text of removed item or -1 if no item is selected."""
        index = self.widget.currentRow()       # Find the index of selected user.
        if index == -1:                             # If no user is selected,
            return -1
        currentText = str(self.widget.currentItem().text())
        currentItem = self.widget.takeItem(self.widget.currentRow())
        del currentItem
        del self.dict[currentText]
        return currentText
        
    def sort(self):
        """Sorts the list items."""
        self.widget.sortItems()
    
    # TODO: Select according to DisplayText?
    def selectItem(self, information):
        """Selects the item with given information"""
        displayText = self.getDisplayText(information)
        self.widget.setCurrentIndex(self.widget.findText(displayText))
        
    def getSelectedInformation(self):
        """Returns the information belonging to the selected item"""
        return self.getInformation(unicode(self.widget.currentText()))
    
    def getSelectedDisplayText(self):
        """Returns the display text beloging to the selected item."""
        return unicode(self.widget.currentText())
        
class ComboBoxHandler(WidgetHandler):
    """Handler for specifically QComboBox. Has special ComboBox functionality implementations."""
    def __init__(self, comboBoxWidget, sorted=True):
        """Initializes the ComboBox Handler with given ComboBox Widget and sorting option."""
        WidgetHandler.__init__(self, comboBoxWidget, sorted)
    
    def sort(self):
        """Sorts the combobox"""
        sortedModel = self.widget.model()
        sortedModel.sort(0)
    def selectItem(self, information):
        """Selects item according to given information"""
        displayText = self.getDisplayText(information)
        self.widget.setCurrentIndex(self.widget.findText(displayText))
        
    def getSelectedInformation(self):
        """Returns the information belonging to the selected item."""
        return self.getInformation(unicode(self.widget.currentText()))
    
    def getSelectedDisplayText(self):
        """Returns the displayText belonging to the selected item."""
        return unicode(self.widget.currentText())
    
    def removeItem(self, displayText=None, information=None):
        """Removes the item matching with the given parameters."""
        if displayText:
            if displayText in self.dict:
                self.widget.removeItem(self.widget.findText(displayText))
                del self.dict[displayText]

class User:
    """User class for validation utilities."""
    def __init__(self, username, realname, password, groups):
        """Initialize with the information from the form. Autologin is disabled by default."""
        self.username = username
        self.realname = realname
        self.password = password
        self.groups = groups
        self.autologin=False
    
    def passwordIsValid(self):
        """Checks if the password is at least 4 characters."""
        if len(self.password) < 4:
            return False
        else:
            return True
    
    def usernameIsValid(self):
        """Checks if the username is valid or not (including only ascii, "_", digits)."""
        valid = ascii_letters + '_' + digits
        name = self.username
        
        if len(name)==0:
            return False
        
        if name[0] not in ascii_letters:
            return False
        
        for letter in name:
            if letter not in valid:
                return False
        
        return True

    def realnameIsValid(self):
        """Checks if the realname is valid or not (excluding newline and colon characters)"""
        not_allowed_chars = '\n' + ':'
        return '' == filter(lambda r: [x for x in not_allowed_chars if x == r], self.realname)
