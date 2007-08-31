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
import pisi.component

class Error(pisi.Error):
    pass

class ComponentDB(object):
    """a database of components"""

    def __init__(self):
        self.d = pisi.db.itembyrepodb.ItemByRepoDB('component')

    def close(self):
        self.d.close()

    def destroy(self):
        self.d.destroy()

    def has_component(self, name, repo = pisi.db.itembyrepodb.repos):
        name = str(name)
        return self.d.has_key(name, repo)

    def get_component(self, name, repo=None):
        try:
            return self.d.get_item(name, repo)
        except pisi.db.itembyrepodb.NotfoundError, e:
            raise Error(_('Component %s not found') % name)

    def get_component_repo(self, name, repo=None):
        try:
            return self.d.get_item_repo(name, repo)
        except pisi.db.itembyrepodb.NotfoundError, e:
            raise Error(_('Component %s not found') % name)

    def get_union_comp(self, name, repo = pisi.db.itembyrepodb.repos ):
        """get a union of all repository components packages, not just the first repo in order.
        get only basic repo info from the first repo"""
        s = self.d.d.get(name)
        pkgs = set()
        srcs = set()
        for repostr in self.d.order(repo = repo):
            if s.has_key(repostr):
                pkgs |= set(s[repostr].packages)
                srcs |= set(s[repostr].sources)
        comp = self.get_component(name)
        comp.packages = list(pkgs)
        comp.sources = list(srcs)
        return comp

    def list_components(self, repo=None):
        return self.d.list(repo)

    # walk: walks through the underlying  components' packages
    def get_union_packages(self, component_name, walk=False, repo=pisi.db.itembyrepodb.repos):
        """returns union of all repository component's packages, not just the first repo's 
        component's in order"""
        
        component = self.get_union_comp(component_name, repo)
        if not walk:
            return component.packages

        packages = []
        packages.extend(component.packages)
        for dep in component.dependencies:
            packages.extend(self.get_union_packages(dep, walk, repo))

        return packages

    # walk: walks through the underlying  components' packages
    def get_packages(self, component_name, walk=False, repo=None):
        """returns the given component's and underlying recursive components' packages"""
        
        component = self.get_component(component_name, repo)
        if not walk:
            return component.packages

        packages = []
        packages.extend(component.packages)
        for dep in component.dependencies:
            packages.extend(self.get_packages(dep, walk, repo))

        return packages

    def add_child(self, component, repo):
        """update component tree"""
        parent_name = ".".join(component.name.split(".")[:-1])
        if not parent_name: # root component
            return

        if self.has_component(parent_name, repo):
            parent = self.get_component(parent_name, repo)
        else:
            parent = pisi.component.Component(name = parent_name)

        if component.name not in parent.dependencies:
            parent.dependencies.append(component.name)
            self.d.add_item(parent_name, parent, repo)

    def update_component(self, component, repo):
        if self.has_component(component.name, repo):
            # preserve list of sources, packages and dependencies
            current = self.d.get_item(component.name, repo)
            component.packages = current.packages
            component.sources = current.sources
            component.dependencies = current.dependencies
        self.d.add_item(component.name, component, repo)
        self.add_child(component, repo)

    def add_package(self, component_name, package, repo):
        assert component_name
        if self.has_component(component_name, repo):
            component = self.get_component(component_name, repo)
        else:
            component = pisi.component.Component( name = component_name )
        if not package in component.packages:
            component.packages.append(package)
        self.d.add_item(component_name, component, repo) # update
        self.add_child(component, repo)

    def remove_package(self, component_name, package, repo = None):
        if not self.has_component(component_name, repo):
            raise Error(_('Information for component %s not available') % component_name)
        if not repo:
            repo = self.d.which_repo(component_name) # get default repo then
        component = self.get_component(component_name, repo)
        if package in component.packages:
            component.packages.remove(package)
        self.d.add_item(component_name, component, repo) # update

    def add_spec(self, component_name, spec, repo):
        assert component_name
        if self.has_component(component_name, repo):
            component = self.get_component(component_name, repo)
        else:
            component = pisi.component.Component( name = component_name )
        if not spec in component.sources:
            component.sources.append(spec)
        self.d.add_item(component_name, component, repo) # update
        self.add_child(component, repo)

    def remove_spec(self, component_name, spec, repo = None):
        if not self.has_component(component_name, repo):
            raise Error(_('Information for component %s not available') % component_name)
        if not repo:
            repo = self.d.which_repo(component_name) # get default repo then
        component = self.get_component(component_name, repo)
        if spec in component.sources:
            component.sources.remove(spec)
        self.d.add_item(component_name, component, repo) # update

    def clear(self):
        self.d.clear()

    def remove_component(self, name, repo = None):
        name = str(name)
        self.d.remove_item(name, repo)

    def remove_repo(self, repo):
        self.d.remove_repo(repo)

componentdb = None

def init():
    global componentdb
    if componentdb is not None:
        return componentdb

    componentdb = ComponentDB()
    return componentdb

def finalize():
    global componentdb
    if componentdb is not None:
        componentdb.close()
        componentdb = None
