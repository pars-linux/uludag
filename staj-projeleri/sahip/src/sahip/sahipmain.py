#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from sahipcore import User, Partitioning
from sahipgui import Ui_Sahip
from sahipgen import SahipGenerator
from yali4.kahya import kahya
from yali4.localedata import locales
from yali4.constants import consts
from yali4.sysutils import TimeZoneList

import gettext
__trans = gettext.translation('sahip', fallback=True)
_ = __trans.ugettext

class SahipWidget(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, None)
        self.ui = Ui_Sahip()
        self.ui.setupUi(self)
        
        #Events
        QtCore.QObject.connect(self.ui.languageBox,QtCore.SIGNAL("currentIndexChanged(QString)"), self.languageChanged)
        QtCore.QObject.connect(self.ui.groupAdd, QtCore.SIGNAL("clicked()"), self.groupAddClicked)
        QtCore.QObject.connect(self.ui.groupDelete, QtCore.SIGNAL("clicked()"), self.groupDeleteClicked)
        QtCore.QObject.connect(self.ui.userAdd, QtCore.SIGNAL("clicked()"), self.userAddClicked)
        QtCore.QObject.connect(self.ui.userDelete, QtCore.SIGNAL("clicked()"), self.userDeleteClicked)       
        QtCore.QObject.connect(self.ui.shadowButton, QtCore.SIGNAL("clicked()"), self.shadowButtonClicked)
        QtCore.QObject.connect(self.ui.generateXMLButton, QtCore.SIGNAL("clicked()"), self.generateXMLButtonClicked)
        
        self.ui.rootPassword.setText("testroot")
        self.ui.hostname.setText("pardus-pc")
        self.ui.username.setText("emre")
        self.ui.realname.setText( "Emre Aladag")
        self.ui.password1.setText("test")
        self.ui.password2.setText("test")
        
        self.ui.disk.setText("disk0")
        
        
        #Events end
        self.users = []
        
        # Load languages
        languages = locales.keys()[:]
        languages.sort()
        self.ui.languageBox.insertItems(0, languages)
        self.ui.languageBox.setCurrentIndex(languages.index("tr"))
        self.languageChanged("tr")
               
        # Load Timezones
        zom = TimeZoneList()
        zoneList = [ x.timeZone for x in zom.getEntries() ]
        zoneList.sort()
        self.ui.timeZone.insertItems(0, zoneList)
        self.ui.timeZone.setCurrentIndex(zoneList.index("Europe/Istanbul"))
        
        # Load Groups        
        # Default Groups to groupsIn
        self.ui.groupsIn.insertItems(0, kahya().defaultGroups)
        # Other groups to groupsOut
        self.ui.groupsOut.insertItems(0, list(set(self.allGroupList()) - set(self.getListItems(self.ui.groupsIn))))
        self.ui.groupsOut.sortItems()        
        
        # Load Partitioning types
        self.partitioningTypes = {
                             "Automatic Partitioning"       : "auto",
                             "Smart Automatic Partitioning" : "smartAuto",
                             "Manuel Partitioning"          : "manuel",
                             
                             }
        
        self.ui.partitioningTypeBox.insertItems(0, self.partitioningTypes.keys())

        
        # Repo settings
        self.ui.repoName.setText(consts.pardus_repo_name)
        self.ui.repoAddress.setText(consts.pardus_repo_uri)
        
    def generateXMLButtonClicked(self):
        for user in self.users:
            if user.username == str(self.ui.autologinUserBox.currentText()):
                user.autologin = True
        variantKey = unicode(self.ui.variantBox.currentText())
        if variantKey:
            variantValue = self.variantContainer[variantKey]
        else:
            variantValue = None
            
        sg = SahipGenerator(language = str(self.ui.languageBox.currentText()),\
                             variant = variantValue,\
                       root_password = str(self.ui.rootPassword.text()),\
                            timezone = str(self.ui.timeZone.currentText()),\
                            hostname = str(self.ui.hostname.text()),\
                               users = self.users,\
                            reponame = str(self.ui.repoName.text()),\
                            repoaddr = str(self.ui.repoAddress.text()),\
                   partitioning_type = self.partitioningTypes[str(self.ui.partitioningTypeBox.currentText())],\
                                disk = str(self.ui.disk.text())
                        )
        
    def isUserAlreadyAdded(self, username):
        for user in self.users:
            if user.username == username:
                return True
        return False
    
    def shadowButtonClicked(self):
        import crypt
        inputPass = QtGui.QInputDialog.getText(self, 'Enter the root password to be shadowed', 'Password:', QtGui.QLineEdit.Normal)
        cryptedPass = crypt.crypt(str(inputPass[0]), str(inputPass[0]))
        self.ui.rootPassword.setText(cryptedPass)
    
    
    def userAddClicked(self):
        if self.ui.password1.text() != self.ui.password2.text():
            QtGui.QMessageBox.question(self, 'Error',"The Passwords do not match...", QtGui.QMessageBox.Ok)
        else: 
            newuser = User(str(self.ui.username.text()), str(self.ui.realname.text()), str(self.ui.password1.text()), self.getListItems(self.ui.groupsIn))
            
            if not newuser.usernameIsValid():
                QtGui.QMessageBox.question(self, 'Error',"Invalid username. Should include only [a-z][A-Z]_[0-9]", QtGui.QMessageBox.Ok)
                return
            if not newuser.realnameIsValid():
                QtGui.QMessageBox.question(self, 'Error',"Invalid real name. Can't have newline or : characters.", QtGui.QMessageBox.Ok)
                return
            if not newuser.passwordIsValid():
                QtGui.QMessageBox.question(self, 'Error',"Invalid password!", QtGui.QMessageBox.Ok)
                return
                
            if self.isUserAlreadyAdded(newuser.username):
                QtGui.QMessageBox.question(self, 'Error',"There's another user with username %s." % newuser.username, QtGui.QMessageBox.Ok)
                return
            
            self.ui.userList.insertItem(0, newuser.username)
            self.ui.userList.sortItems()
            self.users.append(newuser)
            
            # Add new user to autologin box. 
            self.ui.autologinUserBox.addItem(newuser.username)
            
        
    def userDeleteClicked(self):
        index = self.ui.userList.currentRow()
        if index == -1:
            QtGui.QMessageBox.question(self, 'Error',"No user selected.", QtGui.QMessageBox.Ok)
            return
        
        item = self.ui.userList.takeItem(index)
        username = item.text()
        self.ui.autologinUserBox.removeItem(index)
        del item

        # Delete the users in self.users list with the username specified.
        for user in self.users:
            if user.username == username:
                self.users.remove(user)
        
    def groupAddClicked(self):
        index = self.ui.groupsOut.currentRow()
        if index == -1:
            QtGui.QMessageBox.question(self, 'Error',"No group selected.", QtGui.QMessageBox.Ok)
            return
        item = self.ui.groupsOut.takeItem(index)
        self.ui.groupsIn.insertItem(0, item)
        del item
        self.ui.groupsIn.sortItems()
        
    def groupDeleteClicked(self):
        index = self.ui.groupsIn.currentRow()
        if index == -1:
            QtGui.QMessageBox.question(self, 'Error',"No group selected.", QtGui.QMessageBox.Ok)
            return
        item = self.ui.groupsIn.takeItem(index)
        self.ui.groupsOut.insertItem(0, item)
        del item
        self.ui.groupsOut.sortItems()
        
        

    def languageChanged(self, newLanguage):
        '''Retrieves information about the newLanguage and updates the variantBox accordingly.
        If the variant is a list, adds each variant to the variantBox
        If the variant is None, adds nothing to the variantBox.
                
        Creates a Variant instance for each variant to store the letter-name pair.
        '''
        self.localeData = locales[str(newLanguage)]
        
        # --------------------------------------------------------------------        
        # Update the xkbvariant combobox according to the language selected.
        # --------------------------------------------------------------------
        self.ui.variantBox.clear()
        self.variantContainer = {}
        variants = self.localeData["xkbvariant"]
        # If there are multiple variants,
        if isinstance(variants, list):
            # "xkbvariant" : [["f",_("Turkish F")],["",_("Turkish Q")]],
            for variant in variants:
                self.variantContainer[variant[1]] = variant[0]                
                self.ui.variantBox.insertItem(0, variant[1])
        # If the language doesn't have any variant
        elif variants == None:              
            pass
        # If something different, raise Exception.            
        else:
            raise Exception
        # ---------------------------------------------------------------------
        
        
    def allGroupList(self):
        groupsIn = []
        f = open("/etc/group")
        for line in f:
            groupName = line.split(":")[0]
            groupsIn.append(groupName)
        return groupsIn
    
    def getListItems(self, listWidget):
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
