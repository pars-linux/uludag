
import unittest
import os

from pisi import installdb
from pisi import util
from pisi import context

class InstallDBTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = context.Context()
        pass

    def testRemoveDummy(self):
        installdb.remove('installtest')
        self.assert_(not installdb.is_installed('installtest'))
        
    def testInstall(self):
        installdb.remove('installtest')
        installdb.install('installtest', '0.1', '2', './tests/sandbox/files.xml')
        f = installdb.files('installtest')
        a = f.readlines()
        self.assertEqual(a[0], 'placeholder\n')
        self.assert_(installdb.is_installed('installtest'))

    def testRemovePurge(self):
        installdb.install('installtest', '0.1', '2', './tests/sandbox/files.xml')
        self.assert_(installdb.is_installed('installtest'))
        installdb.remove('installtest')
        self.assert_(installdb.is_removed('installtest'))
        installdb.purge('installtest', '0.1', '2')
        self.assert_(not installdb.is_recorded('installtest'))
        self.assert_(not os.access(installdb.files_name('installtest'), os.F_OK))

suite = unittest.makeSuite(InstallDBTestCase)
