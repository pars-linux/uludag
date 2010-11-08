#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

# Class responsible for debug output
class Debug:
    def __init__(self):
        self.writeFunc = sys.stderr.write

    def write(self, msg):
        self.writeFunc("DEBUG: %s\n" % msg)

    def setWriteFunc(self, func):
        self.writeFunc = func
