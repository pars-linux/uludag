# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import unittest
import os

import pisi
import pisi.api
import pisi.util
import pisi.config

class TestCase(unittest.TestCase):

    def setUp(self, comar = False, database = True, options = None):
        if not options:
            options = pisi.config.Options()
            options.ignore_build_no = False
        options.destdir = 'tmp'
        pisi.api.init(options = options, comar = comar,
                      database = database, write = database)

    def tearDown(self, ):
        pisi.api.finalize()
