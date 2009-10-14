import unittest
from pisi.configfile import ConfigurationFile

class ConfigFileTestCase(unittest.TestCase):

    def setUp(self):
        self.cf = ConfigurationFile('pisi.conf')

    def testGeneralDefaults(self):
        cf = self.cf
        self.assertEqual(cf.general.destinationDirectory, cf.general['destinationDirectory'])
        assert not cf.general.autoclean
        self.assertEqual(cf.general.http_proxy, cf.general['http_proxy'])
        assert not cf.general.package_cache

    def testBuildDefaults(self):
        cf = self.cf
        self.assertEqual(cf.build.jobs, cf.build['jobs'])
        assert not cf.build.generateDebug
        assert not cf.build.enableSandbox
        self.assertEqual(cf.build.compressionlevel, cf.build['compressionlevel'])
        self.assertEqual(cf.build.fallback, cf.build['fallback'])

    def testDirectoriesDefaults(self):
        cf = self.cf
        self.assertEqual(cf.dirs.lib_dir, cf.dirs['lib_dir'])
        self.assertEqual(cf.dirs.index_dir, cf.dirs['index_dir'])

    def testConfigurationSection(self):
        cf = self.cf
        if not cf.general:
            self.fail()
        if not cf.build:
            self.fail()
        if not cf.dirs:
            self.fail()

    def testPisiConfValues(self):
        cf = self.cf
        self.assertEqual(cf.dirs.kde_dir, '/usr/kde/3.5')
        self.assertEqual(cf.dirs.compiled_packages_dir, '/var/cache/pisi/packages')
        self.assertEqual(cf.general.architecture, 'i686')
        self.assertEqual(cf.general.distribution_release, '2008')

    def testValuesExists(self):
        cf = self.cf
        assert cf.general.distribution
        assert not cf.general.targetDirectory
        assert cf.build.cxxflags
        assert not cf.build.configurationlevel
        assert cf.dirs.qt_dir
        assert not cf.dirs.cache_dir







