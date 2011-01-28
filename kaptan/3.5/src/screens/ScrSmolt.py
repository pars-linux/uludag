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
import sys
import threading

from screens.Screen import ScreenWidget
from screens.smoltdlg import SmoltWidget

sys.path.append('/usr/share/smolt/client')

import smolt

class Widget(SmoltWidget, ScreenWidget):

    # title and description at the top of the dialog window
    title = i18n("Share your hardware profile")
    desc = i18n("Share your hardware profile")
    icon = ""


    def __init__(self, *args):
        apply(SmoltWidget.__init__, (self,) + args)

        # set texts
        self.setName(i18n("Hardware Profile"))
        self.textSmolt.setText(i18n("You can help Pardus by sharing your hardware profile. Your hardware information will be collected and sent to Pardus anonymously."))
        self.privacyButton.setText(i18n("&Privacy policy"))
        self.sendCheckBox.setText(i18n("&Share my hardware profile"))

        self.hdInfoListView.setSorting(-1)

        self.hdInfoListView.addColumn(i18n("Label"))
        self.hdInfoListView.header().setClickEnabled(0,self.hdInfoListView.header().count() - 1)
        self.hdInfoListView.addColumn(i18n("Value"))
        self.hdInfoListView.header().setClickEnabled(0,self.hdInfoListView.header().count() - 1)
        self.hdInfoListView.setResizeMode( KListView.LastColumn )

        self.labels()

        self.profile = smolt.Hardware()
        for label, value in reversed(list(self.profile.hostIter())):
            item = KListViewItem(self.hdInfoListView, None)
            item.setText(0,self.sendable_host_labels.pop())
            item.setText(1,str(value))

        QObject.connect(self.privacyButton, SIGNAL("clicked()"), self.changePage)

    def showPrivacy(self):
        self.mainStack.raiseWidget(1)
        self.privacyButton.setText(i18n("&Host Information"))
        self.privacyTextEdit.setText(PRIVACY_POLICY)

    def showHost(self):
        self.mainStack.raiseWidget(0)
        self.privacyButton.setText(i18n("&Privacy Policy"))

    def changePage(self):
        if self.mainStack.id(self.mainStack.visibleWidget()) == 0:
            self.showPrivacy()
        else:
            self.showHost()

    def send(self):
        if self.sendCheckBox.isChecked():
            Send().start()

    def labels(self):
        self.sendable_host_labels = [ i18n("UUID"),
                                      i18n("OS"),
                                      i18n("Default Run Level"),
                                      i18n("Language"),
                                      i18n("Platform"),
                                      i18n("BogoMIPS"),
                                      i18n("CPU Vendor"),
                                      i18n("CPU Model"),
                                      i18n("CPU Stepping"),
                                      i18n("CPU Family"),
                                      i18n("CPU Model Num"),
                                      i18n("Number of CPUs"),
                                      i18n("CPU Speed"),
                                      i18n("System Memory"),
                                      i18n("System Swap"),
                                      i18n("Vendor"),
                                      i18n("System"),
                                      i18n("Form Factor"),
                                      i18n("Kernel"),
                                      i18n("SELinux Enabled"),
                                      i18n("SELinux Policy"),
                                      i18n("SELinux Enforce") ]

    def shown(self):
        # Should check internet connection
        pass

    def execute(self):
        self.send()

class Send(threading.Thread):

    def run(self):
        s_client = smolt.Hardware()
        response = s_client.send()

        # Goodbye screen should check against smolt err before quit.
        # What if kaptan quits before smolt finishes its jobs?
        #if response[0] != 0:
        #    with open("smolt.err","w") as flog:
        #        flog.write(str(response[0]))


PRIVACY_POLICY = \
"""<p>Smolt will only send hardware and basic operating system information to the
Pardus smolt server (smoon).  The only tie from the database to a submitters
machine is the UUID.  As long as the submitter does not give out this UUID
the submission is anonymous.  If at any point in time a user wants to delete
their profile from the database they need only run</p>

    <b>smoltDeleteProfile</b>

<p>The information sent to the smolt database server should be considered public
in that anyone can view the statistics, data and share machine profiles.  In 
many ways smolt is designed to get hardware vendors and other 3rd parties'
attention.  As such, not only will this information be shared with 3rd parties,
we will be using smolt as leverage to gain better support for open source
drivers and better support in general.</p>

<p><u><i>IP Logging:</i></u>  In Pardus's smolt install all web traffic goes through a proxy
server first.  This is the only place IP addresses are being logged and they
are kept on that server for a period of 4 weeks at which time log rotation
removes these logs.  The Fedora Project does not aggregate ip addresses in
the smolt database.  These logs are private and will not be available to the
general public.</p>

<p>Users unhappy with this policy should simply not use smolt.  Users with
questions about this policy should contact the Pardus Infrastructure Team at
<i>admin [at] pardus.org.tr<i>  Also remember that users can delete their
profiles at any time using</p>

     <b>smoltDeleteProfile</b>
"""
