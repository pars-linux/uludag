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

import piksemel

import pisi
import pisi.uri
import pisi.util
import pisi.index
import pisi.context as ctx

class Repo:
    def __init__(self, indexuri):
        self.indexuri = indexuri

class RepoDB(object):

    def __init__(self):
        pass

    def has_repo(self, name):
        return name in self.list_repos()

    def get_repo_doc(self, repo_name):
        repo = self.get_repo(repo_name)
        index = os.path.basename(repo.indexuri.get_uri())
        index_path = pisi.util.join_path(ctx.config.index_dir(), repo_name, index)
        return piksemel.parse(index_path[:-4])
    
    def get_repo(self, repo):
        urifile_path = pisi.util.join_path(ctx.config.index_dir(), repo, "uri")
        uri = open(urifile_path, "r").read()
        return Repo(pisi.uri.URI(uri))
        
    def add_repo(self, name, repo_info, at = None):
        repo_path = pisi.util.join_path(ctx.config.index_dir(), name)
        os.makedirs(repo_path)
        urifile_path = pisi.util.join_path(ctx.config.index_dir(), name, "uri")
        uri = open(urifile_path, "w").write(repo_info.indexuri.get_uri())

    def list_repos(self):
        return os.listdir(ctx.config.index_dir())

    def remove_repo(self, name):
        pisi.util.clean_dir(os.path.join(ctx.config.index_dir(), name))
