#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main file for sahip. Controls the signals and includes the logic."""

# Qt4 Stuff
from PyQt4 import QtCore, QtGui

# Required modules within the project.
from sahipcore import User, ComboBoxHandler, ListHandler
from sahipgui import Ui_Sahip
from sahipgen import SahipGenerator

# The modules borrowed from yali and kahya.
from yali4.kahya import kahya
from yali4.localedata import locales
from yali4.constants import consts
from yali4.sysutils import TimeZoneList, getShadowed, text_is_valid

# We need these for i18n.
import gettext
__trans = gettext.translation('sahip', fallback=True)
_ = __trans.ugettext


class SahipWidget(QtGui.QWidget):
    """Uses sahipgui module and defines slots and operations on it."""
    def __init__(self, *args):
        """Sets ui from sahipgui; calls connectSlots, createHandlers and
         setDefaults."""
        QtGui.QWidget.__init__(self, None)
        self.ui = Ui_Sahip()
        self.ui.setupUi(self)
        
        self.createHandlers()
        self.connectSlots()
        self.setDefaults()
        
    
           
    def connectSlots(self):
        """Connects the slots for the events."""
        QtCore.QObject.connect(self.ui.languageBox,QtCore.SIGNAL("currentIndexChanged(QString)"), self.slotLanguageChanged)
        QtCore.QObject.connect(self.ui.groupAdd, QtCore.SIGNAL("clicked()"), self.slotGroupAdd)
        QtCore.QObject.connect(self.ui.groupDelete, QtCore.SIGNAL("clicked()"), self.slotGroupDelete)
        QtCore.QObject.connect(self.ui.userAdd, QtCore.SIGNAL("clicked()"), self.slotUserAdd)
        QtCore.QObject.connect(self.ui.userDelete, QtCore.SIGNAL("clicked()"), self.slotUserDelete)       
        QtCore.QObject.connect(self.ui.shadowButton, QtCore.SIGNAL("clicked()"), self.slotShadow)
        QtCore.QObject.connect(self.ui.generateXMLButton, QtCore.SIGNAL("clicked()"), self.slotGenerateXML)
        QtCore.QObject.connect(self.ui.groupsIn, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.slotGroupDelete)
        QtCore.QObject.connect(self.ui.groupsOut, QtCore.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.slotGroupAdd)
        QtCore.QObject.connect(self.ui.clearButton, QtCore.SIGNAL("clicked()"), self.slotClear)
        QtCore.QObject.connect(self.ui.userList, QtCore.SIGNAL("itemPressed(QListWidgetItem*)"), self.slotUserClicked)
        QtCore.QObject.connect(self.ui.newUser, QtCore.SIGNAL("clicked()"), self.slotNewUser)
                
    def createHandlers(self):
        """Creates handlers """
        self.LanguageHandler = ComboBoxHandler(self.ui.languageBox, sorted=True)
        self.VariantHandler = ComboBoxHandler(self.ui.variantBox, sorted=True)
        self.TimeZoneHandler = ComboBoxHandler(self.ui.timeZone, sorted=True)
        self.UserHandler = ListHandler(self.ui.userList, sorted=True)
        self.AutoLoginHandler = ComboBoxHandler(self.ui.autologinUserBox, sorted=True)
        self.PartitionHandler = ComboBoxHandler(self.ui.partitioningTypeBox, sorted=False)
    
    def slotUserClicked(self):
        userTD = self.UserHandler.getSelectedInformation()
        self.ui.username.setText(userTD.username)
        self.ui.realname.setText(userTD.realname)
        self.ui.password1.setText(userTD.password)
        self.ui.password2.setText(userTD.password)
        #self.ui.
        
    
    def slotClear(self):
        """Sets the defaults for the widgets in the form."""
        self.setDefaults()
    
    def slotShadow(self):
        """Crypts the password entered in a dialog and puts it into the root password field."""        
        inputPass = QtGui.QInputDialog.getText(self, _('Enter the root password to be shadowed'), _('Password:'), QtGui.QLineEdit.Normal)
        if inputPass[0]:
            cryptedPass = getShadowed(str(inputPass[0]))
            self.ui.rootPassword.setText(cryptedPass)
            
    def slotUserAdd(self):
        """Adds a new user with the information filled in the form to the list (of course, with validation)."""
        if self.ui.password1.text() != self.ui.password2.text():
            QtGui.QMessageBox.question(self, _('Error'),_('The Passwords do not match.'), QtGui.QMessageBox.Ok)
        else: 
            newuser = User(unicode(self.ui.username.text()), unicode(self.ui.realname.text()), unicode(self.ui.password1.text()), self.getListItems(self.ui.groupsIn))
            
            if not newuser.isUsernameValid():
                QtGui.QMessageBox.question(self, _('Error'),_('Invalid username. Should include only [a-z][A-Z]_[0-9]'), QtGui.QMessageBox.Ok)
                del newuser
                return
            if not newuser.isRealnameValid():
                QtGui.QMessageBox.question(self, _('Error'),_('Invalid real name. Can\'t have newline or : characters.'), QtGui.QMessageBox.Ok)
                del newuser
                return
            if not newuser.isPasswordValid():
                QtGui.QMessageBox.question(self, _('Error'),_('Invalid password. Password should be at least 4 characters.'), QtGui.QMessageBox.Ok)
                del newuser
                return
            if self.isUserAlreadyAdded(newuser.username):
                QtGui.QMessageBox.question(self, _('Error'),_('There\'s another user with username %s.') % newuser.username, QtGui.QMessageBox.Ok)
                del newuser
                return
            
            self.UserHandler.addItem(newuser.username, newuser)
            self.AutoLoginHandler.addItem(newuser.username, newuser)
            self.slotNewUser()
            
    def slotNewUser(self):
            itemsToBeCleared = [ self.ui.username,
                                 self.ui.realname,
                                 self.ui.password1,
                                 self.ui.password2,
                                 self.ui.groupsIn,
                                 self.ui.groupsOut
                                 ]
            for item in itemsToBeCleared: item.clear()
            self.loadGroups()
            self.UserHandler.unSelect()                   
        
    def slotUserDelete(self):
        """Deletes the selected user from the list."""
        username = self.UserHandler.removeCurrentItem()
        if  username == -1:                             # If no user is selected,
            QtGui.QMessageBox.question(self, _('Error'),_('No user selected.'), QtGui.QMessageBox.Ok)
        elif username:
            self.AutoLoginHandler.removeItem(displayText = username) # Remove the username from the autologinUserBox.

    def slotGroupAdd(self):
        """Moves the group selected from groupsOut into groupsIn."""
        index = self.ui.groupsOut.currentRow()
        if index == -1:
            QtGui.QMessageBox.question(self, _('Error'),_('No group selected.'), QtGui.QMessageBox.Ok)
            return
        item = self.ui.groupsOut.takeItem(index)
        self.ui.groupsIn.insertItem(0, item)
        del item
        self.ui.groupsIn.sortItems()
        
    def slotGroupDelete(self):
        """Moves the group selected from groupsIn into groupsOut."""
        index = self.ui.groupsIn.currentRow()
        if index == -1:
            QtGui.QMessageBox.question(self, _('Error'),_('No group selected.'), QtGui.QMessageBox.Ok)
            return
        item = self.ui.groupsIn.takeItem(index)
        self.ui.groupsOut.insertItem(0, item)
        del item
        self.ui.groupsOut.sortItems()
        
        

    def slotLanguageChanged(self, newLanguage):
        """Retrieves information about the newLanguage and updates the variantBox accordingly.
        If the variant is a list, adds each variant to the variantBox
        If the variant is None, adds nothing to the variantBox.
        """
        if not newLanguage:
            return
        self.localeData = locales[self.LanguageHandler.getInformation(unicode(newLanguage))]
        variants = self.localeData['xkbvariant']
        # --------------------------------------------------------------------        
        # Update the xkbvariant combobox according to the language selected.
        # --------------------------------------------------------------------
        self.VariantHandler.clear()
        
        # If there are multiple variants,
        if isinstance(variants, list):
            # "xkbvariant" : [["f",_("Turkish F")],["",_("Turkish Q")]],
            for variant in variants:
                self.VariantHandler.addItem(variant[1], variant[0])
        # If the language doesn't have any variant
        elif variants == None:              
            pass
        # If something different, raise Exception.            
        else:
            raise Exception
        # ---------------------------------------------------------------------
    
    def slotGenerateXML(self):
        """Generates XML File with the informatio gathered from the form."""
        if not self.isHostNameValid():
            QtGui.QMessageBox.question(self, _('Error'),_('Invalid hostname. Hostname can only include ASCII characters.'), QtGui.QMessageBox.Ok)
            return 
        if not User(None, None, self.ui.rootPassword.text(), None).isPasswordValid():
            QtGui.QMessageBox.question(self, _('Error'),_('Invalid root password. Root password should be at least 4 characters.'), QtGui.QMessageBox.Ok)
            return
        for user in self.UserHandler.getInformationList():
            if user.username == self.AutoLoginHandler.getSelectedDisplayText():
                user.autologin = True
        variantDisplayText = unicode(self.ui.variantBox.currentText())
        if variantDisplayText:
            variantInformation = self.VariantHandler.getInformation(variantDisplayText)
        else:
            variantInformation = None
            
        #a = QtGui.QApplication([])
        filename = QtGui.QFileDialog.getSaveFileName()
        if not filename:
            return
        
        sg = SahipGenerator(filename = filename,\
                            language = self.LanguageHandler.getSelectedInformation(),\
                             variant = self.VariantHandler.getSelectedInformation(),\
                       root_password = str(self.ui.rootPassword.text()),\
                            timezone = str(self.ui.timeZone.currentText()),\
                            hostname = str(self.ui.hostname.text()),\
                               users = self.UserHandler.getInformationList(),\
                            reponame = str(self.ui.repoName.text()),\
                            repoaddr = str(self.ui.repoAddress.text()),\
                   partitioning_type = self.PartitionHandler.getSelectedInformation(),\
                                disk = str(self.ui.disk.text())
                        )
        result = sg.generate()
        if result['status']:
            QtGui.QMessageBox.question(self, _('Successful'),_('The XML File has been saved to %s.') % result['filename'], QtGui.QMessageBox.Ok)
        else:
            QtGui.QMessageBox.question(self, _('Error'),_('Could not save the XML File to %s.') % result['filename'], QtGui.QMessageBox.Ok)
    # ------------------SLOTS END---------------------------------------------
    
    def isHostNameValid(self):
        """Checks if hostname is valid."""
        hostname = self.ui.hostname.text().toAscii()
        if hostname:
            return text_is_valid(hostname)
        else:
            return False
    
    def loadPersonalDefaults(self):
        """Loads test information."""
        self.ui.rootPassword.setText("testroot")
        self.ui.hostname.setText("pardus-pc")
        self.ui.username.setText("pars")
        self.ui.realname.setText( "Pardus Pantheras")
        self.ui.password1.setText("pardons")
        self.ui.password2.setText("pardons")        
        
    def setDefaults(self):
        """Sets defaults for all items in the form.""" 
        # ------ Clear Combobox and Lists -------
        itemsToBeCleared = [ self.ui.groupsIn,
                            self.ui.groupsOut,
                            self.UserHandler,
                            self.LanguageHandler,
                            self.VariantHandler,
                            self.TimeZoneHandler,
                            self.PartitionHandler
                            ]
        for item in itemsToBeCleared: item.clear()
        
        self.loadLanguages()
        self.loadTimeZones()
        self.loadGroups()
        self.loadPartitioningTypes()
        self.loadRepoSettings()
        
        # Should be commented below when releasing.
        # self.loadPersonalDefaults()
        
    def loadLanguages(self):
        """Loads languages from the locales module of yali into the Language Combobox."""
        # ------ Load languages -------
        for abbr in locales.keys():
            self.LanguageHandler.addItem(locales[abbr]['name'], abbr)
                    
        self.LanguageHandler.selectItem("tr")
        self.VariantHandler.selectItem("")
        # -----------------------------
    def loadTimeZones(self):
        """Loads Time Zones from the sysutils module of yali into the Language Combobox.""" 
        for tz in TimeZoneList().getEntries():
            self.TimeZoneHandler.addItem(tz.timeZone, tz.code)
            
        self.TimeZoneHandler.selectItem("TR")
        
    def loadGroups(self):  
        """Loads default groups (from kahya) to groupsIn and all other available groups to groupsOut."""
        # ------ Load Groups ----------        
        # Default Groups to groupsIn
        self.ui.groupsIn.insertItems(0, kahya().defaultGroups)
        # Other groups to groupsOut
        self.ui.groupsOut.insertItems(0, list(set(self.allGroupList()) - set(self.getListItems(self.ui.groupsIn))))
        self.ui.groupsOut.sortItems()        
        # ----------------------------
        
    def loadPartitioningTypes(self):
        """Loads the partitioning types into the partitioning type combobox"""     
        self.PartitionHandler.addItem(_('Automatic Partitioning'), 'auto')
        self.PartitionHandler.addItem(_('Smart Automatic Partitioning'), 'smartAuto')
        self.PartitionHandler.addItem(_('Manuel Partitioning'), 'manuel')
        self.PartitionHandler.selectItem('smartAuto')
        self.ui.disk.setText('disk0')
        # --------------------------------------
    def loadRepoSettings(self):        
        """Loads the default repo name and address."""
        self.ui.repoName.setText(consts.pardus_repo_name)
        self.ui.repoAddress.setText(consts.pardus_repo_uri)        

        
    def isUserAlreadyAdded(self, username):
        """Checks if the userList has a user with the same username as given.""" 
        if self.UserHandler.getInformation(username):
            return True
        return False
        
    def allGroupList(self):
        """Returns all the group names from the system as a list."""
        # TODO: Might be dangerous if the generator system has extra groups.
        groupsIn = []
        f = open("/etc/group")
        for line in f:
            groupName = line.split(":")[0]
            groupsIn.append(groupName)
        return groupsIn
    
    def getListItems(self, listWidget):
        """Returns the items of a list in a string list format."""
        items = []
        for index in xrange(listWidget.count()):
            items.append(str(listWidget.item(index).text()))
        return items   
        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Sahip = SahipWidget()
    Sahip.show()
    sys.exit(app.exec_())
