# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from bsddb3 import db

class bdb:

  def __init__(self, file):
    self.db = db.DB()
    self.index = 0
    try:
      self.verity(file)
    except:
      self.db.open(file, None, db.DB_HASH, db.DB_CREATE)
    else:
      self.db.open(file, None, db.DB_HASH, db.DB_DIRTY_READ)

  def __getitem__(self, key):
    return self.db.get(key)

  def __setitem__(self, key, value):
    self.db.put(key, value)

  def __delitem__(self, key):
    self.db.delete(key)

  def __len__(self):
    return self.db.stat()['nkeys']

  def keys(self):
    return self.db.keys()

  def items(self):
    return self.db.items()
    
  def __iter__(self):
    self.index = 0
    return self
   
  def next(self):
    if self.index == self.__len__():
      raise StopIteration
    r = self.db.keys()[self.index]
    self.index = self.index + 1
    return r

  def end(self):
    self.db.close()
