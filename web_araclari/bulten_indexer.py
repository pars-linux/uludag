#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import time
from os.path import basename
from os import stat

class Index(object):
	
    def __init__(self, index_file):
        self.index = shelve.open(index_file)

    def check(self, src):
        file = basename(src)
        if self.index.has_key(file):
            return True
        return False

    def add(self, src):
        file = basename(src)
        st = stat(src)
        self.index[file] = st

    def get_mtime(self, src):
        file = basename(src)
        return self.index[file].st_mtime

    def get_entries_of_date(self, l, date):
        """return the entries for a given date (year, month)"""
        tmp = []
        for log in l:
            mtime = self.get_mtime(log)
            # date == (year, month)
            if date == time.localtime(mtime)[:2]:
                tmp.append(log)
        return tmp

    def comp(self, x, y):
        """sort filelist using the mtime(s)"""
        x = basename(x)
        y = basename(y)
        i = self.index
            if i.has_key(x) and i.has_key(y):
                if i[x].st_mtime > i[y].st_mtime: return -1
                elif i[x].st_mtime == i[y].st_mtime: return 0
            else: return 1

    def sort_filelist(self, l):
        l.sort(self.comp)
        return l

