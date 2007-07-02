#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.

from profileDialog import profileDialog
from utility import getPrograms

class profileHandler(profileDialog):
    def __init__(self,profiles=None,parent = None,name = None,modal = 0,fl = 0):
##        self.programs = getPrograms()
        profileDialog.__init__(self,parent)
        self.show()
    
    def slotUpdated():
        pass

    def slotApply():
        pass
