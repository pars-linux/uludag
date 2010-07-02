import unittest
from pisi.specfile import SpecFile
from pisi import uri
from pisi.file import File

class FileTestCase(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

    def testMakeUri(self):
        self.spec = SpecFile()
        self.url = uri.URI(self.spec.source.sourceURI)
        f = File('repos/pardus-2007/system/base/curl/pspec.xml', File.read)
        self.assert_(f.make_uri('uri'))

    def testChooseMethod(self):
        compress = File('repos/contrib-2007/pisi-index.xml.bz2', File.read)
        self.assert_(File.choose_method('pisi.conf', compress))

    def testDecompress(self):
        localfile = File('repos/pardus-2007/system/base/curl/pspec.xml', File.read)
        compress = File('repos/contrib-2007/pisi-index.xml.bz2', File.read)
        self.assert_(File.decompress(localfile,compress))

    def testLocalFile(self):
        f = File('repos/pardus-2007/system/base/curl/pspec.xml', File.read)
        r = f.readlines()
        assert (len(r) > 0)

    def testRemoteRead(self):
        f = File('http://www.pardus.org.tr/urunler/pardus-2009.2-Geronticus_eremita-surum-notlari-tr.html', File.read)
        r = f.readlines()
        assert (len(r) > 0)


