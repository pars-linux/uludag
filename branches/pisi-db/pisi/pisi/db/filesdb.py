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

import pisi
import pisi.files
import pisi.oo
import pisi.db.sql as sql
import pysqlite2
 

class FilesDB(object):
    '''
        FilesDB provides db access operations for Files objects (files.Files)  
    '''
    def __init__(self):
        __metaclass__ = pisi.oo.Singleton
        self.connection = sql.get_connection()
        self.cursor = self.connection.cursor()
        self.create()
        self.total = 0
        self.totalsize = 0
    
    def create(self):
        self.cursor.execute(
                    'CREATE TABLE IF NOT EXISTS files \
                    (path TEXT PRIMARY KEY, packagename VARCHAR(50))'
                    )
        self.connection.commit()
        
    def destroy(self):
        self.cursor.execute('DROP TABLE IF EXISTS files ')
        self.connection.commit()
    
    def add_files(self, pkg_name, files, txn = None):
        for file in files.list:
            self.total += 1
            self.totalsize += len(file.path)
            print "Total files:", self.total , "Total size:" , self.totalsize
            st = 'insert into files (path , packagename) values (?, ?)'
            try:
                self.cursor.execute(st, (file.path, pkg_name))
            except:
                pass #collision..
        self.connection.commit()

    def remove_files(self, files, txn = None):
        for file in files.list:
            st = 'delete from files where path = ?'
            self.cursor.execute(st, (file.path,))
        self.connection.commit()
    
    def has_file(self, path, txn = None):
        st = 'select path from files where path= ?'
        self.cursor.execute(st, (path,))
        if self.cursor.fetchone() != None:
            return True
        return False
            
    def get_file(self, path, txn = None):
        st = 'select * from files where path = ?'
        self.cursor.execute(st, (path,))
        row = self.cursor.fetchone()
        if row != None:
            fileinfo = pisi.files.FileInfo()
            fileinfo.path = row[0]
            return (fileinfo, row[1])
        return None
    
    def close(self):
        if self.cursor != None:
            self.cursor.close()
        if self.connection != None:
            self.connection.close()
    
    
#===============================================================================
#    def __init__(self):
#        shelve.LockedDBShelf.__init__(self, 'files')
# 
#    def add_files(self, pkg_name, files, txn = None):
#        def proc(txn):
#            for x in files.list:
#                path = x.path
#                del x.path # don't store redundant attribute in db
#                self.put(path, (pkg_name, x), txn)
#                x.path = path # store it back in
#        self.txn_proc(proc, txn)
# 
#    def remove_files(self, files, txn = None):
#        def proc(txn):
#            for x in files.list:
#                if self.has_key(x.path):
#                    self.delete(x.path, txn)
#        self.txn_proc(proc, txn)
# 
#    def has_file(self, path, txn = None):
#        return self.has_key(str(path), txn)
# 
#    def get_file(self, path, txn = None):
#        path = str(path)
#        def proc(txn):
#            if not self.has_key(path, txn):
#                return None
#            else:
#                (name, fileinfo) = self.get(path, txn)
#                fileinfo.path = path
#                return (name, fileinfo)
#        return self.txn_proc(proc, txn)
#===============================================================================