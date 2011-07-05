#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *
from kdeui import *
from kdecore import i18n, KGlobal, KIcon
from kfile import *

import kdedesigner

import os.path
import shutil
import sys

from permissionDialogUI import PermissionDialogUI

class PermissionDialog(PermissionDialogUI):
    def __init__(self, parent = None, name = None):
        PermissionDialogUI.__init__(self, parent, name)
        self.realLoc = ""
        self.connect(self.pbOK, SIGNAL("clicked()"), self, SLOT("accept()"))
        self.connect(self.pbCancel, SIGNAL("clicked()"), self, SLOT("reject()"))
	