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
import os
import sqlite3

# AppInfo Libs
import config
import backends
import database

class AppInfo(object):
    """ AppInfo
        -------
        Package Management System indepented, package metadata
        information management system.

        Notes:
        ------
        - All methods returns a tuple which contains state of operation and
          state message (Boolean, Unicode)
        - Whole DB is built on sqlite3
        - Default database scheme described in database.py

    """

    def __getattribute__(self, name):
        if object.__getattribute__(self, '_sq') or \
                name in ('createDB', 'initializeDB'):
            return object.__getattribute__(self, name)
        return lambda:(False, 'Initialize a DB first')

    def __init__(self, pm):
        """ Initialize with given PMS (Package Management System) """

        if not pm in backends.known_pms:
            raise Exception('Selected PMS (%s) is not available yet.' % pm)

        self.config = config.Config()
        self._pm = backends.known_pms[pm]()
        self._sq = None
        self._db = None

    def initializeDB(self, db='appinfo.db', force = False):
        """ Initialize given database """

        if os.path.exists(db) or force:
            self._sq = sqlite3.connect(db)
            self._db = db
            return (True, 'DB Initialized sucessfuly.')

        self._sq = None

        return (False, 'No such DB (%s).' % db)

    def getPackagesFromDB(self, fields = '*', condition = ''):
        """ Internal method to get package list from database """

        if condition:
            condition = ' WHERE %s' % condition

        return self._sq.execute('SELECT %s FROM %s%s' % \
                (fields, database.PKG_TABLE, condition)).fetchall()

    def commitDB(self):
        """ Commit changes to DB """

        self._sq.commit()

        if self.config.updateSignAfterEachCommit:
            os.system('md5sum %s' % self._db)

