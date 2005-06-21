
import unittest
import os
from os.path import exists as pathexists
from os.path import basename, islink

from pisi import archive
from pisi import fetcher
from pisi import util
from pisi import context

class ArchiveFileTestCase(unittest.TestCase):
#     def setUp(self):
# 	pass

    def testUnpackTar(self):
	ctx = context.Context("samples/popt/popt.pspec")

	targetDir = ctx.pkg_work_dir()
        fileName = os.path.basename(ctx.spec.source.archiveUri)
        filePath = ctx.archives_dir() + '/' + fileName
	achv = archive.Archive(filePath, ctx.spec.source.archiveType)
	
	assert ctx.spec.source.archiveType == "targz"

	# unpacking is trivial with Archive()
	achv.unpack(targetDir)
	
	# but testing is hard
	# "var/tmp/pisi/popt-1.7-3/work" (targetDir)
	assert pathexists(targetDir + "/popt-1.7")

	testfile = targetDir + "/popt-1.7/Makefile.am"
	assert pathexists(testfile)
	
	# check file integrity
	self.assertEqual(util.sha1_file(testfile),
			 "5af9dd7d754f788cf511c57ce0af3d555fed009d")

    def testUnpackZip(self):
	ctx = context.Context("tests/sandbox/sandbox.pspec")
	fetch = fetcher.Fetcher(ctx)
	fetch.fetch()

	targetDir = ctx.pkg_work_dir()

	assert ctx.spec.source.archiveType == "zip"

        fileName = os.path.basename(ctx.spec.source.archiveUri)
        filePath = ctx.archives_dir() + '/' + fileName
	achv = archive.Archive(filePath, ctx.spec.source.archiveType)
	achv.unpack(targetDir)

	assert pathexists(targetDir + "/sandbox")

	testfile = targetDir + "/sandbox/borek.cs"
	assert pathexists(testfile)
	
	# check file integrity
	self.assertEqual(util.sha1_file(testfile),
			 "06d0ee5ba49eccae6bc20552d55b3ba5ad52995e")

	# check for symbolic links
	testfile = targetDir + "/sandbox/deneme/hed"
	assert islink(testfile)
	
    def testUnpackZipCond(self):
	ctx = context.Context("tests/sandbox/sandbox.pspec")
	fetch = fetcher.Fetcher(ctx)
	fetch.fetch()
	targetDir = ctx.pkg_work_dir()
	assert ctx.spec.source.archiveType == "zip"
        fileName = os.path.basename(ctx.spec.source.archiveUri)
        filePath = ctx.archives_dir() + '/' + fileName
	achv = archive.Archive(filePath, ctx.spec.source.archiveType)
	achv.unpack_files(["sandbox/borek.cd"], targetDir)
	assert pathexists(targetDir + "/sandbox")
	testfile = targetDir + "/sandbox/borek.cs"
	assert pathexists(testfile)


suite = unittest.makeSuite(ArchiveFileTestCase)
