# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('yali4', fallback=True)
_ = __trans.ugettext

import os
import yali4.users
import pardus.xorg
import yali4.gui.context as ctx

from PyQt4 import QtGui
from PyQt4.QtCore import *
from yali4.constants import consts
from yali4.gui.ScreenWidget import ScreenWidget
from yali4.gui.Ui.setupuserswidget import Ui_SetupUsersWidget
from yali4.gui.YaliDialog import Dialog, WarningDialog, WarningWidget

##
# Partitioning screen.
class Widget(QtGui.QWidget, ScreenWidget):
    title = _('Set Users')
    desc = _('Create users to use Pardus..')
    icon = "iconUser"
    help = _('''
<font size="+2">User setup</font>

<font size="+1">
<p>
Other than the system administrator user,
you can create a user account for your 
daily needs, i.e reading your e-mail, surfing
on the web and searching for daily recipe
offerings. Usual password assignment
rules also apply here: This password should 
be unique and private. Choose a password 
difficult to guess, but easy to remember. 
</p>
<p>
Click Next button to proceed.
</p>
</font>
''')

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_SetupUsersWidget()
        self.ui.setupUi(self)

        self.edititemindex = None

        self.ui.pass_error.setVisible(False)
        self.ui.caps_error.setVisible(False)

        self.ui.caps_error.setText(_('<font color="#FF6D19">Caps Lock is on!</font>'))

        # User Icons
        self.normalUserIcon = QtGui.QPixmap(":/gui/pics/user_normal.png")
        self.superUserIcon = QtGui.QPixmap(":/gui/pics/user_root.png")

        # KDE AutoLogin
        self.autoLoginUser = ""

        # Give Admin Privileges default
        self.ui.admin.setChecked(True)

        # Set disabled the create Button
        self.ui.createButton.setEnabled(False)

        # Connections
        self.connect(self.ui.pass1, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.pass2, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.username, SIGNAL("textChanged(const QString &)"),
                     self.slotTextChanged)
        self.connect(self.ui.createButton, SIGNAL("clicked()"),
                     self.slotCreateUser)
        self.connect(self.ui.deleteButton, SIGNAL("clicked()"),
                     self.slotDeleteUser)
        self.connect(self.ui.userList, SIGNAL("itemDoubleClicked(QListWidgetItem*)"),
                     self.slotEditUser)
        self.connect(self.ui.pass2, SIGNAL("returnPressed()"),
                     self.slotReturnPressed)

    def shown(self):
        ctx.installData.users = []
        ctx.installData.autoLoginUser = None

        self.checkUsers()
        self.checkCapsLock()
        self.ui.username.setFocus()

    def execute(self):
        isAdminSet = False
        for i in range(self.ui.userList.count()):
            u = self.ui.userList.item(i).getUser()
            if "wheel" in u.groups:
                isAdminSet = True

        if not isAdminSet:
            # show confirmation dialog
            w = WarningWidget(self)
            w.warning.setText(_('''<b>
<p>You have not defined an administrator!</p>

<p>A user without administrative rights cannot complete system maintenance 
tasks. You are strongly encouraged to define an administrator user.</p>

<p>Click "Cancel" to define an administrator user (recommended) or "OK" to 
go to next screen.</p>
</b>
'''))
            self.dialog = WarningDialog(w, self)
            if not self.dialog.exec_():
                ctx.mainScreen.enableBack()
                ctx.mainScreen.enableNext()
                return False

        # reset and fill pending_users
        yali4.users.reset_pending_users()

        ctx.installData.autoLoginUser = str(self.ui.autoLogin.currentText())

        for i in range(self.ui.userList.count()):
            u = self.ui.userList.item(i).getUser()
            ctx.installData.users.append(u)
            yali4.users.pending_users.append(u)

        return True

    def checkCapsLock(self):
        if pardus.xorg.capslock.isOn():
            self.ui.caps_error.setVisible(True)
        else:
            self.ui.caps_error.setVisible(False)

    def keyReleaseEvent(self, e):
        self.checkCapsLock()

    def showError(self,message):
        self.ui.pass_error.setText("<center>%s</center>" % message)
        self.ui.pass_error.setVisible(True)
        self.ui.createButton.setEnabled(False)

    def slotTextChanged(self):
        p1 = self.ui.pass1.text()
        p2 = self.ui.pass2.text()

        if not p1 == '' and (p1 == self.ui.username.text() or p1 == self.ui.realname.text()):
            self.showError(_('<font color="#FF6D19">Don\'t use your user name or name as a password.</font>'))
            return
        elif p2 != p1 and p2:
            self.showError(_('<font color="#FF6D19">Passwords do not match!</font>'))
            return
        elif len(p1) == len(p2) and len(p2) < 4 and not p1=='':
            self.showError(_('<font color="#FF6D19">Password is too short!</font>'))
            return
        else:
            self.ui.pass_error.setVisible(False)

        if self.ui.username.text() and p1 and p2:
            self.ui.createButton.setEnabled(True)
        else:
            self.ui.createButton.setEnabled(False)

    def slotCreateUser(self):
        u = yali4.users.User()
        u.username = str(self.ui.username.text().toAscii())
        # ignore last character. see bug #887
        u.realname = unicode(self.ui.realname.text())
        u.passwd = unicode(self.ui.pass1.text())
        u.groups = ["users", "pnp", "pnpadmin", "removable", "disk", "audio", "video", "power", "dialout"]
        pix = self.normalUserIcon
        if self.ui.admin.isChecked():
            u.groups.append("wheel")
            pix = self.superUserIcon

        existsInList = [i for i in range(self.ui.userList.count())
                        if self.ui.userList.item(i).getUser().username == u.username]

        # check user validity
        if u.exists() or (existsInList and self.edititemindex == None):
            self.showError(_('<font color="#FF6D19">Username exists, choose another one!</font>'))
            return
        elif not u.usernameIsValid():
            self.showError(_('<font color="#FF6D19">Username contains invalid characters!</font>'))
            return
        elif not u.realnameIsValid():
            self.showError(_('<font color="#FF6D19">Realname contains invalid characters!</font>'))
            return

        self.ui.createButton.setText(_("Create User"))
        updateItem = None

        try:
            self.ui.userList.takeItem(self.edititemindex)
            self.ui.autoLogin.removeItem(self.edititemindex + 1)
        except:
            updateItem = self.edititemindex
            # nothing wrong. just adding a new user...
            pass

        self.edititemindex = None

        i = UserItem(self.ui.userList, pix, user = u)

        # add user to auto-login list.
        self.ui.autoLogin.addItem(QString(u.username))

        if updateItem:
            self.ui.autoLogin.setCurrentIndex(self.ui.autoLogin.count())

        # clear form
        self.resetWidgets()

        ctx.debugger.log("slotCreateUser :: user '%s (%s)' added/updated" % (u.realname,u.username))
        ctx.debugger.log("slotCreateUser :: user groups are %s" % str(','.join(u.groups)))

        # give focus to username widget for a new user. #3280
        self.ui.username.setFocus()
        self.checkUsers()

    def slotDeleteUser(self):
        if self.ui.userList.currentRow()==self.edititemindex:
            self.resetWidgets()
            self.ui.autoLogin.setCurrentIndex(0)
        _cur = self.ui.userList.currentRow()
        self.ui.userList.takeItem(_cur)
        self.ui.autoLogin.removeItem(_cur + 1)
        self.checkUsers()

    def slotEditUser(self, item):
        u = item.getUser()

        self.ui.username.setText(QString(u.username))
        self.ui.realname.setText(QString(u.realname))
        self.ui.pass1.setText(QString(u.passwd))
        self.ui.pass2.setText(QString(u.passwd))

        if "wheel" in u.groups:
            self.ui.admin.setChecked(True)
        else:
            self.ui.admin.setChecked(False)

        self.edititemindex = self.ui.userList.currentRow()
        self.ui.createButton.setText(_("Update User"))

    def checkUsers(self):
        if self.ui.userList.count():
            self.ui.deleteButton.setEnabled(True)
            self.ui.autoLogin.setEnabled(True)
            ctx.mainScreen.enableNext()
        else:
            # there is no user in list so noting to delete
            self.ui.deleteButton.setEnabled(False)
            self.ui.autoLogin.setEnabled(False)
            ctx.mainScreen.disableNext()

    def resetWidgets(self):
        # clear all
        self.ui.username.clear()
        self.ui.realname.clear()
        self.ui.pass1.clear()
        self.ui.pass2.clear()
        self.ui.admin.setChecked(False)
        self.ui.createButton.setEnabled(False)

    def slotReturnPressed(self):
        self.slotCreateUser()

class UserItem(QtGui.QListWidgetItem):

    ##
    # @param user (yali.users.User)
    def __init__(self, parent, pix, user):
        _pix = QtGui.QIcon(pix)
        _user= QString(user.username)
        QtGui.QListWidgetItem.__init__(self,_pix,_user,parent)
        self._user = user

    def getUser(self):
        return self._user
