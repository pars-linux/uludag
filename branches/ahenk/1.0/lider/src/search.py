#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

from qt import *
from kdeui import *
from kdecore import *

import ldap

class SearchDialog(KDialog):
    """User search dialog."""
    
    def __init__(self, parent, connection=None, dn=None):
        KDialog.__init__(self, parent)
        self.connection = connection
        self.dn = dn
        
        self.setCaption(i18n("Search"))
        
        self.resize(450, 250)
        
        vb = QVBoxLayout(self, 6)
        vb.setMargin(12)
        
        grid = QGridLayout(1, 2, 6)
        vb.addLayout(grid)
        
        lab = QLabel(i18n("Name:"), self)
        grid.addWidget(lab, 0, 0, Qt.AlignRight)
        self.w_name = QLineEdit(self)
        grid.addWidget(self.w_name, 0, 1)
        
        self.w_search = QPushButton(self)
        self.w_search.setText(i18n("Search"))
        grid.addWidget(self.w_search, 1, 1)
        
        self.w_list = QListBox(self)
        grid.addWidget(self.w_list, 2, 1)
        
        self.connect(self.w_search, SIGNAL("clicked()"), self.search)
    
    def search(self):
        text = str(self.w_name.text())
        results = self.connection.search(self.dn, ldap.SCOPE_SUBTREE, "(&(objectclass=posixAccount)(|(uid=*%s*)(cn=*%s*)(uidNumber=*%s*)))" % (text, text, text))
        self.w_list.clear()
        for result in results:
            self.w_list.insertItem("%s - %s" % (result[1]["cn"][0], result[0]))

