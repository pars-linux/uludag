# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

##
# Abstract class for screen widgets
class ScreenWidget:

    title = ""
    desc = ""
    help = ""
    icon = None

    def shown(self):
        pass

    def execute(self):
        return True

    def nextCheck(self):
        return True

    def backCheck(self):
        return True

    def update(self):
        pass

