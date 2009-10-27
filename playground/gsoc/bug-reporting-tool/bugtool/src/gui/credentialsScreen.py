# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#


from PyQt4 import QtGui
from PyQt4.QtCore import *
from PyKDE4.kdecore import ki18n
from bugz.bugzilla import Bugz
from cookiepot import CookiePot
from urllib2 import build_opener, HTTPCookieProcessor

from gui.ScreenWidget import ScreenWidget
from gui.credentialsWidget import Ui_bugWidget

#BUGZILLA_URL = 'http://bugs.pardus.org.tr'
BUGZILLA_URL = 'http://landfill.bugzilla.org/bugzilla-3.0-branch/'
LOGOUT_URL = 'http://bugs.pardus.org.tr/relogin.cgi'

class Widget(QtGui.QWidget, ScreenWidget):
    title = ki18n("Bug Reporting Tool")
    desc = ki18n("Credentials Screen")

    def __init__(self, *args):
        QtGui.QWidget.__init__(self,None)
        self.ui = Ui_bugWidget()
        self.ui.setupUi(self)
        QObject.connect(self.ui.logoutButton, SIGNAL("clicked()"),
                        self.logout)
        self.bugzilla = Bugz(BUGZILLA_URL)
        cj = CookiePot().make_lwp_cookiejar(self.bugzilla.cookiejar.filename,
                                            #'bugs.pardus.org.tr')
                                            'landfill.bugzilla.org')
        self.bugzilla.cookiejar = cj
        self.bugzilla.opener = build_opener(HTTPCookieProcessor(cj))
        self.is_logged_in = False

    def logout(self):
        self.bugzilla.authenticated = False
        self.bugzilla.opener.open(LOGOUT_URL).read()
        self.shown()

    def shown(self):
        if self.bugzilla.try_auth():
            self.is_logged_in = True
            self.ui.logoutButton.setVisible(True)
            self.ui.logoutText.setVisible(True)
            self.ui.username.setEnabled(False)
            self.ui.password.setEnabled(False)
        else:
            self.is_logged_in = False
            self.ui.logoutButton.setVisible(False)
            self.ui.logoutText.setVisible(False)
            self.ui.username.setEnabled(True)
            self.ui.password.setEnabled(True)
        pass

    def execute(self):
        if not self.is_logged_in:
            if len(self.ui.password.text()) == 0 or\
               len(self.ui.username.text()) == 0:
                return False
            else:
                self.bugzilla.user = self.ui.username.text()
                self.bugzilla.password = self.ui.password.text()
                try:
                    self.bugzilla.auth()
                except RuntimeError:
                    print 'Invalid user/pass pair!'
                    return False
        self.shared['bugzilla'] = self.bugzilla
        return True

    @property
    def shared(self):
        return self.parent().parent().parent().shared_data
