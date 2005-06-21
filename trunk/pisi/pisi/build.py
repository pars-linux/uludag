# -*- coding: utf-8 -*-
# package bulding stuff
# maintainer: baris and meren

# python standard library
import os
import sys

# import pisipackage
import util
from ui import ui
from context import ctx
from sourcearchive import SourceArchive

class PisiBuildError(Exception):
    pass

class PisiBuild:
    """PisiBuild class, provides the package build and creation routines"""
    def __init__(self, context):
        self.ctx = context
	self.work_dir = self.ctx.pkg_work_dir()
        self.spec = self.ctx.spec
        self.sourceArchive = SourceArchive(self.ctx)

    def build(self):
        ui.info("Building PISI source package: %s\n" % self.spec.source.name)

        ui.info("Fetching source from: %s\n" % self.spec.source.archiveUri)
        self.sourceArchive.fetch()
        ui.info("Source archive is stored: %s/%s\n"
                %(self.ctx.archives_dir(), self.spec.source.archiveName))
	
	self.solveBuildDependencies()

	ui.info("Unpacking archive...")
	self.sourceArchive.unpack()
	ui.info(" unpacked (%s)\n" % self.ctx.pkg_work_dir())

	self.applyPatches()

	try:
	    specdir = os.path.dirname(self.ctx.pspecfile)
	    self.actionScript = open("/".join([specdir,self.ctx.const.actions_file])).read()
	except IOError, e:
	    ui.error ("Action Script: %s\n" % e)
	    return 

	#we'll need this our working directory after actionscript
	#finished its work in the work_dir
	curDir = os.getcwd()

	# FIXME: It's wrong to assume that unpacked archive 
	# will create a name-version top-level directory.
	# Archive module should give the exact location.
	# (from the assumption is evil dept.)
	os.chdir(self.ctx.pkg_work_dir() + "/" + self.spec.source.name + "-" + self.spec.source.version)
	locals = globals = {}
	
	try:
	    exec compile(self.actionScript , "error", "exec") in locals,globals
	except SyntaxError, e:
	    ui.error ("Error : %s\n" % e)
	    return 
		
	self.configureSource(locals)
	self.buildSource(locals)
	self.installSource(locals)

	os.chdir(curDir)
	# after all, we are ready to build/prepare the packages
	self.buildPackages()

    def solveBuildDependencies(self):
    	pass

    def applyPatches(self):
        pass

    def configureSource(self, locals):
	func = self.ctx.const.setup_func
	if func in locals:
	    ui.info("Configuring %s...\n" % self.spec.source.name)
	    locals[func]()

    def buildSource(self, locals):
	func = self.ctx.const.build_func
	if func in locals:
	    ui.info("Building %s...\n" % self.spec.source.name)
	    locals[func]()

    def installSource(self, locals):
	func = self.ctx.const.install_func
	if func in locals:
	    ui.info("Installing %s...\n" % self.spec.source.name)
	    locals[func]()
	    
    def genMetaDataXml(self, package):
	#test
	d = self.ctx.pkg_install_dir()
	c = util.dir_size(d)
	print d, c

    def genFilesXml(self, package):
	# the worst function in this project!
	# just testing...
	install_dir = self.ctx.pkg_install_dir()
	for fpath, fhash in util.get_file_hashes(install_dir):
	    # get the relative path
	    fpath = fpath[len(install_dir):]

	    depth = 0
	    ftype = ""
	    for path in package.paths:
		if fpath.startswith(path.pathname):
		    if depth < len(path.pathname):
			depth = len(path.pathname)
			ftype = path.fileType
	    print fpath, ftype, fhash

    def buildPackages(self):
        for package in self.spec.packages:
            ui.info("** Building package %s\n" % package.name);
	    self.genMetaDataXml(package)
	    self.genFilesXml(package)
    
