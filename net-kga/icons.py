#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *

class Icons:
    def __init__(self):
        self.net_on = None
        self.net_conn = None
        self.net_off = None
        self.wifi_on = None
        self.wifi_conn = None
        self.wifi_off = None
        self.dial_on = None
        self.dial_conn = None
        self.dial_off = None
    
    def _pix(self, name):
        img = QImage(locate("data", "net_kga/" + name))
        img = img.smoothScale(48, 48)
        return QPixmap(img)
    
    def load_icons(self):
        self.net_on = self._pix("ethernet-online.png")
        self.net_conn = self._pix("ethernet-connecting.png")
        self.net_off = self._pix("ethernet-offline.png")
        self.wifi_on = self._pix("wireless-online.png")
        self.wifi_conn = self._pix("wireless-connecting.png")
        self.wifi_off = self._pix("wireless-offline.png")
        self.dial_on = self._pix("dialup-online.png")
        self.dial_conn = self._pix("dialup-connecting.png")
        self.dial_off = self._pix("dialup-offline.png")

icons = Icons()
