# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

from Cheetah.Template import Template

def build_template(template, data={}):
  f = open(template, 'r')
  templateStr = ''.join(f.readlines())
  f.close()
  
  index = Template(templateStr, searchList=[data])
  return str(index)
