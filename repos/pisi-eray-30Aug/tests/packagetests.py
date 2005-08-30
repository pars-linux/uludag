# Copyright (C) 2005, TUBITAK/UEKAE
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

from pisi import util
from pisi.config import config
from pisi import package


class PackageTestCase(unittest.TestCase):

    def setUp(self):
        self.pkgName = util.package_name("testing",
                                         "5.1",
                                         "2")

    def testAddExtract(self):
        cur = os.getcwd()
        tmpdir = config.tmp_dir()
        sandboxdir = os.path.join(cur, "tests/sandbox")

        pkg_path = os.path.join(tmpdir, self.pkgName)
        pkg = package.Package(pkg_path, "w")

        os.chdir(sandboxdir)
        pkg.add_to_package("files.xml")
        pkg.add_to_package("metadata.xml")
        os.chdir(cur)

        pkg.close()

        pkg = package.Package(pkg_path)
        pkg.extract_file("files.xml", cur)
        if not os.path.exists("files.xml"):
            self.fail("Package extract error")

        os.remove("files.xml")
        os.remove(pkg_path)

suite = unittest.makeSuite(PackageTestCase)
