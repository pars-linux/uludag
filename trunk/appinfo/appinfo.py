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

import sys

from appinfo.server import AppInfoServer
from appinfo.client import AppInfoClient

from optparse import OptionParser

if __name__ == '__main__':

    usage = "usage: %prog [options] package [score]"
    parser = OptionParser(usage = usage)
    parser.add_option("-f", "--file", dest="filename", default="appinfo.db",
                      help="database to work on", metavar="FILE")
    parser.add_option("-r", "--reset", default = False, dest="resetdb",
                      help="reset given package score", action="store_true")
    parser.add_option("-u", "--update", default = False, dest="updatepkgdb",
                      help="update package db", action="store_true")
    parser.add_option("-c", "--create", default = False, dest="createdb",
                      help="creates a score db", action="store_true")
    (options, args) = parser.parse_args()

    if len(args) > 2:# or (not options.resetdb and len(args) < 2):
        parser.print_usage()
        sys.exit(0)

    readonly = True
    server = AppInfoServer()
    client = AppInfoClient()

    if any([options.createdb, options.updatepkgdb, options.resetdb, len(args) > 1]):
        readonly = False
        print ' - Trying to initialize Server DB:', server.initializeDB(options.filename)[1]

    if options.createdb:
        print ' - Trying to create db:' , server.createDB(options.filename)[1]
    if options.updatepkgdb:
        print ' - Trying to update packagelist:', server.updatePackageList()[1]
    if options.resetdb:
        print ' - Trying to reset scores:', server.resetPackageScores()
    if not options.resetdb and len(args) > 1:
        print ' - Trying to update package "%s" score:' % args[0], server.updatePackageScore(args[0], int(args[1]))[1]

    if readonly:
        init_db = client.initializeDB(options.filename)
        print ' - Trying to initialize Client DB:', init_db[1]
        if init_db[0] and len(args) > 0:
            print ' - Trying to get score for package "%s":' % args[0], client.getPackageScore(args[0])
    else:
        server.closeAndUpdateSum()

