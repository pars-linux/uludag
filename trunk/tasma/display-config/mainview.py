#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import comar
from qt import *

from utility import *


class DisplayConfig(QWidgetStack):
    def __init__(self, parent):
        link = comar.Link()
        link.localize(languageCode())
        self.link = link
        self.notifier = QSocketNotifier(link.sock.fileno(), QSocketNotifier.Read)
        self.connect(self.notifier, SIGNAL("activated(int)"), self.slotComar)
        
        QWidgetStack.__init__(self, parent)
        #self.browse = browser.BrowseStack(self, link)
    
    def slotComar(self, sock):
        reply = self.link.read_cmd()
