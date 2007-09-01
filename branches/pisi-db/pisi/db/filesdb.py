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

import os
import shelve

import pisi
import pisi.context as ctx

# FIXME:
# We could traverse through files.xml files of the packages to find the path and
# the package - a linear search - as some well known package managers do. But the current 
# file conflict mechanism of pisi prevents this and needs a fast has_file function. 
# So currently filesdb is the only db and we cant still get rid of rebuild-db :/

class FilesDB(object):

    def __init__(self):
        self.filesdb = {}
        self.__check_filesdb()
    
    def has_file(self, path):
        return self.filesdb.has_key(path)

    def get_file(self, path):
        return self.filesdb[path], path
    
    def add_files(self, pkg, files):

        self.__check_filesdb()

        for f in files.list:
            self.filesdb[f.path] = pkg

    def remove_files(self, pkg, files):
        for f in files:
            if self.filesdb.has_key(f):
                del self.filesdb[f]

    def destroy(self):
        files_db = os.path.join(ctx.config.lib_dir(), ctx.const.info_dir, ctx.const.files_db)
        if os.path.exists(files_db):
            os.unlink(files_db)
    
    def close(self):
        if isinstance(self.filesdb, shelve.DbfilenameShelf):
            self.filesdb.close()

    def __check_filesdb(self):
        if isinstance(self.filesdb, shelve.DbfilenameShelf):
            return

        info_dir = os.path.join(ctx.config.lib_dir(), ctx.const.info_dir)
        if not os.path.exists(info_dir):
            os.makedirs(info_dir)

        files_db = os.path.join(ctx.config.lib_dir(), ctx.const.info_dir, ctx.const.files_db)

        if not os.path.exists(files_db):
            flag = "n"
        elif os.access(files_db, os.W_OK):
            flag = "w"
        else:
            flag = "r"

        self.filesdb = shelve.open(files_db, flag)
