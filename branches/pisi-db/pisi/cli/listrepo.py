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

import pisi.cli.command as command
import pisi.context as ctx

class ListRepo(command.Command):
    """List repositories

Usage: list-repo

Lists currently tracked repositories.
"""
    __metaclass__ = command.autocommand

    def __init__(self, args):
        super(ListRepo, self).__init__(args)

    name = ("list-repo", "lr")

    def run(self):

        self.init(database = True, write = False)
        for repo in ctx.repodb.list_repos():
            ctx.ui.info(repo)
            print '  ', ctx.repodb.get_repo(repo).indexuri.get_uri()
        self.finalize()
