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
import pisi.cli.info as info
import pisi.context as ctx
import pisi.api

class Search(info.Info):
    """Search packages

Usage: search <term1> <term2> ... <termn>

Finds a package containing specified search terms
in summary, description, and package name fields.
"""
    __metaclass__ = command.autocommand

    def __init__(self, args):
        super(Search, self).__init__(args)

    name = ("search", "sr")

    def options(self):
        group = optparse.OptionGroup(self.parser, _("search options"))
        super(Search, self).add_options(group)
        group.remove_option("--component")
        group.remove_option("--short")
        group.remove_option("--xml")
        group.add_option("-l", "--long", action="store_true",
                               default=False, help=_("Show details"))
        self.parser.add_option_group(group)

    def run(self):

        self.init(database = True, write = False)

        if not self.args:
            self.help()
            return

        r = pisi.api.search_package(self.args)
        ctx.ui.info(_('%s packages found') % len(r))

        ctx.config.options.short = not ctx.config.options.long
        for pkg in r:
            self.info_package(pkg)
