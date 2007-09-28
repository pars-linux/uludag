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
        component_packages = {}
        component_sources = {}

        self.repodb = pisi.db.repodb.RepoDB()

        for repo in self.repodb.list_repos():
            doc = self.repodb.get_repo_doc(repo)
            component_nodes[repo] = self.__generate_components(doc)
            component_packages[repo] = self.__generate_packages(doc)
            component_sources[repo] = self.__generate_sources(doc)

        self.cdb = pisi.db.itembyrepo.ItemByRepo(component_nodes)
        self.cpdb = pisi.db.itembyrepo.ItemByRepo(component_packages)
        self.csdb = pisi.db.itembyrepo.ItemByRepo(component_sources)

    def __generate_packages(self, doc):
        components = {}
        for pkg in doc.tags("Package"):
            components.setdefault(pkg.getTagData("PartOf"), []).append(pkg.getTagData("Name"))
        return components

    def __generate_sources(self, doc):
        components = {}
        for pkg in doc.tags("Source"):
            components.setdefault(pkg.getTagData("PartOf"), []).append(pkg.getTagData("Name"))
        return components
 
    def __generate_components(self, doc):
        return dict(map(lambda x: (x.getTagData("Name"), x.toString()), doc.tags("Component")))

    def has_component(self, name, repo = None):
        return self.cdb.has_item(name, repo)

    def list_components(self, repo=None):
        return self.cdb.get_item_keys(repo)

    # Returns the component in given repo or first found component in repo order if repo is None
    def get_component(self, component_name, repo = None):

        if not self.has_component(component_name, repo):
            raise Exception(_('Component %s not found') % component_name)

        component = pisi.component.Component()
        component.parse(self.cdb.get_item(component_name, repo))

        try:
            component.packages = self.cpdb.get_item(component_name, repo)
            component.sources = self.csdb.get_item(component_name, repo)
        except Exception: #FIXME: what exception could we catch here, replace with that.
            pass

        return component

    # Returns the component with combined packages and sources from all repos that contain this component
    def get_union_component(self, component_name):

        component = pisi.component.Component()
        component.parse(self.cdb.get_item(component_name))
        
        for repo in self.repodb.list_repos():
            try:
                component.packages.extend(self.cpdb.get_item(component_name, repo))
                component.sources.extend(self.csdb.get_item(component_name, repo))
            except Exception: #FIXME: what exception could we catch here, replace with that.
                pass
            
        return component

    # Returns packages of given component from given repo or first found component's packages in repo
    # order if repo is None. 
    # If walk is True than also the sub components' packages are returned
    def get_packages(self, component_name, repo=None, walk=False):

        component = self.get_component(component_name, repo)
        if not walk:
            return component.packages

        packages = []
        packages.extend(component.packages)

        sub_components = filter(lambda x:x.startswith(component_name+"."), self.list_components(repo))
        for sub in sub_components:
            try:
                packages.extend(self.get_component(sub, repo).packages)
            except Exception: #FIXME: what exception could we catch here, replace with that.
                pass

        return packages

    # Returns the component with combined packages and sources from all repos that contain this component
    # If walk is True than also the sub components' packages from all repos are returned
    def get_union_packages(self, component_name, walk=False):

        component = self.get_union_component(component_name)
        if not walk:
            return component.packages

        packages = []
        packages.extend(component.packages)

        sub_components = filter(lambda x:x.startswith(component_name+"."), self.list_components())
        for sub in sub_components:
            try:
                packages.extend(self.get_union_component(sub).packages)
            except Exception: #FIXME: what exception could we catch here, replace with that.
                pass

        return packages
