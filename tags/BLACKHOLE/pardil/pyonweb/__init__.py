# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

__version__ = "0.1"

__all__ = ['page']

import sys

class Error(Exception):
  """Base class for exceptions in this module."""
  def __init__(self, value):
    print 'Content-type: text/html'
    print ''
    print 'Hata: ' + repr(value)
    sys.exit()
