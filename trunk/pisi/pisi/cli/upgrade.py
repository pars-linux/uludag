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

import os
import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.cli.command as command
import pisi.context as ctx
import pisi.blacklist
import pisi.api
import pisi.db

class Upgrade(command.PackageOp):
    """Upgrade PiSi packages

Usage: Upgrade [<package1> <package2> ... <packagen>]

<packagei>: package name

Upgrades the entire system if no package names are given

You may use only package names to specify packages because
the package upgrade operation is defined only with respect
to repositories. If you have specified a package name, it
should exist in the package repositories. If you just want to
reinstall a package from a PiSi file, use the install command.

You can also specify components instead of package names, which will be
expanded to package names.
"""
    __metaclass__ = command.autocommand

    def __init__(self, args):
        super(Upgrade, self).__init__(args)
        self.componentdb = pisi.db.componentdb.ComponentDB()

    name = ("upgrade", "up")

    def options(self):
        group = optparse.OptionGroup(self.parser, _("upgrade options"))

        super(Upgrade, self).options(group)
        group.add_option("--ignore-build-no", action="store_true",
                               default=False,
                               help=_("Do not take build no into account."))
        group.add_option("--security-only", action="store_true",
                     default=False, help=_("Security related package upgrades only"))
        group.add_option("-r", "--bypass-update-repo", action="store_true",
                     default=False, help=_("Do not update repositories"))
        group.add_option("--ignore-file-conflicts", action="store_true",
                     default=False, help=_("Ignore file conflicts"))
        group.add_option("--ignore-package-conflicts", action="store_true",
                     default=False, help=_("Ignore package conflicts"))
        group.add_option("-c", "--component", action="append",
                               default=None, help=_("Upgrade component's and recursive components' packages"))
        group.add_option("-f", "--fetch-only", action="store_true",
                     default=False, help=_("Fetch upgrades but do not install."))
        group.add_option("-x", "--exclude", action="append",
                     default=None, help=_("When upgrading system, ignore packages and components whose basenames match pattern."))
        group.add_option("--exclude-from", action="store",
                     default=None, help=_("When upgrading system, ignore packages and components whose basenames \
                     match any pattern contained in file."))

        self.parser.add_option_group(group)

    def run(self):

        if self.options.fetch_only:
            self.init(database=True, write=False)
        else:
            self.init()

        if not ctx.get_option('bypass_update_repo'):
            ctx.ui.info(_('Updating repositories'))
            repos = pisi.api.list_repos()
            for repo in repos:
                pisi.api.update_repo(repo)
            # reinitialize after update repo operation
            pisi.db.historydb.HistoryDB().init()
        else:
            ctx.ui.info(_('Will not update repositories'))

        components = ctx.get_option('component')
        packages = []
        if components:
            for name in components:
                if self.componentdb.has_component(name):
                    packages.extend(self.componentdb.get_union_packages(name, walk=True))
        packages.extend(self.args)

        if packages == []:
            packages = pisi.api.list_installed()

        packages = pisi.blacklist.exclude_from(packages, ctx.const.blacklist)

        if ctx.get_option('exclude_from'):
            packages = pisi.blacklist.exclude_from(packages, ctx.get_option('exclude_from'))

        if ctx.get_option('exclude'):
            packages = pisi.blacklist.exclude(packages, ctx.get_option('exclude'))

        pisi.api.upgrade(packages)
