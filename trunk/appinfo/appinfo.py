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

class AppInfo:
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

    def __init__(self, pm):
        """ Initialize with given PMS (Package Management System) """

        if not pm in backends.known_pms:
            raise Exception('Selected PMS (%s) is not available yet.' % pm)

        self._pm = backends.known_pms[pm]()
        self._sq = None

    def createDB(self, db='appinfo.db', force=False):
        """ Create given database """

        if not force and os.path.exists(db):
            return (False, 'DB already created.')

        if os.path.exists(db+'.backup'):
            os.unlink(db+'.backup')
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

        return (False, 'No such DB (%s).' % db)

    def _getPackagesFromDB(self):
        """ Internal method to get package list from database """

        if not self._sq:
            return (False, 'Initialize a DB first.')

        cursor = self._sq.execute('SELECT name FROM packages')
        return [str(package[0]) for package in cursor]

    def updatePackageList(self):
        """ Merge packages in database with packages in PMS """

        if not self._sq:
            return (False, 'Initialize a DB first.')

        packages_from_pms = self._pm.getPackageList()
        packages_from_db = self._getPackagesFromDB()
        new_packages = list(set(packages_from_db).difference(packages_from_db))

        for package in new_packages:
            self._sq.execute('INSERT INTO packages (name, score, nose) VALUES (?,0,0)', (package,) )

        self._sq.commit()
        return (True, '%s package insterted.' % len(new_packages))

