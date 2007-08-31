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

"""
package source database
interface for update/query to local package repository
we basically store everything in sourceinfo class
yes, we are cheap
to handle multiple repositories, for sources, we
store a set of repositories in which the source appears.
the actual guy to take is determined from the repo order.
"""

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.context as ctx
import pisi.db.itembyrepodb

class NotfoundError(pisi.Error):
    pass

class SourceDB(object):

    def __init__(self):
        self.d = pisi.db.itembyrepodb.ItemByRepoDB('source')
        self.dpkgtosrc = pisi.db.itembyrepodb.ItemByRepoDB('pkgtosrc')

    def close(self):
        self.d.close()
        self.dpkgtosrc.close()

    def list(self):
        return self.d.list()

    def has_spec(self, name, repo=None):
        return self.d.has_key(name, repo)

    def get_spec(self, name, repo=None):
        try:
            return self.d.get_item(name, repo)
        except pisi.db.itembyrepodb.NotfoundError:
            raise NotfoundError(_("Source package %s not found") % name)

    def get_spec_repo(self, name, repo=None):
        try:
            return self.d.get_item_repo(name, repo)
        except pisi.db.itembyrepodb.NotfoundError:
            raise NotfoundError(_("Source package %s not found") % name)

    def pkgtosrc(self, name):
        return self.dpkgtosrc.get_item(name)

    def add_spec(self, spec, repo):
        assert not spec.errors()
        name = str(spec.source.name)

        self.d.add_item(name, spec, repo)
        for pkg in spec.packages:
            self.dpkgtosrc.add_item(pkg.name, name, repo)
        ctx.componentdb.add_spec(spec.source.partOf, spec.source.name, repo)

    def remove_spec(self, name, repo):
        name = str(name)

        assert self.has_spec(name)
        spec = self.d.get_item(name, repo)
        self.d.remove_item(name)
        for pkg in spec.packages:
            self.dpkgtosrc.remove_item_repo(pkg.name, repo)
        ctx.componentdb.remove_spec(spec.source.partOf, spec.source.name, repo)

    def remove_repo(self, repo):
        self.d.remove_repo(repo)
        self.dpkgtosrc.remove_repo(repo)

srcdb = None

def init():
    global srcdb
    if srcdb is not None:
        return srcdb

    srcdb = SourceDB()
    return srcdb

def finalize():
    global srcdb
    if srcdb is not None:
        srcdb.close()
        srcdb = None
