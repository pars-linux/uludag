#!/usr/bin/python
# -*- coding: utf-8 -*-

globalIconFinder = None

def setIconFinder(finder):
    global globalIconFinder
    globalIconFinder = finder

def iconFinder():
    global globalIconFinder

    if not globalIconFinder:
        return lambda icon: ""

    return globalIconFinder
