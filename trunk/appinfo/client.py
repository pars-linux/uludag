#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2010, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# Python Libs
import math

# AppInfo Base Object
from base import AppInfo

class AppInfoClient(AppInfo):
    """ AppInfoClient
        -------------
        Client-side operations for AppInfo

        Notes:
        ------
        - Whole DB is built on sqlite3
        - Default database scheme described in database.py

    """

    def __init__(self, pm):
        AppInfo.__init__(self, pm)

    def getPackageScore(self, package):
        """ Returns given package calculated score:
            Where score = score / nose """

        info = self.getPackagesFromDB(condition = "name = '%s'" % package)
        if info:
            return int(math.ceil(float(max(1,info[0][2])) / \
                                 float(max(1,info[0][3]))))
        return 1

    def getPackageId(self, package):
        """ Returns given package db id """

        info = self.getPackagesFromDB("id", condition = "name = '%s'" % \
                package)
        if info:
            return info[0][0]

