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
import pisi.context as ctx

class SourceDB(object):

    def __init__(self):

        self.source_nodes = {}
        repodb = pisi.db.repodb.RepoDB()

        for repo in repodb.list_repos():
            doc = repodb.get_repo_doc(repo)
            self.source_nodes[repo] = dict(map(lambda x: (x.getTagData("Name"), x.toString()), doc.tags("Source")))

    def list_sources(self):
        raise Exception(_('Not implemented'))

    def has_spec(self, name, repo=None):
        raise Exception(_('Not implemented'))

    def get_spec(self, name, repo=None):
        raise Exception(_('Not implemented'))

    def get_spec_repo(self, name, repo=None):
        raise Exception(_('Not implemented'))

    def pkgtosrc(self, name):
        raise Exception(_('Not implemented'))
