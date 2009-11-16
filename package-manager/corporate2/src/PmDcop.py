#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

#
# Package Manager DCOP interface

import dcopexport

class PmDcop(dcopexport.DCOPExObj):
    def __init__ (self, parent, id="Installer"):
        dcopexport.DCOPExObj.__init__(self, id)

        self.parent = parent
        self.addMethod ("void install(QString)", self.install)

    def install (self, package):
        manager = self.parent.mainwidget
        if manager.command.inProgress():
            return

        manager.installPackage(str(package))
