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

import os
from qt import *
from kdecore import *
from khtml import *

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self)
        self.setCaption(i18n("PiSi KGA Help"))
        self.layout = QGridLayout(self)
        self.htmlPart = KHTMLPart(self)
        self.resize(500,600)
        self.layout.addWidget(self.htmlPart.view(),1,1)
        
        if os.environ['LANG'].startswith('tr_TR'):
            self.htmlPart.openURL(KURL(locate("data","pisi_kga/help/tr/main_help.html")))
        else:
            self.htmlPart.openURL(KURL(locate("data","pisi_kga/help/en/main_help.html")))
    
    # Workaround http://mats.imk.fraunhofer.de/pipermail/pykde/2005-August/010945.html
    def close(self, alsoDelete = 1):  
        return QDialog.close(self, 1)
    
    # Same as above
    def __del__(self):
        try:
            return QDialog.close(self, 1)
        except:
            pass
