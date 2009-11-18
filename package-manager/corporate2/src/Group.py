#!/usr/bin/python
# -*- coding: utf-8 -*-

from qt import *

class Group:
    def __init__(self, name, packages, summary):
        self.name = name
        self.packages = packages
        self.summary = summary

    def remove(self, package):
        self.packages.remove(package)
