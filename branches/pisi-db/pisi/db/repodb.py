# -*- coding: utf-8 -*-
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

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi
import pisi.db.lockeddbshelve as shelve
import pisi.context as ctx

class Error(pisi.Error):
    pass

class Repo:
    def __init__(self, indexuri):
        self.indexuri = indexuri

#class HttpRepo

#class FtpRepo

#class RemovableRepo


class RepoDB(object):
    """RepoDB maps repo ids to repository information"""

    def __init__(self):
        self.d = shelve.LockedDBShelf("repo")
        if not self.d.has_key("order"):
            self.d.put("order", [])

    def close(self):
        self.d.close()

    def repo_name(self, ix):
        l = self.list()
        return l[ix]

    def has_repo(self, name):
        name = str(name)
        return self.d.has_key("repo-" + name)

    def get_repo(self, name):
        name = str(name)
        return self.d["repo-" + name]

    def set_default_repo(self, name):
        name = str(name)
        order = self.d.get("order")
        try:
            index = order.index(name)
            order[0], order[index] = order[index], order[0]
            self.d.put("order", order)
        except ValueError:
            raise Error(_('No repository named %s exists') % name)

    def add_repo(self, name, repo_info, at = None):
        """add repository with name and repo_info at a given optional position"""
        name = str(name)
        assert (isinstance(repo_info,Repo))

        if self.d.has_key("repo-" + name):
            raise Error(_('Repository %s already exists') % name)

        self.d.put("repo-" + name, repo_info)
        order = self.d.get("order")
        if at == None:
            order.append(name)
        else:
            if at<0 or at>len(order):
                raise Error(_("Cannot add repository at position %s") % at)
            order.insert(at, name)
        self.d.put("order", order)

    def list(self):
        return self.d["order"]

    def clear(self):
        self.d.clear()

    def remove_repo(self, name):
        name = str(name)

        self.d.delete("repo-" + name)
        l = self.d.get("order")
        l.remove(name)
        self.d.put("order", l)
        ctx.packagedb.remove_repo(name)
        ctx.sourcedb.remove_repo(name)
        ctx.componentdb.remove_repo(name)

db = None

def init():
    global db

    if db is not None:
        return db

    db = RepoDB()
    return db

def finalize():
    global db

    if db is not None:
        db.close()
        db = None
