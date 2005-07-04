# -*- coding: utf-8 -*-
# package bulding stuff
# maintainer: baris and meren

# python standard library
import os
import sys

import util
from ui import ui
from constants import const
from sourcearchive import SourceArchive
from files import Files, FileInfo
from metadata import MetaData
from package import Package

class PisiBuildError(Exception):
    pass


# Helper Functions
def getFileType(path, pinfoList):
    """Return the file type of a path according to the given PathInfo
    list"""
    # The usage of depth is somewhat confusing. It is used for finding
    # the best match to paths(in pinfolist). For an example, if paths
    # contain ['/usr/share','/usr/share/doc'] and path is
    # /usr/share/doc/filename our iteration over paths should match
    # the second item.
    depth = 0
    ftype = ""
    path = "/"+path # we need a real path.
    for pinfo in pinfoList:
        if util.subpath(pinfo.pathname, path):
            length = len(pinfo.pathname)
            if depth < length:
                depth = length
                ftype = pinfo.fileType
    return ftype

def checkPathCollision(package, pkgList):
    """This function will check for collision of paths in a package with
    the paths of packages in pkgList. The return value will be the
    list containing the paths that collide."""
    collisions = []
    for pinfo in package.paths:
        for pkg in pkgList:
            if pkg is package:
                continue
            for path in pkg.paths:
                # if pinfo.pathname is a subpath of path.pathname like
                # the example below. path.patname is marked as a
                # collide. Exp:
                # pinfo.pathname: /usr/share
                # path.pathname: /usr/share/doc
                if util.subpath(pinfo.pathname, path.pathname):
                    collisions.append(path.pathname)
    return collisions


class PisiBuild:
    """PisiBuild class, provides the package build and creation routines"""
    def __init__(self, buildcontext):
        self.ctx = buildcontext
        self.pspecDir = os.path.dirname(self.ctx.pspecfile)
        self.spec = self.ctx.spec
        self.sourceArchive = SourceArchive(self.ctx)

        self.setEnvorinmentVars()

        self.actionLocals = None
        self.actionGlobals = None
        self.srcDir = None

    def build(self):
        """Build the package in one shot."""
        ui.info("Building PISI source package: %s\n" % self.spec.source.name)

        ui.info("Fetching source from: %s\n" % self.spec.source.archiveUri)
        self.sourceArchive.fetch()
        ui.info("Source archive is stored: %s/%s\n"
                %(self.ctx.archives_dir(), self.spec.source.archiveName))
    
        self.solveBuildDependencies()

        ui.info("Unpacking archive...")
        self.sourceArchive.unpack()
        ui.info(" unpacked (%s)\n" % self.ctx.pkg_work_dir())

        self.compileActionScript()
        self.srcDir = self.pkgSrcDir()

        self.applyPatches()

        # we'll need our working directory after actionscript
        # finished its work in the archive source directory.
        curDir = os.getcwd()
        os.chdir(self.srcDir)

        #  Run configure, build and install phase
        ui.info("Setting up source...\n")
        self.runActionFunction(const.setup_func)
        ui.info("Building source...\n")
        self.runActionFunction(const.build_func)
        ui.info("Intalling...\n")
        # install function is mandatory!
        self.runActionFunction(const.install_func, True)

        os.chdir(curDir)

        # after all, we are ready to build/prepare the packages
        self.buildPackages()

    def setEnvorinmentVars(self):
        """Sets the environment variables for actions API to use"""
        evn = {
            "PKG_DIR": self.ctx.pkg_dir(),
            "WORK_DIR": self.ctx.pkg_work_dir(),
            "INSTALL_DIR": self.ctx.pkg_install_dir(),
            "SRC_NAME": self.spec.source.name,
            "SRC_VERSION": self.spec.source.version,
            "SRC_RELEASE": self.spec.source.release
            }
        os.environ.update(evn)

    def compileActionScript(self):
        try:
            specdir = os.path.dirname(self.ctx.pspecfile)
            self.actionScript = open(os.path.join(specdir,
                                                  const.actions_file)).read()
        except IOError, e:
            ui.error("Action Script: %s\n" % e)
            return

        localSymbols = globalSymbols = {}
        try:
            exec compile(self.actionScript, "error", "exec") in \
                                             localSymbols, globalSymbols
        except SyntaxError, e:
            ui.error ("Error : %s\n" % e)
            return
        self.actionLocals = localSymbols
        self.actionGlobals = globalSymbols
        
    def pkgSrcDir(self):
        """Returns the real path of WorkDir for an unpacked archive."""
        join = os.path.join
        if 'WorkDir' in self.actionGlobals:
            path = join(self.ctx.pkg_work_dir(),self.actionGlobals['WorkDir'])
        else:
            path = join(self.ctx.pkg_work_dir(), 
                        self.spec.source.name + "-" + self.spec.source.version)
            
        if not os.path.exists(path):
            ui.error ("No such file or directory: %s\n" % e)
            sys.exit(1)
        return path

    def runActionFunction(self, func, mandatory=False):
        """Calls the corresponding function in actions.py. 

        If mandatory parameter is True, and function is not present in
        actionLocals PisiBuildError will be raised."""
        if func in self.actionLocals:
            self.actionLocals[func]()
        else:
            if mandatory:
                PisiBuildError, "unable to call function from actions: %s" %func

    def solveBuildDependencies(self):
        """pre-alpha: fail if dependencies not satisfied"""
        pass

    def applyPatches(self):
        files_dir = os.path.abspath(os.path.join(self.pspecDir,
                                                 const.files_dir))

        for patch in self.spec.source.patches:
            patchFile = os.path.join(files_dir, patch.filename)
            if patch.compressionType:
                patchFile = util.uncompress(patchFile,
                                            compressType = patch.compressionType,
                                            targetDir=self.ctx.tmp_dir())

            ui.info("Applying patch: %s\n" % patch.filename)
            util.do_patch(self.srcDir, patchFile, level=patch.level)

    def genMetaDataXml(self, package):
        """Generate the metadata.xml file for build source.

        metadata.xml is composed of the information from specfile plus
        some additional information."""
        metadata = MetaData()
        metadata.fromSpec(self.spec.source, package)
        metadata.package.distribution = const.distribution
        metadata.package.distributionRelease = const.distributionRelease
        metadata.package.architecture = "Any"
        
        # FIXME: Bu hatalı. installsize'ı almak için tüm
        # pkg_install_dir()'ın boyutunu hesaplayamayız. Bir source
        # birden fazla kaynak üretebilir. package.paths ile
        # karşılaştırarak file listesinden boyutları hesaplatmalıyız.
        d = self.ctx.pkg_install_dir()
        size = util.dir_size(d)
        metadata.package.installedSize = str(size)
        metadata.write(os.path.join(self.ctx.pkg_dir(), const.metadata_xml))

    def genFilesXml(self, package):
        """Generetes files.xml using the path definitions in specfile and
        generated files by the build system."""
        files = Files()
        install_dir = self.ctx.pkg_install_dir()
        collisions = checkPathCollision(package,
                                        self.spec.packages)
        for pinfo in package.paths:
            path = install_dir + pinfo.pathname
            for fpath, fhash in util.get_file_hashes(path, collisions, install_dir):
                frpath = util.removepathprefix(install_dir, fpath) # relative path
                ftype = getFileType(frpath, package.paths)
                try: # broken links can cause problem
                    fsize = str(os.path.getsize(fpath))
                except OSError:
                    fsize = "0"
                files.append(FileInfo(frpath, ftype, fsize, fhash))

        files.write(os.path.join(self.ctx.pkg_dir(), const.files_xml))

    def buildPackages(self):
        """Build each package defined in PSPEC file. After this process there
        will be .pisi files hanging around, AS INTENDED ;)"""
        for package in self.spec.packages:
            ui.info("** Building package %s\n" % package.name);
            
            ui.info("Generating %s..." % const.metadata_xml)
            self.genMetaDataXml(package)
            ui.info(" done.\n")

            ui.info("Generating %s..." % const.files_xml)
            self.genFilesXml(package)
            ui.info(" done.\n")

            # testing
            pkgName = package.name + '-' + self.spec.source.version +\
                '-' + self.spec.source.release + ".pisi"
            
            ui.info("Creating PISI package %s\n" % pkgName)
            
            pkg = Package(pkgName, 'w')
            c = os.getcwd()

            os.chdir(self.ctx.pkg_dir())
            pkg.add_to_package(const.metadata_xml)
            pkg.add_to_package(const.files_xml)

            # Now it is time to add files to the packages using newly
            # created files.xml
            files = Files()
            files.read(const.files_xml)
            for finfo in files.list:
                pkg.add_to_package("install/" + finfo.path)

            pkg.close()
            os.chdir(c)
