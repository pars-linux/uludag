#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdecore import *

def getIconSet(name, group=KIcon.Toolbar):
    return KGlobal.iconLoader().loadIconSet(name, group)


class Icons:
    def _pix(self, name, scale=True):
        img = QImage(locate("data", "network-manager/" + name))
        if scale:
            img = img.smoothScale(32, 32)
        return QPixmap(img)

    def load_icons(self):
        self.nets = {
            "up": self._pix("ethernet-online.png"),
            "connecting": self._pix("ethernet-connecting.png"),
            "down": self._pix("ethernet-offline.png")
        }
        self.wifis = {
            "up": self._pix("wireless-online.png"),
            "connecting": self._pix("wireless-connecting.png"),
            "down": self._pix("wireless-offline.png")
        }
        self.dials = {
            "up": self._pix("dialup-online.png"),
            "connecting": self._pix("dialup-connecting.png"),
            "down": self._pix("dialup-offline.png")
        }
        self.pixs = {
            "net": self.nets,
            "wifi": self.wifis,
            "dialup": self.dials
        }
    
    def get_state(self, type, state):
        group = self.pixs.get(type, self.nets)
        icon = group.get(state, group["down"])
        return icon


icons = Icons()
