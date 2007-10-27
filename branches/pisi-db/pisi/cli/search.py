# -*- coding:utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import optparse

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.cli.command as command
import pisi.context as ctx
import pisi.db

class Search(command.Command):
    """Search packages

Usage: search <term1> <term2> ... <termn>

Finds a package containing specified search terms
in summary, description, and package name fields.
Default search is done in package database. Use
options to search in install database or source
database.
"""
    __metaclass__ = command.autocommand

    def __init__(self, args):
        super(Search, self).__init__(args)

    name = ("search", "sr")

    def options(self):
        group = optparse.OptionGroup(self.parser, _("search options"))
        group.add_option("-i", "--installdb", action="store_true",
                               default=False, help=_("Search in installdb"))
        group.add_option("-s", "--sourcedb", action="store_true",
                               default=False, help=_("Search in sourcedb"))
        self.parser.add_option_group(group)

    def run(self):

        self.init(database = True, write = False)

        if not self.args:
            self.help()
            return

        if ctx.get_option('installdb'):
            installdb = pisi.db.installdb.InstallDB()
            for pkg in installdb.search_package(self.args):
                pkg_info = installdb.get_package(pkg)
                print "%s - %s" % (pkg_info.name, pkg_info.summary)
        elif ctx.get_option('sourcedb'):
            sourcedb = pisi.db.sourcedb.SourceDB()
            for spec in sourcedb.search_spec(self.args):
                spec_info = sourcedb.get_spec(spec)
                print "%s - %s" % (spec_info.source.name, spec_info.source.summary)
        else:
            packagedb = pisi.db.packagedb.PackageDB()
            for pkg in packagedb.search_package(self.args):
                pkg_info = packagedb.get_package(pkg)
                print "%s - %s" % (pkg_info.name, pkg_info.summary)
