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

import os

import pisi
import pisi.uri
import pisi.index
import pisi.context as ctx

class Repo:
    def __init__(self, indexuri):
        self.indexuri = indexuri

class RepoDB(object):

    def __init__(self):
        pass

    def close(self):
        pass

    def repo_name(self, ix):
        pass

    def has_repo(self, name):
        return name in self.list()

    def get_repo(self, repo):
        urifile_path = pisi.util.join_path(ctx.config.index_dir(), repo, "uri")
        uri = open(urifile_path, "r").read()
        return Repo(pisi.uri.URI(uri))
        
    def set_default_repo(self, name):
        pass

    def add_repo(self, name, repo_info, at = None):
        repo_path = pisi.util.join_path(ctx.config.index_dir(), name)
        os.makedirs(repo_path)
        urifile_path = pisi.util.join_path(ctx.config.index_dir(), name, "uri")
        uri = open(urifile_path, "w").write(repo_info.indexuri.get_uri())

    def list(self):
        return os.listdir(ctx.config.index_dir())

    def clear(self):
        pass

    def remove_repo(self, name):
        pass

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
