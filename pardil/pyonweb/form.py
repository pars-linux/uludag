# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import cgi

class form:

  def __init__(self):
    form = cgi.FieldStorage()
    self.index = 0
    self.data = {}
    for i in form.keys():
      self.data[i] = form.getvalue(i)

  def __getitem__(self, key):
    if key in self.data:
      return self.data[key]
    return ''
    
  def __setitem__(self, key, value):
    self.data[key] = value

  def __delitem__(self, key):
    del self.data[key]
    
  def __len__(self):
    return len(self.data)

  def has_key(self, key):
    return key in self.data.keys()

  def keys(self):
    return self.data.keys()

  def items(self):
    return self.data.items()
    
  def __iter__(self):
    return self
    
  def next(self):
    if self.index == len(self.data):
      self.index = 0
      raise StopIteration
    r = self.data.keys()[self.index]
    self.index = self.index + 1
    return r
