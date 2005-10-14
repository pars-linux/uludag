#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bulten_conf import *
from os.path import basename

class Entry(object):
    """An entry, that will be shown"""
    def __init__(self, src):
        self.src = src
        self.file = open(src, "r")
        super(Entry, self).__init__()

    def __str__(self):
        return self.src 

    def content(self):
        self.file.seek(0)
        return self.file.read()

    def title(self):
        self.file.seek(0)
        return self.file.readline()

    def file_name(self):
        return basename(self.file.name)

    def html_name(self):
        fname = self.file_name()
        return fname[:-3] + "html"

if __name__ == "__main__":
    pass
