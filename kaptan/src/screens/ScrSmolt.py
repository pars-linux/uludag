# -*- coding: utf-8 -*-
#
# Copyright (C) 2008, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

from qt import *
from kdecore import *
from kdeui import *
import kdedesigner
import subprocess

from screens.Screen import ScreenWidget
from screens.smoltdlg import SmoltWidget
from screens.smoltDetailsPopup import smoltDetailsWidget
from screens.smoltPrivacyPopup import smoltPrivacyWidget

class Widget(SmoltWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Pardus hardware profiler")
    desc = i18n("Pardus hardware profiler")
    icon = ""


    def __init__(self, *args):
        apply(SmoltWidget.__init__, (self,) + args)

        # set texts
        self.textSmolt.setText(i18n("Pardus hardware profiler gets your hardware info and sends it<br> to public Pardus server."))
        self.detailesButton.setText(i18n("Show details"))
        self.privacyButton.setText(i18n("Privacy policy"))
        self.sendCheckBox.setText(i18n("Send"))

        # run smolt and show output to user
        p = subprocess.Popen(["smoltSendProfile", "-p"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        global fullHdInfo
        fullHdInfo = QString(out).remove("\t")
        sumHdInfo = QString(out).remove("\t")
        i = sumHdInfo.find( "Devices", 0 )
        sumHdInfo.remove( i-2, 10000)
        #fullHdInfo.remove( 0, i+42)
        sumHdInfo = str(sumHdInfo).splitlines()
        #fullHdInfo = str(fullHdInfo).splitlines()

        self.hdInfoListView.setSorting(-1)

        self.hdInfoListView.addColumn(i18n("Label"))
        self.hdInfoListView.header().setClickEnabled(0,self.hdInfoListView.header().count() - 1)
        self.hdInfoListView.addColumn(i18n("Data"))
        self.hdInfoListView.header().setClickEnabled(0,self.hdInfoListView.header().count() - 1)
        self.hdInfoListView.setResizeMode( KListView.LastColumn )
        item = KListViewItem(self.hdInfoListView, None)

        global d
        d = {}
        l = len(sumHdInfo)
        x = True
        for line in sumHdInfo:
            label, data = line.split(':')
            d[label] = data
            item.setText(0,(label))
            item.setText(1,(d[label]))
            item = KListViewItem(self.hdInfoListView, item)

        QObject.connect(self.privacyButton, SIGNAL("clicked()"), self.privacy)
        QObject.connect(self.detailesButton, SIGNAL("clicked()"), self.popup)

    def popup(self):
        self.smoltPopup = smoltDetailsWidget()
        self.smoltPopup.hdInfoTextEdit.setText(fullHdInfo)
        self.smoltPopup.show()

    def privacy(self):
        self.smoltPrivacy = smoltPrivacyWidget()
        self.smoltPrivacy.privacyTextEdit.setText(PRIVACY_POLICY)
        self.smoltPrivacy.show()

    def send(self):
        if self.sendCheckBox.isChecked():
            p = subprocess.Popen(["smoltSendProfile", "-s", "http://www.smolts.org", "-a" ], stdout=subprocess.PIPE)
            out, err = p.communicate()
            #print err, "*****************\n\n\n", out

    def shown(self):
        pass

    def execute(self):
        self.send()
        #pass


PRIVACY_POLICY = \
"""Smolt will only send hardware and basic operating system information to the
Fedora smolt server (smoon).  The only tie from the database to a submitters
machine is the UUID.  As long as the submitter does not give out this UUID
the submission is anonymous.  If at any point in time a user wants to delete
their profile from the database they need only run

    smoltDeleteProfile

The information sent to the smolt database server should be considered public
in that anyone can view the statistics, data and share machine profiles.  In 
many ways smolt is designed to get hardware vendors and other 3rd parties'
attention.  As such, not only will this information be shared with 3rd parties,
we will be using smolt as leverage to gain better support for open source
drivers and better support in general.

IP Logging:  In Fedora's smolt install all web traffic goes through a proxy
server first.  This is the only place IP addresses are being logged and they
are kept on that server for a period of 4 weeks at which time log rotation
removes these logs.  The Fedora Project does not aggregate ip addresses in
the smolt database.  These logs are private and will not be available to the
general public.

Users unhappy with this policy should simply not use smolt.  Users with
questions about this policy should contact the Fedora Infrastructure Team at
admin [at] fedoraproject.org  Also remember that users can delete their
profiles at any time using "smoltDeleteProfile"
"""
