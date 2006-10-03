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

class page:

  def __init__(self):
    self.index = 0
    self.data = {}
    self.actions = {}
    self.form = cgi.FieldStorage()

    self.init()

  def __getitem__(self, key):
    return self.data[key]
    
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
    self.index = 0
    return self
    
  def next(self):
    if self.index == len(self.data):
      raise StopIteration
    r = self.data.keys()[self.index]
    self.index = self.index + 1
    return r

  def init(self):
    return

  def begin(self):
    return
    
  def end(self):
    return
    
  def run(self):
    self.begin()

    if self.form.getvalue('action', '') in self.actions:
      self.act = self.form.getvalue('action')
    else:
      self.act = 'default'

    self.actions[self.act]()

    self.end()

  def debug(self):
    self.run()

    print 'Content-type: text/html'
    print ''
    for i, j in self.data.items():
      print "%s => %s<br/>" % (i, repr(j))
