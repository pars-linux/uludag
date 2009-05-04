# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file


class StorageFormat(object):
    """Generic Storage Format"""

    type = None
    partedFlag = None
    _resizable = False
    _bootable = False
    _migratable = False
    _maxSize = 0
    _minSize = 0
    _dump = False
    _check = False

    def __init__(self, *args, **kwargs):
        """

        """
    @property
    def type(self):
        return self.type

    @property
    def resizable(self):
        return self._resizable

    @property
    def bootable(self):
        self._bootable

    @property
    def migratable(self):
        return self._migratable

    @property
    def dump(self):
        return self._dump

    @property
    def check(self):
        return self._check

    @property
    def minSize(self):
        return self._minSize

    @property
    def maxSize(self):
