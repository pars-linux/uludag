#!/usr/bin/python
#-*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Authors:  Faik Uygur <faik@pardus.org.tr>

ADDED, REMOVED, INIT = range(3)
VERSION, CONFLICT, DEPENDENCY = range(3)

class with:
    def __init__(self):
        pass

def with_action(types, action, data):
    w = with()
    w.types = types
    w.action = action
    w.data = data
    return w

def with_version(version):
    return with_action(VERSION, INIT, version)

def with_conflicts(*cons):
    return with_action(CONFLICT, INIT, cons)

def with_dependencies(*deps):
    return with_action(DEPENDENCY, INIT, deps)

def with_added_conflicts(*cons):
    return with_action(CONFLICT, ADDED, cons)

def with_removed_conflicts(*cons):
    return with_action(CONFLICT, REMOVED, cons)

def with_added_dependencies(*deps):
    return with_action(DEPENDENCY, ADDED, deps)

def with_removed_dependencies(*deps):
    return with_action(DEPENDENCY, REMOVED, deps)
