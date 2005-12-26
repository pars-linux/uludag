# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# All bugs are copyright (C) 2005, İsmail Dönmez <ismail@uludag.org.tr>

from qt import *
from kdecore import *
from kdeui import *

import users
from setupuserswidget import SetupUsersWidget

##
# Partitioning screen.
class Widget(SetupUsersWidget):

    def __init__(self, *args):
        apply(SetupUsersWidget.__init__, (self,) + args)

        self.pix.setPixmap(KGlobal().iconLoader().loadIcon("kuser", KIcon.Panel))
        self.pass_error.setText("")
        self.createButton.setEnabled(False)

        self.connect(self.pass1, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.pass2, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.username, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)

        self.connect(self.createButton, SIGNAL("clicked()"),
                     self.slotCreateUser)

        self.connect(self.deleteButton, SIGNAL("clicked()"),
                     self.slotDeleteUser)


        self.connect(self.userList, SIGNAL("doubleClicked(QListBoxItem*)"),
                     self.slotEditUser)

        self.connect(self.pass2, SIGNAL("returnPressed()"),
                     self.slotReturnPressed)

        self.connect(self.cancelButton, SIGNAL("clicked()"),
                     self.reset)

        self.editingMode = False
        
        f = file("/etc/passwd")
        for line in f.readlines():
            uid = int(line.split(':')[2])
            if uid >= 1000 and uid <= 2000:
                user = users.User(line.split(':')[0])
                user.realname = unicode(line.split(':')[4])
                useritem = UserItem(self.userList,user)

    def reset(self):
        self.editingMode = False
	self.username.setEnabled(True)
        self.username.clear()
        self.realname.clear()
        self.pass1.clear()
        self.pass2.clear()
        self.createButton.setText(i18n("&Create User"))
        
    def execute(self,user):
        self.reset()
        user.addUser()

        return True

    def slotTextChanged(self):

        p1 = self.pass1.text()
        p2 = self.pass2.text()

        if p2 != p1 and p2:
            self.pass_error.setText(
                i18n('<font color="#FF6D19">Passwords do not match!</font>'))
            self.pass_error.setAlignment(QLabel.AlignCenter)
            return self.createButton.setEnabled(False)
        else:
            self.pass_error.setText("")


        if self.username.text() and p1 and p2:
            self.createButton.setEnabled(True)
        else:
            self.createButton.setEnabled(False)

        if self.username.text() and self.username.text().isEmpty():
            self.createButton.setEnabled(False)

    def slotCreateUser(self):

        if self.editingMode:
            if self.pass1.text().isEmpty() or self.pass2.text().isEmpty():
                self.pass_error.setText(i18n('<font color="#FF6D19">Password shouldn\'t be empty'))
                return
            u = users.User(str(self.userList.currentText()))
            u.realname = str(self.realname.text())
            u.passwd = str(self.pass1.text())
            u.updateUser()
            return
        
        u = users.User()
        u.username = self.username.text().ascii()
        # ignore last character. see bug #887
        u.realname = unicode(self.realname.text().utf8().data())[:-1]
        u.passwd = self.pass1.text().ascii()
        u.groups = ["users", "audio", "video", "haldaemon", "plugdev", "wheel", "dialout", "uucp", "scanner"]


        # check user validity
        if u.exists():
            self.pass_error.setText(
                i18n('<font color="#FF6D19">Username exists, choose another one!</font>'))
            return
        elif not u.usernameIsValid():
            self.pass_error.setText(
                i18n('<font color="#FF6D19">Username contains invalid characters!</font>'))
            return
        elif not u.realnameIsValid():
            self.pass_error.setText(
                i18n('<font color="#FF6D19">Realname contains invalid characters!</font>'))
            return

        try:
            self.userList.removeItem(self.edititemindex)
            del self.edititemindex
        except:
            # nothing wrong. just adding a new user...
            pass
        i = UserItem(self.userList, user = u)

        self.execute(u)


    def slotDeleteUser(self):

        if KMessageBox.warningContinueCancel(self,i18n('Do you really want to delete user \'%1\'?').arg(self.userList.currentText())) == KMessageBox.Continue:
            user = users.User(self.userList.currentText())
            user.delUser()
            self.userList.removeItem(self.userList.currentItem())
            self.reset()
        
    def slotEditUser(self, item):
        u = item.getUser()

        self.username.setText(u.username)
        self.realname.setText(u.realname)
        self.pass1.setText(u.passwd)
        self.pass2.setText(u.passwd)

        self.edititemindex = self.userList.currentItem()

        self.editingMode = True
        self.createButton.setText(i18n("&Edit User"))
        self.createButton.setEnabled(True)
        self.username.setEnabled(False)

        self.slotCreateUser()

    def slotReturnPressed(self):
        self.slotCreateUser()



class UserItem(QListBoxText):

    ##
    # @param user (users.User)
    def __init__(self, parent, user):
        apply(QListBoxText.__init__, (self,parent,user.username))
        self._user = user
    
    def getUser(self):
        return self._user

