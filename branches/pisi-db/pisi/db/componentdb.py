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
import pisi.component

class ComponentDB(object):

    def __init__(self):

        self.component_nodes = {}
        self.repodb = pisi.db.repodb.RepoDB()

        for repo in self.repodb.list_repos():
            doc = self.repodb.get_repo_doc(repo)
            self.component_nodes[repo] = dict(map(lambda x: (x.getTagData("Name"), x), doc.tags("Component")))
            del doc

    def has_component(self, name, repo):
        return self.component_nodes.has_key(repo) and self.component_nodes[repo].has_key(name)
        
    def get_component(self, component_name, repo):

        if not self.has_component(component_name, repo):
            raise Exception(_('Component %s not found') % component_name)

        component = pisi.component.Component()
        component.parse(self.component_nodes[repo][component_name].toString())
        
        doc = self.repodb.get_repo_doc(repo)
        for pkg in doc.tags("Package"):
            if pkg.getTagData("PartOf") == component_name:
                component.packages.append(pkg.getTagData("Name"))

        for pkg in doc.tags("Source"):
            if pkg.getTagData("PartOf") == component_name:
                component.sources.append(pkg.getTagData("Name"))
        del doc
        
        return component

    def list_components(self, repo):

        if not self.component_nodes.has_key(repo):
            raise Exception(_('Repository %s does not exist.') % repo)

        return self.component_nodes[repo].keys()
