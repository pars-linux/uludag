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

import os
import sqlite3
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

        self._pm = backends.known_pms[pm]()
        self._sq = None

    def createDB(self, db='appinfo.db', force=False):
        """ Create given database """

        if not force and os.path.exists(db):
            self.initializeDB(db)
            return (False, 'DB already exists.')

        if os.path.exists(db+'.backup'):
            os.unlink(db+'.backup')

        if os.path.exists(db):
            os.rename(db, db+'.backup')

        self._sq = sqlite3.connect(db)
        self._sq.execute(database.DB_SCHEME)
        self._sq.commit()

        return (True, 'DB created sucessfuly.')

    def initializeDB(self, db='appinfo.db'):
        """ Initialize given database """

        if os.path.exists(db):
            self._sq = sqlite3.connect(db)
            return (True, 'DB Initialized sucessfuly.')

        self._sq = None
        return (False, 'No such DB (%s).' % db)

    def _getPackagesFromDB(self, fields = '*'):
        """ Internal method to get package list from database """

        return self._sq.execute('SELECT %s FROM %s' % (fields, database.PKG_TABLE)).fetchall()

    def updatePackageList(self):
        """ Merge packages in database with packages in PMS """

        packages_from_pms = self._pm.getPackageList()
        packages_from_db = [str(x[1]) for x in self._getPackagesFromDB()]
        new_packages = list(set(packages_from_pms) - set(packages_from_db))

        for package in new_packages:
            self._sq.execute('INSERT INTO %s (name, score, nose) VALUES (?,0,0)' % database.PKG_TABLE, (package,) )

        self._sq.commit()
        return (True, '%s package insterted.' % len(new_packages))

    def createRatingDB(self):
        """ It creates a rating DB from packages DB,
            to use by Appinfo clients """

        return self._getPackagesFromDB()

        # raw = self._sq.execute('SELECT * FROM %s' % database.PKG_TABLE)

a = AppInfo('pisi')
print a.createDB()
print a.updatePackageList()
#print a.createRatingDB()

