# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import Cookie

class cookie:

  def __init__(self):
    self.c = Cookie.SimpleCookie()
    self.index = 0
    try:
      cr = os.environ['HTTP_COOKIE']
    except KeyError:
      pass
    else:
      self.c.load(cr)

  def __getitem__(self, key):
    if key in self.c.keys():
      return self.c[key].value
    return ''
    
  def __setitem__(self, key, value):
    self.c[key] = value
    self.c[key]['max-age'] = 1800
    
  def __delitem__(self, key):
    self.c[key] = ''
    
  def __len__(self):
    return len(self.c)

  def has_key(self, key):
    return key in self.c.keys()

  def keys(self):
    return self.c.keys()

  def items(self):
    return self.c.items()
    
  def __iter__(self):
    self.index = 0
    return self
    
  def next(self):
    if self.index == len(self.c):
      raise StopIteration
    r = self.c.keys()[self.index]
    self.index = self.index + 1
    return r

  def save(self):
    print self.c
