
import unittest
import os

from pisi import version
from pisi import util
from pisi import context

class VersionTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def testOps(self):
        v1 = version.Version("0.3.1")
        v2 = version.Version("0.3.5")
        v3 = version.Version("1.5.2-4")
        v4 = version.Version("0.3.1-1")
        self.assert_(v1 < v2)
        self.assert_(v3 > v2)
        self.assert_(v1 <= v3)
        self.assert_(v4 >= v4)

suite = unittest.makeSuite(VersionTestCase)
