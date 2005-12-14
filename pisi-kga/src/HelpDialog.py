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
#
# Authors:  İsmail Dönmez <ismail@uludag.org.tr>

from kdecore import KURL
from khtml import *

class HelpDialog(KHTMLPart):
    def __init__(self, parent=None):
        KHTMLPart.__init__(self)
        self.view().resize(500,600)
        self.openURL(KURL("file:///home/cartman/SVN/pisi-kga/help/tr/main_help.html"))
