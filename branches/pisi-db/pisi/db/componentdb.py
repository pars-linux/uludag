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
import pisi.db.repodb
import pisi.db.itembyrepo
import pisi.component

class ComponentDB(object):

    def __init__(self):

        component_nodes = {}
        self.repodb = pisi.db.repodb.RepoDB()

        for repo in self.repodb.list_repos():
            doc = self.repodb.get_repo_doc(repo)
            component_nodes[repo] = self.__generate_components(doc)
            del doc

        self.cdb = pisi.db.itembyrepo.ItemByRepo(component_nodes)

    def __generate_components(self, doc):
        return dict(map(lambda x: (x.getTagData("Name"), x.toString()), doc.tags("Component")))

    def has_component(self, name, repo = None):
        return self.cdb.has_item(name, repo)

    def get_component(self, component_name, repo = None):

        if not self.has_component(component_name, repo):
            raise Exception(_('Component %s not found') % component_name)

        component = pisi.component.Component()
        component.parse(self.cdb.get_item(component_name, repo))
        return component

    def get_packages(self, component_name, repo, walk=False):

        packages = []

        if not self.has_component(component_name, repo):
            raise Exception(_('Component %s not found') % component_name)
        
        if walk:
            components = filter(lambda x:x.startswith(component_name), self.cdb.get_item_keys())
        else:
            components = self.cdb.get_item_keys()

        doc = self.repodb.get_repo_doc(repo)
        for pkg in doc.tags("Package"):
            if pkg.getTagData("PartOf") in components:
                packages.append(pkg.getTagData("Name"))

        return packages

    def list_components(self, repo=None):
        return self.cdb.get_item_keys(repo)

    def get_union_comp(self, component_name):

        component = self.get_component(component_name)

        for repo in self.repodb.list_repos():
            doc = self.repodb.get_repo_doc(repo)
            for pkg in doc.tags("Package"):
                if pkg.getTagData("PartOf") == component_name:
                    component.packages.append(pkg.getTagData("Name"))

            for pkg in doc.tags("Source"):
                if pkg.getTagData("PartOf") == component_name:
                    component.sources.append(pkg.getTagData("Name"))
            del doc

        return component
    
