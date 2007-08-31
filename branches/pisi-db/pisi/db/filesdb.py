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

class Error(pisi.Error):
    pass

class FilesDB(object):

    def __init__(self):
        self.d = shelve.LockedDBShelf('files')

    def add_files(self, pkg_name, files):
        for x in files.list:
            path = x.path
            del x.path # don't store redundant attribute in db
            self.d.put(path, (pkg_name, x))
            x.path = path # store it back in

    def remove_files(self, files):
        for x in files.list:
            if self.d.has_key(x.path):
                self.d.delete(x.path)

    def close(self):
        self.d.close()
    
    def has_file(self, path):
        return self.d.has_key(str(path))

    def get_file(self, path):
        path = str(path)
        if not self.d.has_key(path):
            return None
        else:
            (name, fileinfo) = self.d.get(path)
            fileinfo.path = path
            return (name, fileinfo)

filesdb = None

def init():
    global filesdb
    if filesdb is not None:
        return filesdb

    filesdb = FilesDB()
    return filesdb

def finalize():
    global filesdb
    if filesdb is not None:
        filesdb.close()
        filesdb = None
