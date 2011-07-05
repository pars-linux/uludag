#!/usr/bin/python
# -*- coding: utf-8 -*-

"""The utils library for Sahip. Includes some Handlers and the User Class."""


from string import ascii_letters, digits
from PyQt4 import QtGui, QtCore
from copy import deepcopy
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
        """Returns the information list in the dictionary"""
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
        
    def hasItem(self, displayText):
        """Checks if the handler has an item with specified displayText."""
        return displayText in self.dict
    
    def isAnySelected(self):
        """Checks if any item is selected in the list."""
        index = self.widget.currentRow()       # Find the index of selected user.
        if index == -1:                             # If no user is selected,
            return False
        return True
    def removeCurrentItem(self):
        """Removes the current selected item from both the widget and the internal dictionary.
        Returns the text of removed item or -1 if no item is selected."""
        if not self.isAnySelected():
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
    #TODO: ?????? No findText function for QListWidget?!!!!!
    def findItems(self, displayText):
        """Finds items with the displayText."""
        return self.widget.findItems(unicode(displayText), QtCore.Qt.MatchExactly)
    
    def getSelectedInformation(self):
        """Returns the information belonging to the selected item"""
        if self.isAnySelected():
            return self.getInformation(unicode(self.widget.currentItem().text()))
        else:
            return None
    
    def getSelectedDisplayText(self):
        """Returns the display text beloging to the selected item."""
        return unicode(self.widget.currentText())
    
    def unSelect(self):
        self.widget.setCurrentRow(-1) 
        
    def updateItem(self, oldText, newText, newInformation):        
        currentInformation = deepcopy(newInformation)
        # TODO: Change this, delete according to oldText.
        self.removeCurrentItem() #Dangerous but workaround
        self.addItem(newText, newInformation)
        
        
                
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
    def __init__(self, username=None, realName=None, normalPassword=None, shadowedPassword=None, groups=None):
        """Initialize with the information from the form. Autologin is disabled by default."""
        self.username = username
        self.realName = realName
        self.normalPassword = normalPassword
        self.shadowedPassword = shadowedPassword
        self.groups = groups
        self.autologin = False
        
        if shadowedPassword:
            self.shadowed = True
        else:
            self.shadowed = False
    
    def isPasswordValid(self):
        """Checks if the password is at least 4 characters."""
        if self.shadowedPassword:
            return len(self.shadowedPassword) == 34
        else:
            return len(self.normalPassword) >=4
    
    def isUsernameValid(self):
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

    def isRealNameValid(self):
        """Checks if the realname is valid or not (excluding newline and colon characters)"""
        not_allowed_chars = '\n' + ':'
        return '' == filter(lambda r: [x for x in not_allowed_chars if x == r], self.realName)

# Borrowed from yali4 v2.0.1 to be able to work with v2.0.0
import random, md5

def getShadowed(passwd):
    des_salt = list('./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') 
    salt, magic = str(random.random())[-8:], '$1$'

    ctx = md5.new(passwd)
    ctx.update(magic)
    ctx.update(salt)

    ctx1 = md5.new(passwd)
    ctx1.update(salt)
    ctx1.update(passwd)

    final = ctx1.digest()

    for i in range(len(passwd), 0 , -16):
        if i > 16:
            ctx.update(final)
        else:
            ctx.update(final[:i])

    i = len(passwd)

    while i:
        if i & 1:
            ctx.update('\0')
        else:
            ctx.update(passwd[:1])
        i = i >> 1
    final = ctx.digest()

    for i in range(1000):
        ctx1 = md5.new()
        if i & 1:
            ctx1.update(passwd)
        else:
            ctx1.update(final)
        if i % 3: ctx1.update(salt)
        if i % 7: ctx1.update(passwd)
        if i & 1:
            ctx1.update(final)
        else:
            ctx1.update(passwd)
        final = ctx1.digest()

    def _to64(v, n):
        r = ''
        while (n-1 >= 0):
            r = r + des_salt[v & 0x3F]
            v = v >> 6
            n = n - 1
        return r

    rv = magic + salt + '$'
    final = map(ord, final)
    l = (final[0] << 16) + (final[6] << 8) + final[12]
    rv = rv + _to64(l, 4)
    l = (final[1] << 16) + (final[7] << 8) + final[13]
    rv = rv + _to64(l, 4)
    l = (final[2] << 16) + (final[8] << 8) + final[14]
    rv = rv + _to64(l, 4)
    l = (final[3] << 16) + (final[9] << 8) + final[15]
    rv = rv + _to64(l, 4)
    l = (final[4] << 16) + (final[10] << 8) + final[5]
    rv = rv + _to64(l, 4)
    l = final[11]
    rv = rv + _to64(l, 2)

    return rv
