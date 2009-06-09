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
import pisi.db.lazydb as lazydb

class RepoError(pisi.Error):
    pass

class Repo:
    def __init__(self, indexuri):
        self.indexuri = indexuri

medias = (cd, usb, remote, local) = range(4)

class RepoOrder:

    def __init__(self):
        self.repos = self._get_repos()

    def add(self, repo_name, repo_url, repo_type="remote"):
        repo_doc = self._get_doc()

        try:
            node = [x for x in repo_doc.tags("Repo")][-1]
            repo_node = node.appendTag("Repo")
        except IndexError:
            repo_node = repo_doc.insertTag("Repo")

        name_node = repo_node.insertTag("Name")
        name_node.insertData(repo_name)

        url_node = repo_node.insertTag("Url")
        url_node.insertData(repo_url)

        name_node = repo_node.insertTag("Status")
        name_node.insertData("active")

        media_node = repo_node.insertTag("Media")
        media_node.insertData(repo_type)

        self._update(repo_doc)

    def set_status(self, repo_name, status):
        repo_doc = self._get_doc()

        for r in repo_doc.tags("Repo"):
            if r.getTagData("Name") == repo_name:
                status_node = r.getTag("Status")
                if status_node:
                    status_node.firstChild().hide()
                    status_node.insertData(status)
                else:
                    status_node = r.insertTag("Status")
                    status_node.insertData(status)

        self._update(repo_doc)

    def get_status(self, repo_name):
        repo_doc = self._get_doc()
        for r in repo_doc.tags("Repo"):
            if r.getTagData("Name") == repo_name:
                status_node = r.getTag("Status")
                if status_node:
                    status = status_node.firstChild().data()
                    if status in ["active", "deactive"]:
                        return status
        return "deactive"

    def remove(self, repo_name):
        repo_doc = self._get_doc()

        for r in repo_doc.tags("Repo"):
            if r.getTagData("Name") == repo_name:
                r.hide()

        self._update(repo_doc)

    def get_order(self):
        order = []

        #FIXME: get media order from pisi.conf
        for m in ["cd", "usb", "remote", "local"]:
            if self.repos.has_key(m):
                order.extend(self.repos[m])

        return order

    def _update(self, doc):
        repos_file = os.path.join(ctx.config.info_dir(), ctx.const.repos)
        open(repos_file, "w").write("%s\n" % doc.toPrettyString())
        self.repos = self._get_repos()

    def _get_doc(self):
        repos_file = os.path.join(ctx.config.info_dir(), ctx.const.repos)
        if not os.path.exists(repos_file):
            return piksemel.newDocument("REPOS")
        return piksemel.parse(repos_file)

    def _get_repos(self):
        repo_doc = self._get_doc()
        order = {}

        for r in repo_doc.tags("Repo"):
            media = r.getTagData("Media")
            name = r.getTagData("Name")
            status = r.getTagData("Status")
            order.setdefault(media, []).append(name)

        return order

class RepoDB(lazydb.LazyDB):

    def init(self):
        self.repoorder = RepoOrder()

    def has_repo(self, name):
        return name in self.list_repos(only_active=False)

    def has_repo_url(self, url):
        return url in self.list_repo_urls()

    def get_repo_doc(self, repo_name):
        repo = self.get_repo(repo_name)
        index = os.path.basename(repo.indexuri.get_uri())
        index_path = pisi.util.join_path(ctx.config.index_dir(), repo_name, index)

        if index_path.endswith("bz2"):
            index_path = index_path.split(".bz2")[0]

        if not os.path.exists(index_path):
            ctx.ui.warning("%s repository needs to be updated" % repo_name)
            return piksemel.newDocument("PISI")

        try:
            return piksemel.parse(index_path)
        except Exception, e:
            raise RepoError("Error parsing repository index information. Index file does not exist or is malformed.")

    def get_repo(self, repo):
        return Repo(pisi.uri.URI(self.get_repo_url(repo)))

    #FIXME: this method is a quick hack around repo_info.indexuri.get_uri()
    def get_repo_url(self, repo):
        urifile_path = pisi.util.join_path(ctx.config.index_dir(), repo, "uri")
        uri = open(urifile_path, "r").read()
        return uri

    def add_repo(self, name, repo_info, at = None):
        repo_path = pisi.util.join_path(ctx.config.index_dir(), name)
        os.makedirs(repo_path)
        urifile_path = pisi.util.join_path(ctx.config.index_dir(), name, "uri")
        uri = open(urifile_path, "w").write(repo_info.indexuri.get_uri())
        self.repoorder.add(name, repo_info.indexuri.get_uri())

    def remove_repo(self, name):
        pisi.util.clean_dir(os.path.join(ctx.config.index_dir(), name))
        self.repoorder.remove(name)

    def get_source_repos(self, only_active=True):
        repos = []
        for r in self.list_repos(only_active):
            if self.get_repo_doc(r).getTag("SpecFile"):
                repos.append(r)
        return repos

    def get_binary_repos(self, only_active=True):
        repos = []
        for r in self.list_repos(only_active):
            if not self.get_repo_doc(r).getTag("SpecFile"):
                repos.append(r)
        return repos

    def list_repos(self, only_active=True):
        return filter(lambda x:True if not only_active else self.repo_active(x), self.repoorder.get_order())

    def list_repo_urls(self, only_active=True):
        repos = []
        for r in self.list_repos(only_active):
            repos.append(self.get_repo_url(r))
        return repos

    def get_repo_by_url(self, url):
        if not self.has_repo_url(url):
            return None

        for r in self.list_repos(only_active=False):
            if self.get_repo_url(r) == url:
                return r

    def activate_repo(self, name):
        self.repoorder.set_status(name, "active")

    def deactivate_repo(self, name):
        self.repoorder.set_status(name, "deactive")

    def repo_active(self, name):
        return self.repoorder.get_status(name) == "active"
