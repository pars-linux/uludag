# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

class Singleton(object):
    def __new__(type):
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

class LazyDB(Singleton):
    def __init__(self):
        if not self.__dict__.has_key("initialized"):
            self.initialized = False
    
    def __getattr__(self, attr):
        if not self.initialized:
            self.init()
            self.initialized = True

        if not self.__dict__.has_key(attr):
            raise AttributeError, attr

        return self.__dict__[attr]
