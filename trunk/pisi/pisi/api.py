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
import pisi.db
import pisi.context as ctx
from pisi.uri import URI
import pisi.util as util
import pisi.dependency as dependency
import pisi.pgraph as pgraph
import pisi.operations as operations
import pisi.db.packagedb as packagedb
import pisi.db.repodb
import pisi.db.installdb
import pisi.db.filesdb
import pisi.db.componentdb
import pisi.db.sourcedb
import pisi.db.lockeddbshelve as lockeddbshelve
import pisi.component as component
from pisi.index import Index
import pisi.cli
from pisi.config import Options
from pisi.operations import install, remove, upgrade, emerge
from pisi.operations import plan_install_pkg_names as plan_install
from pisi.operations import plan_remove, plan_upgrade, upgrade_base, calculate_conflicts, reorder_base_packages
from pisi.build import build_until
from pisi.atomicoperations import resurrect_package, build
from pisi.metadata import MetaData
from pisi.files import Files
from pisi.file import File
import pisi.db.lockeddbshelve as shelve
from pisi.version import Version

class Error(pisi.Error):
    pass

def init(database = True, write = True,
         options = Options(), ui = None, comar = True,
         stdout = None, stderr = None,
         comar_sockname = None,
         signal_handling = True):
    """Initialize PiSi subsystem.
    
    You should call finalize() when your work is finished. Otherwise
    you can left the database in a bad state.
    
    """

    # UI comes first

    if ui is None:
        from pisi.cli import CLI
        if options:
            ctx.ui = CLI(options.debug, options.verbose)
        else:
            ctx.ui = CLI()
    else:
        ctx.ui = ui

    if os.access('/var/log', os.W_OK):
        handler = logging.handlers.RotatingFileHandler('/var/log/pisi.log')
        #handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)-12s: %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        ctx.log = logging.getLogger('pisi')
        ctx.log.addHandler(handler)
        ctx.loghandler = handler
        ctx.log.setLevel(logging.DEBUG)
    else:
        ctx.log = None

    # If given define stdout and stderr. Needed by buildfarm currently
    # but others can benefit from this too.
    if stdout:
        ctx.stdout = stdout
    if stderr:
        ctx.stderr = stderr

    import pisi.config
    ctx.config = pisi.config.Config(options)

    if signal_handling:
        ctx.sig = pisi.signalhandler.SignalHandler()

    # TODO: this is definitely not dynamic beyond this point!
    ctx.comar = comar and not ctx.config.get_option('ignore_comar')
    # This is for YALI, used in comariface.py
    ctx.comar_sockname = comar_sockname

    # initialize repository databases
    ctx.database = database
    if database:
        shelve.init_dbenv(write=write)
        ctx.repodb = pisi.db.repodb.init()
        ctx.installdb = pisi.db.installdb.init()
        ctx.filesdb = pisi.db.filesdb.FilesDB()
        ctx.componentdb = pisi.db.componentdb.ComponentDB()
        ctx.packagedb = packagedb.init_db()
        ctx.sourcedb = pisi.db.sourcedb.init()
    else:
        ctx.repodb = None
        ctx.installdb = None
        ctx.filesdb = None
        ctx.componentdb = None
        ctx.packagedb = None
        ctx.sourcedb = None
    ctx.ui.debug('PiSi API initialized')
    ctx.initialized = True

def finalize():
    """Close the database cleanly and do other cleanup."""
    if ctx.initialized:
        ctx.disable_keyboard_interrupts()
        if ctx.log:
            ctx.loghandler.flush()
            ctx.log.removeHandler(ctx.loghandler)

        if ctx.repodb:
            ctx.repodb.finalize()
            ctx.repodb = None
        if ctx.installdb:
            ctx.installdb.finalize()
            ctx.installdb = None    
        if ctx.filesdb != None:
            ctx.filesdb.close()
            ctx.filesdb = None
        if ctx.componentdb != None:
            ctx.componentdb.close()
            ctx.componentdb = None
        if ctx.packagedb:
            packagedb.finalize_db()
            ctx.packagedb = None
        if ctx.sourcedb:
            pisi.db.sourcedb.finalize()
            ctx.sourcedb = None
        if ctx.dbenv:
            ctx.dbenv.close()
            ctx.dbenv_lock.close()
        if ctx.build_leftover and os.path.exists(ctx.build_leftover):
            os.unlink(ctx.build_leftover)

        ctx.ui.debug('PiSi API finalized')
        ctx.ui.close()
        ctx.initialized = False
        ctx.enable_keyboard_interrupts()

def list_installed():
    """Return a set of installed package names."""
    return set(ctx.installdb.list_installed())

def list_available(repo = None):
    """Return a set of available package names."""
    return set(ctx.packagedb.list_packages(repo = repo))

def list_upgradable():
    ignore_build = ctx.get_option('ignore_build_no')

    return filter(pisi.operations.is_upgradable, ctx.installdb.list_installed())

def package_graph(A, repo = pisi.db.itembyrepodb.installed, ignore_installed = False):
    """Construct a package relations graph.
    
    Graph will contain all dependencies of packages A, if ignore_installed
    option is True, then only uninstalled deps will be added.
    
    """

    ctx.ui.debug('A = %s' % str(A))

    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(ctx.packagedb, repo)             # construct G_f

    # find the "install closure" graph of G_f by package 
    # set A using packagedb
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = ctx.packagedb.get_package(x, repo)
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
    # @C: conflicting and must be removed packages list to proceed
    # @D: list of the conflicting packages _with each other_ in the to be installed list
    # @E: dictionary that contains which package in the to be installed list conflicts
    #     with which packages

    (C, D, E) = calculate_conflicts(A, ctx.packagedb)
    return (C, D, E)

def generate_pending_order(A):
    # returns pending package list in reverse topological order of dependency
    G_f = pgraph.PGraph(ctx.packagedb, pisi.db.itembyrepodb.installed) # construct G_f
    for x in A.keys():
        G_f.add_package(x)
    B = A
    while len(B) > 0:
        Bp = set()
        for x in B.keys():
            pkg = ctx.packagedb.get_package(x, pisi.db.itembyrepodb.installed)
            for dep in pkg.runtimeDependencies():
                if dep.package in G_f.vertices():
                    G_f.add_dep(x, dep)
        B = Bp
    if ctx.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    order.reverse()

    # Bug 4211
    if ctx.componentdb.has_component('system.base'):
        order = reorder_base_packages(order)

    return order

def configure_pending():
    # start with pending packages
    # configure them in reverse topological order of dependency
    A = ctx.installdb.list_pending()
    order = generate_pending_order(A)
    try:
        import pisi.comariface as comariface
        for x in order:
            if ctx.installdb.is_installed(x):
                pkginfo = A[x]
                pkgname = util.package_name(x, pkginfo.version,
                                        pkginfo.release,
                                        False,
                                        False)
                pkg_path = util.join_path(ctx.config.lib_dir(),
                                          'package', pkgname)
                m = MetaData()
                metadata_path = util.join_path(pkg_path, ctx.const.metadata_xml)
                m.read(metadata_path)
                # FIXME: we need a full package info here!
                pkginfo.name = x
                ctx.ui.notify(pisi.ui.configuring, package = pkginfo, files = None)
                pisi.comariface.post_install(
                    pkginfo.name,
                    m.package.providesComar,
                    util.join_path(pkg_path, ctx.const.comar_dir),
                    util.join_path(pkg_path, ctx.const.metadata_xml),
                    util.join_path(pkg_path, ctx.const.files_xml),
                )
                ctx.ui.notify(pisi.ui.configured, package = pkginfo, files = None)
            ctx.installdb.clear_pending(x)
    except ImportError:
        raise Error(_("comar package is not fully installed"))

def info(package, installed = False):
    if package.endswith(ctx.const.package_suffix):
        return info_file(package)
    else:
        return info_name(package, installed)

def info_file(package_fn):
    from package import Package

    if not os.path.exists(package_fn):
        raise Error (_('File %s not found') % package_fn)

    package = Package(package_fn)
    package.read()
    return package.metadata, package.files

def info_name(package_name, installed=False):
    """Fetch package information for the given package."""
    if installed:
        package = ctx.packagedb.get_package(package_name, pisi.db.itembyrepodb.installed)
    else:
        package, repo = ctx.packagedb.get_package_repo(package_name, pisi.db.itembyrepodb.repos)
        repostr = repo

    from pisi.metadata import MetaData
    metadata = MetaData()
    metadata.package = package
    #FIXME: get it from sourcedb if available
    metadata.source = None
    #TODO: fetch the files from server if possible (wow, you maniac -- future exa)
    if installed and ctx.installdb.is_installed(package.name):
        try:
            files = ctx.installdb.files(package.name)
        except pisi.Error, e:
            ctx.ui.warning(e)
            files = None
    else:
        files = None
    return metadata, files

def search_package_terms(terms, repo = pisi.db.itembyrepodb.all):
    return search_in_packages(terms, ctx.packagedb.list_packages(repo), repo)

def search_in_packages(terms, packages, repo = pisi.db.itembyrepodb.all):

    def search(package, term):
        term = unicode(term).lower()
        if term in unicode(package.name).lower() or \
                term in unicode(package.summary).lower() or \
                term in unicode(package.description).lower():
            return True

    found = []
    for name in packages:
        pkg = ctx.packagedb.get_package(name, repo)
        if terms == filter(lambda x:search(pkg, x), terms):
            found.append(name)

    return found

def check(package):
    md, files = info(package, True)
    corrupt = []
    for file in files.list:
        if file.hash and file.type != "config" \
           and not os.path.islink('/' + file.path):
            ctx.ui.info(_("Checking /%s ") % file.path, noln=True, verbose=True)
            try:
                if file.hash != util.sha1_file('/' + file.path):
                    corrupt.append(file)
                    ctx.ui.error(_("\nCorrupt file: %s") % file)
                else:
                    ctx.ui.info(_("OK"), verbose=True)
            except pisi.util.FileError,e:
                ctx.ui.error("\n%s" % e)
    return corrupt

def index(dirs=None, output='pisi-index.xml', skip_sources=False, skip_signing=False):
    """Accumulate PiSi XML files in a directory, and write an index."""
    index = Index()
    index.distribution = None
    if not dirs:
        dirs = ['.']
    for repo_dir in dirs:
        repo_dir = str(repo_dir)
        ctx.ui.info(_('* Building index of PiSi files under %s') % repo_dir)
        index.index(repo_dir, skip_sources)

    if skip_signing:
        index.write(output, sha1sum=True, compress=File.bz2, sign=None)
    else:
        index.write(output, sha1sum=True, compress=File.bz2, sign=File.detached)
    ctx.ui.info(_('* Index file written'))

def add_repo(name, indexuri, at = None):
    if ctx.repodb.has_repo(name):
        raise Error(_('Repo %s already present.') % name)
    else:
        repo = pisi.db.repodb.Repo(URI(indexuri))
        ctx.repodb.add_repo(name, repo, at = at)
        ctx.ui.info(_('Repo %s added to system.') % name)

def remove_repo(name):
    if ctx.repodb.has_repo(name):
        ctx.repodb.remove_repo(name)
        pisi.util.clean_dir(os.path.join(ctx.config.index_dir(), name))
        ctx.ui.info(_('Repo %s removed from system.') % name)
    else:
        ctx.ui.error(_('Repository %s does not exist. Cannot remove.')
                 % name)

def list_repos():
    return ctx.repodb.list()

def update_repo(repo, force=False):
    ctx.ui.info(_('* Updating repository: %s') % repo)
    ctx.ui.notify(pisi.ui.updatingrepo, name = repo)
    index = Index()
    if ctx.repodb.has_repo(repo):
        repouri = ctx.repodb.get_repo(repo).indexuri.get_uri()
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

        ctx.txn_proc(lambda txn : index.update_db(repo, txn=txn))
        ctx.ui.info(_('* Package database updated.'))
    else:
        raise Error(_('No repository named %s found.') % repo)

def delete_cache():
    util.clean_dir(ctx.config.packages_dir())
    util.clean_dir(ctx.config.archives_dir())
    util.clean_dir(ctx.config.tmp_dir())

def rebuild_repo(repo):
    ctx.ui.info(_('* Rebuilding \'%s\' named repo... ') % repo)

    if ctx.repodb.has_repo(repo):
        repouri = URI(ctx.repodb.get_repo(repo).indexuri.get_uri())
        indexname = repouri.filename()
        index = Index()
        indexpath = pisi.util.join_path(ctx.config.index_dir(), repo, indexname)
        tmpdir = os.path.join(ctx.config.tmp_dir(), 'index')
        pisi.util.clean_dir(tmpdir)
        pisi.util.check_dir(tmpdir)
        try:
            index.read_uri(indexpath, tmpdir, force=True) # don't look for sha1sum there
        except IOError, e:
            ctx.ui.warning(_("Input/Output error while reading %s: %s") % (indexpath, unicode(e)))
            return
        ctx.txn_proc(lambda txn : index.update_db(repo, txn=txn))
    else:
        raise Error(_('No repository named %s found.') % repo)

def rebuild_db(files=False):

    assert ctx.database == False

    # Bug 2596
    # finds and cleans duplicate package directories under '/var/lib/pisi/package'
    # deletes the _older_ versioned package directories.
    def clean_duplicates():
        i_version = {} # installed versions
        replica = []
        for pkg in os.listdir(pisi.util.join_path(pisi.api.ctx.config.lib_dir(), 'package')):
            (name, ver) = util.parse_package_name(pkg)
            if i_version.has_key(name):
                if Version(ver) > Version(i_version[name]):
                    # found a greater version, older one is a replica
                    replica.append(name + '-' + i_version[name])
                    i_version[name] = ver
                else:
                    # found an older version which is a replica
                    replica.append(name + '-' + ver)
            else:
                i_version[name] = ver

        for pkg in replica:
            pisi.util.clean_dir(pisi.util.join_path(pisi.api.ctx.config.lib_dir(), 'package', pkg))

    def destroy(files):
        #TODO: either don't delete version files here, or remove force flag...
        import bsddb3.db
        for db in os.listdir(ctx.config.db_dir()):
            if db.endswith('.bdb'):# or db.startswith('log'):  # delete only db files
                if db.startswith('files') or db.startswith('filesdbversion'):
                    clean = files
                else:
                    clean = True
                if clean:
                    fn = pisi.util.join_path(ctx.config.db_dir(), db)
                    #NB: there is a parameter bug with python-bsddb3, fixed in pardus
                    ctx.dbenv.dbremove(file=fn, flags=bsddb3.db.DB_AUTO_COMMIT)

    def reload_packages(files, txn):
        packages = os.listdir(pisi.util.join_path(ctx.config.lib_dir(), 'package'))
        progress = ctx.ui.Progress(len(packages))
        processed = 0
        for package_fn in packages:
            if not package_fn == "scripts":
                ctx.ui.debug('Resurrecting %s' % package_fn)
                pisi.api.resurrect_package(package_fn, files, txn)
                processed += 1
                ctx.ui.display_progress(operation = "rebuilding-db",
                                        percent = progress.update(processed),
                                        info = _("Rebuilding package database"))

    def reload_indices(txn):
        index_dir = ctx.config.index_dir()
        if os.path.exists(index_dir):  # it may have been erased, or we may be upgrading from a previous version -- exa
            for repo in os.listdir(index_dir):
                indexuri = pisi.util.join_path(ctx.config.lib_dir(), 'index', repo, 'uri')
                indexuri = open(indexuri, 'r').readline()
                pisi.api.add_repo(repo, indexuri)
                pisi.api.rebuild_repo(repo)

    # check db schema versions
    try:
        pisi.lockeddbshelve.check_dbversion('filesdbversion', pisi.__filesdbversion__, write=False)
    except KeyboardInterrupt:
        raise
    except Exception, e: #FIXME: what exception could we catch here, replace with that.
        files = True # exception means the files db version was wrong
    lockeddbshelve.init_dbenv(write=True, writeversion=True)
    destroy(files) # bye bye

    # save parameters and shutdown pisi
    options = ctx.config.options
    ui = ctx.ui
    comar = ctx.comar
    finalize()

    # construct new database
    init(database=True, options=options, ui=ui, comar=comar)
    clean_duplicates()
    txn = ctx.dbenv.txn_begin()
    reload_packages(files, txn)
    reload_indices(txn)
    txn.commit()
