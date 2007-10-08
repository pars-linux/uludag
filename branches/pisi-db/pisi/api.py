# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

"""Top level PiSi interfaces. a facade to the entire PiSi system"""

import os
import sys
import logging
import logging.handlers

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi
import pisi.context as ctx
import pisi.uri
import pisi.util
import pisi.dependency as dependency
import pisi.pgraph as pgraph
import pisi.db.packagedb
import pisi.db.repodb
import pisi.db.filesdb
import pisi.db.installdb
import pisi.db.sourcedb
import pisi.db.componentdb
import pisi.index
import pisi.config
import pisi.metadata
import pisi.file
import pisi.version
import pisi.atomicoperations
import pisi.operations.delta
import pisi.operations.remove
import pisi.operations.upgrade
import pisi.operations.install
import pisi.operations.helper
import pisi.operations.emerge
import pisi.operations.build
import pisi.comariface
import pisi.signalhandler

class Error(pisi.Error):
    pass

def set_userinterface(ui):
    ctx.ui = ui

def set_io_streams(stdout=None, stderr=None)
    if stdout:
        ctx.stdout = stdout
    if stderr:
        ctx.stderr = stderr

def set_comar_sockname(sockname):
    ctx.comar_sockname = comar_sockname

def init(database = True, write = True,
         options = pisi.config.Options(), ui = None, comar = True,
         stdout = None, stderr = None,
         comar_sockname = None,
         signal_handling = True):

    # FIXME: something is wrong here... see __init__.py also. Why do we import pisi.api in __init__.py
    import pisi.config
    ctx.config = pisi.config.Config(options)

    if os.access('%s/var/log' % ctx.config.log_dir(), os.W_OK):
        handler = logging.handlers.RotatingFileHandler('%s/var/log/pisi.log' % ctx.config.log_dir())
        #handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-12s: %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        ctx.log = logging.getLogger('pisi')
        ctx.log.addHandler(handler)
        ctx.loghandler = handler
        ctx.log.setLevel(logging.DEBUG)
    else:
        ctx.log = None

    if signal_handling:
        ctx.sig = pisi.signalhandler.SignalHandler()

    # TODO: this is definitely not dynamic beyond this point!
    ctx.comar = comar and not ctx.config.get_option('ignore_comar')

    ctx.ui.debug('PiSi API initialized')
    ctx.initialized = True

def _cleanup():
    """Close the database cleanly and do other cleanup."""
    if ctx.initialized:
        ctx.disable_keyboard_interrupts()
        if ctx.log:
            ctx.loghandler.flush()
            ctx.log.removeHandler(ctx.loghandler)
            
        filesdb = pisi.db.filesdb.FilesDB()
        filesdb.close()

        if ctx.build_leftover and os.path.exists(ctx.build_leftover):
            os.unlink(ctx.build_leftover)

        ctx.ui.debug('PiSi API finalized')
        ctx.ui.close()
        ctx.initialized = False
        ctx.enable_keyboard_interrupts()

def list_pending():
    """Return a set of configuration pending package names."""
    installdb = pisi.db.installdb.InstallDB()
    return set(installdb.list_pending())

def list_installed():
    """Return a set of installed package names."""
    installdb = pisi.db.installdb.InstallDB()
    return set(installdb.list_installed())

def list_replaces(repo = None):
    """Returns a dict of the replaced packages."""
    packagedb = pisi.db.packagedb.PackageDB()
    return packagedb.get_replaces(repo = repo)

def list_available(repo = None):
    """Return a set of available package names."""
    packagedb = pisi.db.packagedb.PackageDB()
    return set(packagedb.list_packages(repo = repo))

def list_upgradable():
    installdb = pisi.db.installdb.InstallDB()
    packagedb = pisi.db.packagedb.PackageDB()
    return filter(pisi.operations.upgrade.is_upgradable, installdb.list_installed()) + packagedb.get_replaces().keys()

def package_graph(A, packagedb, ignore_installed = False):
    """Construct a package relations graph.
    
    Graph will contain all dependencies of packages A, if ignore_installed
    option is True, then only uninstalled deps will be added.
    
    """

    ctx.ui.debug('A = %s' % str(A))

    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(packagedb)             # construct G_f

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
            for dep in pkg.runtimeDependencies():
                if ignore_installed:
                    if dependency.installed_satisfies_dep(dep):
                        continue
                if not dep.package in G_f.vertices():
                    Bp.add(str(dep.package))
                G_f.add_dep(x, dep)
        B = Bp
    return G_f

def generate_install_order(A):
    # returns the install order of the given install package list with any extra
    # dependency that is also going to be installed
    G_f, order = plan_install(A, ignore_package_conflicts = True)
    return order

def generate_remove_order(A):
    # returns the remove order of the given removal package list with any extra
    # reverse dependency that is also going to be removed
    G_f, order = plan_remove(A)
    return order

def generate_upgrade_order(A):
    # returns the upgrade order of the given upgrade package list with any needed extra
    # dependency
    G_f, order = plan_upgrade(A)
    return order

def generate_base_upgrade(A):
    # all the packages of the system.base must be installed on the system.
    # method returns the currently needed system.base component install and 
    # upgrade needs
    base = upgrade_base(A, ignore_package_conflicts = True)
    return list(base)

def generate_conflicts(A):
    # returns the conflicting packages list of the to be installed packages.
    # @conflicting_pkgs: conflicting and must be removed packages list to proceed
    # @conflicts_inorder: list of the conflicting packages _with each other_ in the to be installed list
    # @conflicting_pairs: dictionary that contains which package in the to be installed list conflicts
    #     with which packages
    packagedb = pisi.db.packagedb.PackageDB()
    (conflicting_pkgs, conflicts_inorder, conflicting_pairs) = pisi.conflict.calculate_conflicts(A, packagedb)
    return (conflicting_pkgs, conflicts_inorder, conflicting_pairs)

def generate_pending_order(A):
    # returns pending package list in reverse topological order of dependency
    installdb = pisi.db.installdb.InstallDB()
    G_f = pgraph.PGraph(installdb) # construct G_f
    for x in A:
        G_f.add_package(x)
    B = A
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = installdb.get_package(x)
            for dep in pkg.runtimeDependencies():
                if dep.package in G_f.vertices():
                    G_f.add_dep(x, dep)
        B = Bp
    if ctx.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    order.reverse()

    componentdb = pisi.db.componentdb.ComponentDB()
    # Bug 4211
    if componentdb.has_component('system.base'):
        order = reorder_base_packages(order)

    return order

def configure_pending():
    # start with pending packages
    # configure them in reverse topological order of dependency
    installdb = pisi.db.installdb.InstallDB()
    A = installdb.list_pending()
    order = generate_pending_order(A)
    try:
        for x in order:
            if installdb.has_package(x):
                pkginfo = installdb.get_package(x)
                pkgname = pisi.util.package_name(x, pkginfo.version,
                                        pkginfo.release,
                                        False,
                                        False)
                pkg_path = pisi.util.join_path(ctx.config.lib_dir(),
                                          'package', pkgname)
                m = pisi.metadata.MetaData()
                metadata_path = pisi.util.join_path(pkg_path, ctx.const.metadata_xml)
                m.read(metadata_path)
                # FIXME: we need a full package info here!
                pkginfo.name = x
                ctx.ui.notify(pisi.ui.configuring, package = pkginfo, files = None)
                pisi.comariface.post_install(
                    pkginfo.name,
                    m.package.providesComar,
                    pisi.util.join_path(pkg_path, ctx.const.comar_dir),
                    pisi.util.join_path(pkg_path, ctx.const.metadata_xml),
                    pisi.util.join_path(pkg_path, ctx.const.files_xml),
                )
                ctx.ui.notify(pisi.ui.configured, package = pkginfo, files = None)
            installdb.clear_pending(x)
    except ImportError:
        raise Error(_("comar package is not fully installed"))

def info(package, installed = False):
    if package.endswith(ctx.const.package_suffix):
        return info_file(package)
    else:
        metadata, files, repo = info_name(package, installed)
        return metadata, files

def info_file(package_fn):

    if not os.path.exists(package_fn):
        raise Error (_('File %s not found') % package_fn)

    package = pisi.package.Package(package_fn)
    package.read()
    return package.metadata, package.files

def info_name(package_name, useinstalldb=False):
    """Fetch package information for the given package."""

    installdb = pisi.db.installdb.InstallDB()
    packagedb = pisi.db.packagedb.PackageDB()
    if useinstalldb:
        package = installdb.get_package(package_name)
        repo = None
    else:
        package, repo = packagedb.get_package_repo(package_name)

    metadata = pisi.metadata.MetaData()
    metadata.package = package
    #FIXME: get it from sourcedb if available
    metadata.source = None
    #TODO: fetch the files from server if possible (wow, you maniac -- future exa)
    if useinstalldb and installdb.has_package(package.name):
        try:
            files = installdb.get_files(package.name)
        except pisi.Error, e:
            ctx.ui.warning(e)
            files = None
    else:
        files = None
    return metadata, files, repo

def search_package_terms(terms, repo = None):
    packagedb = pisi.db.packagedb.PackageDB()
    return search_in_packages(terms, packagedb.list_packages(repo), repo)

def search_in_packages(terms, packages, repo = None):

    def search(package, term):
        term = unicode(term).lower()
        if term in unicode(package.name).lower() or \
                term in unicode(package.summary).lower() or \
                term in unicode(package.description).lower():
            return True

    packagedb = pisi.db.packagedb.PackageDB()
    found = []
    for name in packages:
        pkg = packagedb.get_package(name, repo)
        if terms == filter(lambda x:search(pkg, x), terms):
            found.append(name)

    return found

def check(package):
    md, files = info(package, True)
    corrupt = []
    for f in files.list:
        if f.hash and f.type != "config" \
           and not os.path.islink('/' + f.path):
            ctx.ui.info(_("Checking /%s ") % f.path, noln=True, verbose=True)
            try:
                if f.hash != pisi.util.sha1_file('/' + f.path):
                    corrupt.append(f)
                    ctx.ui.error(_("\nCorrupt file: %s") % f)
                else:
                    ctx.ui.info(_("OK"), verbose=True)
            except pisi.util.FileError,e:
                ctx.ui.error("\n%s" % e)
    return corrupt

def index(dirs=None, output='pisi-index.xml', skip_sources=False, skip_signing=False):
    """Accumulate PiSi XML files in a directory, and write an index."""
    index = pisi.index.Index()
    index.distribution = None
    if not dirs:
        dirs = ['.']
    for repo_dir in dirs:
        repo_dir = str(repo_dir)
        ctx.ui.info(_('* Building index of PiSi files under %s') % repo_dir)
        index.index(repo_dir, skip_sources)

    if skip_signing:
        index.write(output, sha1sum=True, compress=pisi.file.File.bz2, sign=None)
    else:
        index.write(output, sha1sum=True, compress=pisi.file.File.bz2, sign=pisi.file.File.detached)
    ctx.ui.info(_('* Index file written'))

def add_repo(name, indexuri, at = None):
    repodb = pisi.db.repodb.RepoDB()
    if repodb.has_repo(name):
        raise Error(_('Repo %s already present.') % name)
    else:
        repo = pisi.db.repodb.Repo(pisi.uri.URI(indexuri))
        repodb.add_repo(name, repo, at = at)
        ctx.ui.info(_('Repo %s added to system.') % name)

def remove_repo(name):
    repodb = pisi.db.repodb.RepoDB()
    if repodb.has_repo(name):
        repodb.remove_repo(name)
        ctx.ui.info(_('Repo %s removed from system.') % name)
    else:
        ctx.ui.error(_('Repository %s does not exist. Cannot remove.')
                 % name)

def list_repos():
    repodb = pisi.db.repodb.RepoDB()
    return repodb.list_repos()

def update_repo(repo, force=False):
    ctx.ui.info(_('* Updating repository: %s') % repo)
    ctx.ui.notify(pisi.ui.updatingrepo, name = repo)
    repodb = pisi.db.repodb.RepoDB()
    index = pisi.index.Index()
    if repodb.has_repo(repo):
        repouri = repodb.get_repo(repo).indexuri.get_uri()
        try:
            index.read_uri_of_repo(repouri, repo)
        except pisi.file.AlreadyHaveException, e:
            ctx.ui.info(_('No updates available for repository %s.') % repo)
            if force:
                ctx.ui.info(_('Updating database at any rate as requested'))
                index.read_uri_of_repo(repouri, repo, force = force)
            else:
                return

        try:
            index.check_signature(repouri, repo)
        except pisi.file.NoSignatureFound, e:
            ctx.ui.warning(e)

        ctx.ui.info(_('* Package database updated.'))
    else:
        raise Error(_('No repository named %s found.') % repo)

def delete_cache():
    pisi.util.clean_dir(ctx.config.packages_dir())
    pisi.util.clean_dir(ctx.config.archives_dir())
    pisi.util.clean_dir(ctx.config.tmp_dir())

def rebuild_repo(repo):
    ctx.ui.info(_('* Rebuilding \'%s\' named repo... ') % repo)

    repodb = pisi.db.repodb.RepoDB()
    if repodb.has_repo(repo):
        repouri = pisi.uri.URI(repodb.get_repo(repo).indexuri.get_uri())
        indexname = repouri.filename()
        index = pisi.index.Index()
        indexpath = pisi.util.join_path(ctx.config.index_dir(), repo, indexname)
        tmpdir = os.path.join(ctx.config.tmp_dir(), 'index')
        pisi.util.clean_dir(tmpdir)
        pisi.util.check_dir(tmpdir)
        try:
            index.read_uri(indexpath, tmpdir, force=True) # don't look for sha1sum there
        except IOError, e:
            ctx.ui.warning(_("Input/Output error while reading %s: %s") % (indexpath, unicode(e)))
            return
    else:
        raise Error(_('No repository named %s found.') % repo)

def rebuild_db(files=False):

    filesdb = pisi.db.filesdb.FilesDB()
    installdb = pisi.db.installdb.InstallDB()

    def rebuild_filesdb():
        for pkg in list_installed():
            ctx.ui.info(_('* Adding \'%s\' to db... ') % pkg, noln=True)
            files = installdb.get_files(pkg)
            filesdb.add_files(pkg, files)
            ctx.ui.info(_('OK.'))

    # save parameters and shutdown pisi
    options = ctx.config.options
    ui = ctx.ui
    comar = ctx.comar
    _cleanup()

    filesdb.destroy()
    filesdb.init()

    # construct new database
    init(database=True, options=options, ui=ui, comar=comar)
    rebuild_filesdb()

############# FIXME: this was a quick fix. ##############################

# api was importing other module's functions and providing them as api functions. This is wrong.
# these are quick fixes for this problem. The api functions should be in this module.

# from pisi.operations import install, remove, upgrade, emerge
# from pisi.operations import plan_install_pkg_names as plan_install
# from pisi.operations import plan_remove, plan_upgrade, upgrade_base, calculate_conflicts, reorder_base_packages
# from pisi.build import build_until
# from pisi.atomicoperations import resurrect_package, build

def install(*args, **kw):
    return pisi.operations.install.install(*args, **kw)

def remove(*args, **kw):
    return pisi.operations.remove.remove(*args, **kw)

def upgrade(*args, **kw):
    return pisi.operations.upgrade.upgrade(*args, **kw)

def emerge(*args, **kw):
    return pisi.operations.emerge.emerge(*args, **kw)

def plan_install(*args, **kw):
    return pisi.operations.install.plan_install_pkg_names(*args, **kw)

def plan_remove(*args, **kw):
    return pisi.operations.remove.plan_remove(*args, **kw)

def plan_upgrade(*args, **kw):
    return pisi.operations.upgrade.plan_upgrade(*args, **kw)

def upgrade_base(*args, **kw):
    return pisi.operations.upgrade.upgrade_base(*args, **kw)

def calculate_conflicts(*args, **kw):
    return pisi.conflict.calculate_conflicts(*args, **kw)

def reorder_base_packages(*args, **kw):
    return pisi.operations.helper.reorder_base_packages(*args, **kw)

def build_until(*args, **kw):
    return pisi.operations.build.build_until(*args, **kw)

def build(*args, **kw):
    return pisi.atomicoperations.build(*args, **kw)

########################################################################

## Deletes the cached pisi packages to keep the package cache dir within cache limits
#  @param all When set all the cached packages will be deleted
def clearCache(all=False):

    import glob
    from sets import Set as set

    def getPackageLists(pkgList):
        latest = {}
        for f in pkgList:
            try:
                name, version = util.parse_package_name(f)
                if latest.has_key(name):
                    if Version(latest[name]) < Version(version):
                        latest[name] = version
                else:
                    if version:
                        latest[name] = version
            except:
                pass

        latestVersions = []
        for pkg in latest:
            latestVersions.append("%s-%s" % (pkg, latest[pkg]))

        oldVersions = list(set(pkgList) - set(latestVersions))
        return oldVersions, latestVersions

    def getRemoveOrder(cacheDir, pkgList):
        sizes = {}
        for pkg in pkgList:
            sizes[pkg] = os.stat(os.path.join(cacheDir, pkg) + ".pisi").st_size

        # sort dictionary by value from PEP-265
        from operator import itemgetter
        return sorted(sizes.iteritems(), key=itemgetter(1), reverse=False)

    def removeOrderByLimit(cacheDir, order, limit):
        totalSize = 0
        for pkg, size in order:
            totalSize += size
            if totalSize >= limit:
                try:
                    os.remove(os.path.join(cacheDir, pkg) + ".pisi")
                except exceptions.OSError:
                    pass

    def removeAll(cacheDir):
        cached = glob.glob("%s/*.pisi" % cacheDir) + glob.glob("%s/*.part" % cacheDir)
        for pkg in cached:
            try:
                os.remove(pkg)
            except exceptions.OSError:
                pass

    cacheDir = ctx.config.packages_dir()

    pkgList = map(lambda x: os.path.basename(x).split(".pisi")[0], glob.glob("%s/*.pisi" % cacheDir))
    if not all:
        # Cache limits from pisi.conf
        limit = int(ctx.config.values.general.package_cache_limit) * 1024 * 1024 # is this safe?
        if not limit:
            return

        old, latest = getPackageLists(pkgList)
        order = getRemoveOrder(cacheDir, latest) + getRemoveOrder(cacheDir, old)
        removeOrderByLimit(cacheDir, order, limit)
    else:
        removeAll(cacheDir)
