# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.context as ctx

class ItemByRepo:
    def __init__(self, dbobj):
        self.dbobj = dbobj

    def has_repo(self, repo):
        return self.dbobj.has_key(repo)

    def has_item(self, item, repo=None):
        repos = ctx.repodb.list_repos()
        if repo:
            repos = [repo]

        for r in repos:
            if self.dbobj.has_key(r) and self.dbobj[r].has_key(item):
                return True

        return False

    def which_repo(self, item):
        for r in ctx.repodb.list_repos():
            if self.dbobj.has_key(r) and self.dbobj[r].has_key(item):
                return r

        raise Exception(_("Item not found"))

    def get_item_repo(self, item, repo=None):
        repos = ctx.repodb.list_repos()
        if repo:
            repos = [repo]

        for r in repos:
            if self.dbobj.has_key(r) and self.dbobj[r].has_key(item):
                return self.dbobj[r][item], r

        raise Exception(_("Repo item not found"))

    def get_item(self, item, repo=None):
        item, repo = self.get_item_repo(item, repo)
        return item

    def get_item_keys(self, repo=None):
        repos = ctx.repodb.list_repos()
        if repo:
            repos = [repo]

        items = []

        for r in repos:
            if not self.has_repo(r):
                raise Exception(_('Repository %s does not exist.') % repo)

            if self.dbobj.has_key(r):
                items.extend(self.dbobj[r].keys())

        return list(set(items))

    def get_item_values(self, repo=None):
        repos = ctx.repodb.list_repos()
        if repo:
            repos = [repo]

        items = []

        for r in repos:
            if not self.has_repo(r):
                raise Exception(_('Repository %s does not exist.') % repo)

            items.extend(self.dbobj[r])

        return list(set(items))
