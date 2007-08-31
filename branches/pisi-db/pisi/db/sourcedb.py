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

import piksemel

import pisi
import pisi.specfile

class SourceDB(object):

    def __init__(self):

        self.source_nodes = {}
        self.pkgstosrc = {}

        repodb = pisi.db.repodb.RepoDB()

        for repo in repodb.list_repos():

            self.source_nodes[repo] = {}
            self.pkgstosrc[repo] = {}

            doc = repodb.get_repo_doc(repo)
            for spec in doc.tags("SpecFile"):
                src_name = x.getTag("Source").getTagData("Name")
                self.source_nodes[repo][src_name] = spec.toString()
                for package in spec.tags("Package"):
                    self.pkgstosrc[repo][package.getTagData("Name")] = src_name
            del doc

    def list_sources(self, repo):
        if self.source_nodes.has_key(repo):
            return self.source_nodes[repo].keys()

        raise Exception(_('Repository %s does not exists.') % repo)

    def has_spec(self, name, repo):
        return self.source_nodes.has_key(repo) and self.source_nodes[repo].has_key(name)

    def get_spec(self, name, repo):
        spec, repo = self.get_spec_repo(name, repo)
        return spec

    def get_spec_repo(self, name, repo):
        if self.source_nodes.has_key(repo):
            if self.source_nodes[repo].has_key(name):
                spec = pisi.specfile.SpecFile()
                spec.parse(self.source_nodes[repo][name])
                return spec, repo

        raise Exception(_('Source package %s not found.') % name)

    def pkgtosrc(self, name, repo):
        if self.pkgstosrc.has_key(repo) and self.pkgstosrc[repo].has_key(name):
            return self.pkgstosrc[repo]
    

