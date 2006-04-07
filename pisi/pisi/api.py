# -*- coding: utf-8 -*-
#
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
from os.path import exists
import bsddb3.db as db

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
import pisi.sourcedb
import pisi.component as component
from pisi.index import Index
import pisi.cli
from pisi.operations import install, remove, upgrade, emerge
from pisi.build import build_until
from pisi.atomicoperations import resurrect_package, build
from pisi.metadata import MetaData
from pisi.files import Files
from pisi.file import File
import pisi.search
import pisi.lockeddbshelve as shelve

class Error(pisi.Error):
    pass

def init(database = True, write = True, options = None, ui = None, comar = True):
    """Initialize PiSi subsystem"""

    # UI comes first
        
    if ui is None:
        from pisi.cli import CLI
        if options:
            ctx.ui = CLI(options.debug)
        else:
            ctx.ui = CLI()
    else:
        ctx.ui = ui

    import pisi.config
    ctx.config = pisi.config.Config(options)

    # TODO: this is definitely not dynamic beyond this point!
    ctx.comar = comar and not ctx.config.get_option('ignore_comar')

    # initialize repository databases
    ctx.database = database
    if database:
        shelve.init_dbenv(write=write)
        ctx.repodb = pisi.repodb.init()
        ctx.installdb = pisi.installdb.init()
        ctx.filesdb = pisi.files.FilesDB()
        ctx.componentdb = pisi.component.ComponentDB()
        ctx.packagedb = packagedb.init_db()
        ctx.sourcedb = pisi.sourcedb.init()
        pisi.search.init(['summary', 'description'], ['en', 'tr'])
    else:
        ctx.repodb = None
        ctx.installdb = None
        ctx.filesdb = None
        ctx.componentdb = None
        ctx.packagedb = None
        ctx.sourcedb = None
    ctx.ui.debug('PISI API initialized')
    ctx.initialized = True

def finalize():
    if ctx.initialized:
        pisi.repodb.finalize()
        pisi.installdb.finalize()
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
            pisi.sourcedb.finalize()
            ctx.sourcedb = None
        pisi.search.finalize()
        if ctx.dbenv:
            ctx.dbenv.close()
        ctx.ui.debug('PISI API finalized')
        ctx.ui.close()
        ctx.initialized = False

def list_available():
    '''returns a set of available package names'''

    available = set()
    for repo in pisi.context.repodb.list():
        available.update(ctx.packagedb.list_packages())
    return available

def list_upgradable():
    ignore_build = ctx.get_option('ignore_build_no')

    A = ctx.installdb.list_installed()
    # filter packages that are not upgradable
    Ap = []
    for x in A:
        (version, release, build) = ctx.installdb.get_version(x)
        pkg = ctx.packagedb.get_package(x)
        if ignore_build or (not build):
            if release < pkg.release:
                Ap.append(x)
        elif build < pkg.build:
                Ap.append(x)
        else:
            pass
            #ctx.ui.info('Package %s cannot be upgraded. ' % x)
    return Ap


def package_graph(A, ignore_installed = False):
    """Construct a package relations graph, containing
    all dependencies of packages A, if ignore_installed
    option is True, then only uninstalled deps will
    be added."""

    ctx.ui.debug('A = %s' % str(A))
  
    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(ctx.packagedb)               # construct G_f

    # find the "install closure" graph of G_f by package 
    # set A using packagedb
    for x in A:
        G_f.add_package(x)
    B = A
    #state = {}
    while len(B) > 0:
        Bp = set()
        for x in B:
            pkg = ctx.packagedb.get_package(x)
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

def configure_pending():
    # start with pending packages
    # configure them in reverse topological order of dependency
    A = ctx.installdb.list_pending()
    G_f = pgraph.PGraph(ctx.packagedb)               # construct G_f
    for x in A.keys():
        G_f.add_package(x)
    B = A
    while len(B) > 0:
        Bp = set()
        for x in B.keys():
            pkg = ctx.packagedb.get_package(x)
            for dep in pkg.runtimeDependencies():
                if dep.package in G_f.vertices():
                    G_f.add_dep(x, dep)
        B = Bp
    if ctx.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    order.reverse()
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
                for pcomar in m.package.providesComar:
                    scriptPath = util.join_path(pkg_path,
                                            ctx.const.comar_dir,
                                            pcomar.script)
                    comariface.register(pcomar, x, scriptPath)
                    # FIXME: we need a full package info here!
                    # Eray, please fix this
                    # your wish is a command, darling -- eray
                    pkginfo.name = x
                    ctx.ui.notify(pisi.ui.configuring, package = pkginfo, files = None)
                    comariface.run_postinstall(x)
                    ctx.ui.notify(pisi.ui.configured, package = pkginfo, files = None)
            ctx.installdb.clear_pending(x)
    except ImportError:
        raise Error(_("COMAR: comard not fully installed"))

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
    """fetch package information for a package"""
    if ctx.packagedb.has_package(package_name):
        package, repo = ctx.packagedb.get_package_repo(package_name)

        if (not installed) and (repo==pisi.itembyrepodb.installed):
            raise Error(_('Package %s not found') % package_name)
        
        from pisi.metadata import MetaData
        metadata = MetaData()
        metadata.package = package
        #FIXME: get it from sourcedb
        metadata.source = None
        #TODO: fetch the files from server if possible
        if installed and ctx.installdb.is_installed(package.name):
            files = ctx.installdb.files(package.name)
        else:
            files = None
        return metadata, files
    else:
        raise Error(_('Package %s not found') % package_name)

def search_package_terms(terms, lang = None):
    if not lang:
        lang = pisi.pxml.autoxml.LocalText.get_lang()
    r1 = pisi.search.query_terms('summary', lang, terms)
    r2 = pisi.search.query_terms('description', lang, terms)
    r = r1.union(r2)
    return r

def search_package(query, lang = None):
    if not lang:
        lang = pisi.pxml.autoxml.LocalText.get_lang()
    r1 = pisi.search.query('summary', lang, query)
    r2 = pisi.search.query('description', lang, query)
    r = r1.union(r2)
    return r

def check(package):
    md, files = info(package, True)
    corrupt = []
    for file in files.list:
        if file.hash and file.type != "config" \
           and not os.path.islink('/' + file.path):
            ctx.ui.info(_("Checking %s...") % file.path, False, True) 
            if file.hash != util.sha1_file('/' + file.path):
                corrupt.append(file)
                ctx.ui.info("Corrupt file: %s" % file)
            else:
                ctx.ui.info("OK", False)
    return corrupt

def index(dirs=None, output = 'pisi-index.xml', skip_sources=False):
    """accumulate PISI XML files in a directory"""
    index = Index()
    if not dirs:
        dirs = ['.']
    for repo_dir in dirs:
        repo_dir = str(repo_dir)
        ctx.ui.info(_('* Building index of PISI files under %s') % repo_dir)
        index.index(repo_dir, skip_sources)
    index.write(output, sha1sum=True, compress=File.xmill, sign=File.detached)
    ctx.ui.info(_('* Index file written'))

def add_repo(name, indexuri):
    if ctx.repodb.has_repo(name):
        raise Error(_('Repo %s already present.') % name)
    else:
        repo = pisi.repodb.Repo(URI(indexuri))
        ctx.repodb.add_repo(name, repo)
        ctx.ui.info(_('Repo %s added to system.') % name)

def remove_repo(name):
    if ctx.repodb.has_repo(name):
        ctx.repodb.remove_repo(name)
        pisi.util.clean_dir(os.path.join(ctx.config.index_dir(), repo))
        ctx.ui.info(_('Repo %s removed from system.') % name)
    else:
        ctx.ui.error(_('Repository %s does not exist. Cannot remove.') 
                 % name)

def update_repo(repo, force=False):
    ctx.ui.info(_('* Updating repository: %s') % repo)
    index = Index()
    if ctx.repodb.has_repo(repo):
        repouri = ctx.repodb.get_repo(repo).indexuri.get_uri()
        try:
            index.read_uri(repouri, repo)
        except pisi.file.AlreadyHaveException, e:
            ctx.ui.info(_('No updates available for repository %s.' % repo))
            if force:
                ctx.ui.info(_('Updating database at any rate as requested'))
                index.read_uri(repouri, repo, force = force)
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

def rebuild_db(files=False):

    assert ctx.database == False

    def destroy(files):
        #from pisi.lockeddbshelve import LockedDBShelf
        pisi.lockeddbshelve.init_dbenv(write=True)
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
                    #FIXME: there is a bug with bsddb3
                    #ctx.dbenv.dbremove(fn, "", None, bsddb3.db.DB_AUTO_COMMIT)
                    ctx.dbenv.dbremove(file=fn, flags=bsddb3.db.DB_AUTO_COMMIT)
                    #os.unlink(fn)
        ctx.dbenv.close()

    def reload(files, txn):
        for package_fn in os.listdir( pisi.util.join_path( ctx.config.lib_dir(),
                                                           'package' ) ):
            if not package_fn == "scripts":
                ctx.ui.debug('Resurrecting %s' % package_fn)
                pisi.api.resurrect_package(package_fn, files, txn)

    # check db schema versions
    try:
        pisi.lockeddbshelve.check_dbversion('filesdbversion', pisi.__filesdbversion__, write=False)
    except:
        files = True # exception means the files db version was wrong
    destroy(files) # bye bye
    pisi.lockeddbshelve.check_dbversion('dbversion', pisi.__dbversion__, write=True, update=True)
    pisi.lockeddbshelve.check_dbversion('filesdbversion', pisi.__filesdbversion__, write=True, update=True)

    # save parameters and shutdown pisi
    options = ctx.config.options
    ui = ctx.ui
    comar = ctx.comar
    finalize()
    # construct new database version
    init(database=True, options=options, ui=ui, comar=comar)
    #ctx.txn_proc(reload)
    reload(files, None)
