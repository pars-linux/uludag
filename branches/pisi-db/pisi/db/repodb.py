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

medias = (cd, usb, remote, local) = range(4)

class RepoDB(object):

    def __init__(self):
        self.__repoorder = self.__get_repoorder()

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

    def remove_repo(self, name):
        pisi.util.clean_dir(os.path.join(ctx.config.index_dir(), name))

    def get_source_repos(self):
        repos = []
        for r in self.list_repos():
            if self.get_repo_doc(r).getTag("SpecFile"):
                repos.append(r)
        return repos

    def get_binary_repos(self):
        repos = []
        for r in self.list_repos():
            if not self.get_repo_doc(r).getTag("SpecFile"):
                repos.append(r)
        return repos

    def list_repos(self):
        order = []

        #FIXME: get media order from pisi.conf
        for m in ["cd", "usb", "remote", "local"]:
            if self.__repoorder.has_key(m):
                order.extend(self.__repoorder[m])

        return order

    def __get_repoorder(self):
        repos_file = os.path.join(ctx.config.lib_dir(), ctx.const.info_dir, ctx.const.repos)
        repos = piksemel.parse(repos_file)
        order = {}

        for r in repos.tags():
            media = r.getTagData("Media")
            name = r.getTagData("Name")
            order.setdefault(media, []).append(name)

        return order
