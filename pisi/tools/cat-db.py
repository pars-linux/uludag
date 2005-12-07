#!/usr/bin/python
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Author: Eray Ozkural <eray@uludag.org.tr>

import sys
import bsddb3.dbshelve as shelve

sys.path.append('.')

import pisi

d = shelve.open( sys.argv[1], flags='r' )

for (k, data) in d.iteritems():
    print k, data

d.close()
