# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#
# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr>

"""Top level PISI interfaces. a facade to the entire PISI system"""

import os
import sys
ver = sys.version_info
if ver[0] <= 2 and ver[1] < 4:
    from sets import Set as set
    
import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi

import pisi.context as ctx
from pisi.uri import URI
import pisi.util as util
import pisi.dependency as dependency
import pisi.pgraph as pgraph
import pisi.operations as operations
import pisi.packagedb as packagedb
import pisi.repodb
import pisi.installdb
from pisi.index import Index
import pisi.cli

class Error(pisi.Error):
    pass


def init(database = True, options = None, ui = None, comar = True):
    """Initialize PiSi subsystem"""

    import pisi.config
    ctx.config = pisi.config.Config(options)

    # TODO: this is definitely not dynamic beyond this point!
    ctx.comar = comar and not ctx.config.get_option('ignore_comar')

    if ui is None:
        if options:
            pisi.context.ui = pisi.cli.CLI(options.debug)
        else:
            pisi.context.ui = pisi.cli.CLI()
    else:
        pisi.context.ui = ui

    # initialize repository databases
    if database:
        ctx.repodb = pisi.repodb.init()
        ctx.installdb = pisi.installdb.init()
        ctx.filesdb = pisi.files.FilesDB()

        # TODO: bunun da ctx'de olmasi gerek, global hesabi
        packagedb.init()
#        import pisi.sourcedb
#        pisi.sourcedb.init()

def install(packages):
    """install a list of packages (either files/urls, or names)"""

    # FIXME: this function name "install" makes impossible to import
    # and use install module directly.
    from install import Error as InstallError

    try:
        # determine if this is a list of files/urls or names
        if packages[0].endswith('.pisi'): # they all have to!
            return install_pkg_files(packages)
        else:
            return install_pkg_names(packages)

    #FIXME: As Gurer warns, something's fishy with this exception proc.
    except InstallError, e:
        # FIXME: This is a workaround for __str__ conversion used in
        # Python exceptions
        ctx.ui.error(e.args[0])

    except packagedb.Error, e:
        # FIXME: same workaround...
        ctx.ui.error("PackageDBError: (%s)" % e.args[0])
        ctx.ui.error(_("Package is not installable."))

    #except Exception, e:
    #    print e
    #    ctx.ui.error("Error: %s" % e)

def install_pkg_files(package_URIs):
    """install a number of pisi package files"""
    from package import Package

    ctx.ui.debug('A = %s' % str(package_URIs))

    for x in package_URIs:
        if not x.endswith(ctx.const.package_prefix):
            ctx.ui.error(_('Mixing file names and package names not supported YET.'))
            return False

    if ctx.config.get_option('ignore_dependency'):
        # simple code path then
        for x in package_URIs:
            operations.install_single_file(x)
        return True
            
    # read the package information into memory first
    # regardless of which distribution they come from
    d_t = {}
    dfn = {}
    for x in package_URIs:
        package = Package(x)
        package.read()
        name = str(package.metadata.package.name)
        d_t[name] = package.metadata.package
        dfn[name] = x

    def satisfiesDep(dep):
        return dependency.installed_satisfies_dep(dep) \
               or dependency.dict_satisfies_dep(d_t, dep)
            
    # for this case, we have to determine the dependencies
    # that aren't already satisfied and try to install them 
    # from the repository
    dep_unsatis = []
    for name in d_t.keys():
        pkg = d_t[name]
        deps = pkg.runtimeDeps
        for dep in deps:
            if not satisfiesDep(dep):
                dep_unsatis.append(dep)

    # now determine if these unsatisfied dependencies could
    # be satisfied by installing packages from the repo

    # if so, then invoke install_pkg_names
    extra_packages = [x.package for x in dep_unsatis]
    if (extra_packages and install_pkg_names(extra_packages)) or \
           (not extra_packages):
    
        class PackageDB:
            def __init__(self):
                self.d = d_t
            
            def get_package(self, key):
                return d_t[str(key)]
        
        packagedb = PackageDB()
       
        A = d_t.keys()
       
        if len(A)==0:
            ctx.ui.info(_('No packages to install.'))
            return True
        
        # try to construct a pisi graph of packages to
        # install / reinstall
    
        G_f = pgraph.PGraph(packagedb)               # construct G_f
    
        # find the "install closure" graph of G_f by package 
        # set A using packagedb
        #print A
        for x in A:
            G_f.add_package(x)
        B = A
        #state = {}
        while len(B) > 0:
            Bp = set()
            for x in B:
                pkg = packagedb.get_package(x)
                #print pkg
                for dep in pkg.runtimeDeps:
                    #print 'checking ', dep
                    if dependency.dict_satisfies_dep(d_t, dep):
                        if not dep.package in G_f.vertices():
                            Bp.add(str(dep.package))
                        G_f.add_dep(x, dep)
            B = Bp
        if ctx.config.get_option('debug'):
            G_f.write_graphviz(sys.stdout)
        order = G_f.topological_sort()
        order.reverse()
        #if ctx.config.get_option('debug'):
        #    print 'installation order', order
        for x in order:
            operations.install_single_file(dfn[x])
    else:
        raise Error(_('External dependencies not satisfied'))

    return True # everything went OK.

def install_pkg_names(A):
    """This is the real thing. It installs packages from
    the repository, trying to perform a minimum number of
    installs"""

    A_0 = A = set(A) # A was a list, remove duplicates

    ctx.ui.debug('A = %s' % str(A))

    if len(A)==0:
        ctx.ui.info(_('No packages to install.'))
        return True
    
    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(packagedb)               # construct G_f

    # find the "install closure" graph of G_f by package 
    # set A using packagedb
    #print A
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = packagedb.get_package(x)
            #print pkg
            for dep in pkg.runtimeDeps:
                ctx.ui.debug('checking %s' % str(dep))
                # we don't deal with already *satisfied* dependencies
                if not dependency.installed_satisfies_dep(dep):
                    if not dep.package in G_f.vertices():
                        Bp.add(str(dep.package))
                    G_f.add_dep(x, dep)
        B = Bp
    if ctx.config.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    order.reverse()
    ctx.ui.info(_("""\
The following minimal list of packages will be installed \
in the respective order to satisfy dependencies: """) + util.strlist(order))
    if len(order) > len(A_0):
        if not ctx.ui.confirm('Do you want to continue?'):
            return False
    for x in order:
        operations.install_single_name(x)
        
    return True                         # everything went OK :)

def package_graph(A, ignore_installed = False):
    """Construct a package relations graph, containing
    all dependencies of packages A, if ignore_installed
    option is True, then only uninstalled deps will
    be added."""

    ctx.ui.debug('A = %s' % str(A))
  
    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(packagedb)               # construct G_f

    # find the "install closure" graph of G_f by package 
    # set A using packagedb
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = packagedb.get_package(x)
            #print pkg
            for dep in pkg.runtimeDeps:
                if ignore_installed:
                    if dependency.installed_satisfies_dep(dep):
                        continue
                if not dep.package in G_f.vertices():
                    Bp.add(str(dep.package))
                G_f.add_dep(x, dep)
        B = Bp
    return G_f

def upgrade(A):
    upgrade_pkg_names(A)

def upgrade_pkg_names(A):
    """Re-installs packages from the repository, trying to perform
    a maximum number of upgrades."""
    
    ignore_build = ctx.config.options and ctx.config.options.ignore_build_no

    # filter packages that are not upgradable
    A_0 = A = set(A)
    Ap = []
    for x in A:
        if x.endswith('.pisi'):
            ctx.ui.debug(_("Warning: package *name* ends with '.pisi'"))
        if not ctx.installdb.is_installed(x):
            ctx.ui.info(_('Package %s is not installed.') % x)
            continue
        (version, release, build) = ctx.installdb.get_version(x)
        pkg = packagedb.get_package(x)

        # First check version. If they are same, check release. Again
        # if releases are same and checking buildno is premitted,
        # check build number.
        if version < pkg.version:
            Ap.append(x)
        elif version == pkg.version:
            if release < pkg.release:
                Ap.append(x)
            if release == pkg.release and build and not ignore_build:
                if build < pkg.build:
                    Ap.append(x)
        else:
            #ctx.ui.info('Package %s cannot be upgraded. ' % x)
            ctx.ui.info(_('Package %s is already at its latest \
version %s, release %s, build %s.')
                    % (x, pkg.version, pkg.release, pkg.build))
    A = set(Ap)

    if len(A)==0:
        ctx.ui.info(_('No packages to upgrade.'))
        return True

    ctx.ui.debug('A = %s' % str(A))
    
    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(packagedb)               # construct G_f

    # find the "install closure" graph of G_f by package 
    # set A using packagedb
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = packagedb.get_package(x)
            #print pkg
            for dep in pkg.runtimeDeps:
                #print 'checking ', dep
                # add packages that can be upgraded
                if dependency.repo_satisfies_dep(dep):
                    if ctx.installdb.is_installed(dep.package):
                        (v,r,b) = ctx.installdb.get_version(dep.package)
                        rep_pkg = packagedb.get_package(dep.package)
                        (vp,rp,bp) = (rep_pkg.version, rep_pkg.release, 
                                      rep_pkg.build)
                        if ignore_build or (not b) or (not bp):
                            # if we can't look at build
                            if r >= rp:     # installed already new
                                continue
                        elif b and bp and b >= bp:
                            continue
                    if not dep.package in G_f.vertices():
                        Bp.add(str(dep.package))
                    G_f.add_dep(x, dep)
        B = Bp
    if ctx.options.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    order.reverse()
    ctx.ui.info(_("""The following packages will be upgraded: """) +
                util.strlist(order))
    if len(order) > len(A_0):
        if not ctx.ui.confirm('Do you want to continue?'):
            return False
    for x in order:
        operations.install_single_name(x, True)
        
    return True                         # everything went OK :)

def list_upgradable():
    ignore_build = ctx.config.options and ctx.config.options.ignore_build_no

    A = ctx.installdb.list_installed()
    # filter packages that are not upgradable
    Ap = []
    for x in A:
        if not ctx.installdb.is_installed(x):
            continue
        (version, release, build) = ctx.installdb.get_version(x)
        pkg = packagedb.get_package(x)
        if ignore_build or (not build):
            if release < pkg.release:
                Ap.append(x)
        elif build < pkg.build:
                Ap.append(x)
        else:
            pass
            #ctx.ui.info('Package %s cannot be upgraded. ' % x)
    return Ap

def remove(A):
    """remove set A of packages from system (A is a list of package names)"""
    
    # filter packages that are not installed
    A_0 = A = set(A)
    Ap = []
    for x in A:
        if ctx.installdb.is_installed(x):
            Ap.append(x)
        else:
            ctx.ui.info(_('Package %s does not exist. Cannot remove.') % x)
    A = set(Ap)

    if len(A)==0:
        ctx.ui.info(_('No packages to remove.'))
        return True
        
    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(packagedb)               # construct G_f

    # find the (install closure) graph of G_f by package 
    # set A using packagedb
    #print A
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = packagedb.get_package(x)
            #print 'processing', pkg.name
            rev_deps = packagedb.get_rev_deps(x)
            for (rev_dep, depinfo) in rev_deps:
                #print 'checking ', rev_dep
                # we don't deal with unsatisfied dependencies
                if dependency.installed_satisfies_dep(depinfo):
                    if not rev_dep in G_f.vertices():
                        Bp.add(rev_dep)
                        G_f.add_plain_dep(rev_dep, x)
        B = Bp
    if ctx.config.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    ctx.ui.info(_("""\
The following minimal list of packages will be removed \ 
in the respective order to satisfy dependencies: """) + util.strlist(order))
    if len(order) > len(A_0):
        if not ctx.ui.confirm('Do you want to continue?'):
            return False
    for x in order:
        if ctx.installdb.is_installed(x):
            operations.remove_single(x)
        else:
            ctx.ui.info(_('Package %s is not installed. Cannot remove.') % x)
        
    return True                         # everything went OK :)

def configure_pending():
    # start with pending packages
    # configure them in reverse topological order of dependency
    A = ctx.installdb.list_pending()
    #print A
    G_f = pgraph.PGraph(packagedb)               # construct G_f
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = packagedb.get_package(x)
            #print pkg
            for dep in pkg.runtimeDeps:
                if dep.package in G_f.vertices():
                    G_f.add_dep(x, dep)
        B = Bp
    G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    order.reverse()
    #print order
    try:
        import pisi.comariface as comariface
        for x in order:
            comariface.run_postinstall(x)
    except ImportError:
        raise Error(_("COMAR: comard not fully installed"))
    

def info(package):
    if package.endswith(ctx.const.package_prefix):
        return info_file(package)
    else:
        return info_name(package)
    
def info_file(package_fn):
    from package import Package

    if not os.path.exists(package_fn):
        raise Error (_('File %s not found') % package_fn)

    package = Package(package_fn)
    package.read()
    return package.metadata, package.files

def info_name(package_name):
    """fetch package information for a package"""
    if packagedb.has_package(package_name):
        package = packagedb.get_package(package_name)
        from pisi.metadata import MetaData
        metadata = MetaData()
        metadata.package = package
        #FIXME: get it from sourcedb
        metadata.source = None
        #TODO: fetch the files from server if possible
        if ctx.installdb.is_installed(package.name):
            files = ctx.installdb.files(package.name)
        else:
            files = None
        return metadata, files
    else:
        raise Error(_('Package %s not found') % package_name)

def index(repo_dir = '.'):

    ctx.ui.info(_('* Building index of PISI files under %s') % repo_dir)
    index = Index()
    index.index(repo_dir)
    index.write(ctx.const.pisi_index)
    ctx.ui.info(_('* Index file written'))


def add_repo(name, indexuri):
    repo = pisi.repodb.Repo(URI(indexuri))
    ctx.repodb.add_repo(name, repo)

def remove_repo(name):
    if ctx.repodb.has_repo(name):
        ctx.repodb.remove_repo(name)
    else:
        ctx.ui.error(_('* Repository %s does not exist. Cannot remove.') 
                 % name)

def update_repo(repo):

    ctx.ui.info(_('* Updating repository: %s') % repo)
    index = Index()
    index.read(ctx.repodb.get_repo(repo).indexuri.get_uri(), repo)
    index.update_db(repo)
    ctx.ui.info(_('\n* Package database updated.'))


# build functions...
def prepare_for_build(pspecfile, authInfo=None):

    # FIXME: there is a function named "build" in this module which
    # makes it impossible to use build module directly.
    from build import PisiBuild

    url = URI(pspecfile)
    if url.is_remote_file():
        from sourcefetcher import SourceFetcher
        fs = SourceFetcher(url, authInfo)
        url.uri = fs.fetch_all()

    pb = PisiBuild(url.uri)

    # find out the build dependencies that are not satisfied...
    dep_unsatis = []
    for dep in pb.spec.source.buildDeps:
        if not dependency.installed_satisfies_dep(dep):
            dep_unsatis.append(dep)

    # FIXME: take care of the required buildDeps...
    # For now just report an error!
    if dep_unsatis:
        ctx.ui.error(_("Unsatisfied Build Dependencies:"))
        for dep in dep_unsatis:
            ctx.ui.warning(dep.package)

    # FIXME: Don't exit for now! It's annoying to test on a system that
    # doesn't has all packages made with pisi.
    # Will be enabled on the full-pisi system.
    #        sys.exit(1)

    return pb

def build(pspecfile, authInfo=None):
    pb = prepare_for_build(pspecfile, authInfo)
    pb.build()


order = {"none": 0,
         "unpack": 1,
         "setupaction": 2,
         "buildaction": 3,
         "installaction": 4,
         "buildpackages": 5}

def __buildState_unpack(pb):
    # unpack is the first state to run.
    pb.fetch_source_archive()
    pb.unpack_source_archive()
    pb.apply_patches()

def __buildState_setupaction(pb, last):

    if order[last] < order["unpack"]:
        __buildState_unpack(pb)
    pb.run_setup_action()

def __buildState_buildaction(pb, last):

    if order[last] < order["setupaction"]:
        __buildState_setupaction(pb, last)
    pb.run_build_action()

def __buildState_installaction(pb, last):
    
    if order[last] < order["buildaction"]:
        __buildState_buildaction(pb, last)
    pb.run_install_action()

def __buildState_buildpackages(pb, last):

    if order[last] < order["installaction"]:
        __buildState_installaction(pb, last)
    pb.build_packages()

def build_until(pspecfile, state, authInfo=None):
    pb = prepare_for_build(pspecfile, authInfo)
    pb.compile_action_script()
    
    last = pb.get_state()
    ctx.ui.info("Last state was %s"%last)

    if not last: last = "none"

    if state == "unpack":
        __buildState_unpack(pb)
        return

    if state == "setupaction":
        __buildState_setupaction(pb, last)
        return
    
    if state == "buildaction":
        __buildState_buildaction(pb, last)
        return

    if state == "installaction":
        __buildState_installaction(pb, last)
        return

    __buildState_buildpackages(pb, last)

def delete_cache():
    util.clean_dir(ctx.config.packages_dir())
    util.clean_dir(ctx.config.archives_dir())
    util.clean_dir(ctx.config.tmp_dir())
