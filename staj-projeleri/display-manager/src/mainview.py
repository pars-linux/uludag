#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

from qt import *
from kdecore import *
from kdeui import *

from utility import *

import kdedesigner
from display_manager import formMain

import comar

class widgetMain(formMain):
    def __init__(self, parent):
        link = comar.Link()
        link.localize()
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL('activated(int)'), self.slotComar)

        formMain.__init__(self, parent)

        self.connect(self.pushTest, SIGNAL('clicked()'), self.slotTest)
        self.connect(self.pushHelp, SIGNAL('clicked()'), self.slotHelp)

    def slotComar(self, sock):
        reply = self.link.read_cmd()
        if reply.id == 1:
            self.editTest.setText(reply.data)

    def slotTest(self):
        self.link.call('Time.Clock.getDate', id=1)

    def slotHelp(self):
        help = HelpDialog('display-manager', i18n('Help'), self.parent())
        help.show()
