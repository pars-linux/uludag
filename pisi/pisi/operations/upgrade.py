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
#

import sys

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi
import pisi.ui as ui
import pisi.context as ctx
import pisi.pgraph as pgraph
import pisi.atomicoperations as atomicoperations
import pisi.operations as operations
import pisi.util as util
import pisi.dependency as dependency
import pisi.db
import pisi.blacklist

def find_upgrades(packages, replaces):
    packagedb = pisi.db.packagedb.PackageDB()
    installdb = pisi.db.installdb.InstallDB()

    security_only = ctx.get_option('security_only')
    ignore_build = ctx.get_option('ignore_build_no')

    Ap = []
    for i_pkg in packages:

        if i_pkg in replaces.keys():
            # Replaced packages will be forced for upgrade, cause replaced packages are marked as obsoleted also. So we
            # pass them.
            continue

        if i_pkg.endswith(ctx.const.package_suffix):
            ctx.ui.debug(_("Warning: package *name* ends with '.pisi'"))

        if not installdb.has_package(i_pkg):
            ctx.ui.info(_('Package %s is not installed.') % i_pkg, True)
            continue

        if not packagedb.has_package(i_pkg):
            ctx.ui.info(_('Package %s is not available in repositories.') % i_pkg, True)
            continue

        pkg = packagedb.get_package(i_pkg)
        (version, release, build, distro, distro_release) = installdb.get_version_and_distro_release(i_pkg)

        if security_only and not pkg.has_update_type("security", release):
            continue

        if pkg.distribution == distro and \
                pisi.version.make_version(pkg.distributionRelease) > pisi.version.make_version(distro_release):
            Ap.append(i_pkg)

        elif ignore_build or (not build) or (not pkg.build):
            if int(release) < int(pkg.release):
                Ap.append(i_pkg)
            else:
                ctx.ui.info(_('Package %s is already at the latest release %s.')
                            % (pkg.name, pkg.release), True)
        else:
            if build < pkg.build:
                Ap.append(i_pkg)
            else:
                ctx.ui.info(_('Package %s is already at the latest build %s.')
                            % (pkg.name, pkg.build), True)

    return Ap

def upgrade(A=[], repo=None):
    """Re-installs packages from the repository, trying to perform
    a minimum or maximum number of upgrades according to options."""

    packagedb = pisi.db.packagedb.PackageDB()
    installdb = pisi.db.installdb.InstallDB()
    replaces = packagedb.get_replaces()
    if not A:
        # if A is empty, then upgrade all packages
        A = installdb.list_installed()

    if repo:
        repo_packages = set(packagedb.list_packages(repo))
        A = set(A).intersection(repo_packages)

    A_0 = A = set(A)
    Ap = find_upgrades(A, replaces)
    A = set(Ap)

    # Force upgrading of installed but replaced packages or else they will be removed (they are obsoleted also).
    # This is not wanted for a replaced driver package (eg. nvidia-X).
    #
    # sum(array, []) is a nice trick to flatten an array of arrays
    A |= set(sum(replaces.values(), []))

    A |= upgrade_base(A)

    A = pisi.blacklist.exclude_from(A, ctx.const.blacklist)

    if ctx.get_option('exclude_from'):
        A = pisi.blacklist.exclude_from(A, ctx.get_option('exclude_from'))

    if ctx.get_option('exclude'):
        A = pisi.blacklist.exclude(A, ctx.get_option('exclude'))

    ctx.ui.debug('A = %s' % str(A))

    if len(A)==0:
        ctx.ui.info(_('No packages to upgrade.'))
        return True


    ctx.ui.debug('A = %s' % str(A))

    if not ctx.config.get_option('ignore_dependency'):
        G_f, order = plan_upgrade(A, replaces=replaces)
    else:
        G_f = None
        order = list(A)

    componentdb = pisi.db.componentdb.ComponentDB()

    # Bug 4211
    if componentdb.has_component('system.base'):
        order = operations.helper.reorder_base_packages(order)

    ctx.ui.status(_('The following packages will be upgraded:'))
    ctx.ui.info(util.format_by_columns(sorted(order)))

    total_size, cached_size = operations.helper.calculate_download_sizes(order)
    total_size, symbol = util.human_readable_size(total_size)
    ctx.ui.info(_('Total size of package(s): %.2f %s') % (total_size, symbol))

    if ctx.get_option('dry_run'):
        return

    if set(order) - A_0 - set(sum(replaces.values(), [])):
        if not ctx.ui.confirm(_('There are extra packages due to dependencies. Do you want to continue?')):
            return False

    ctx.ui.notify(ui.packagestogo, order = order)

    conflicts = []
    if not ctx.get_option('ignore_package_conflicts'):
        conflicts = operations.helper.check_conflicts(order, packagedb)

    paths = []
    for x in order:
        ctx.ui.info(util.colorize(_("Downloading %d / %d") % (order.index(x)+1, len(order)), "yellow"))
        install_op = atomicoperations.Install.from_name(x)
        paths.append(install_op.package_fname)

    # fetch to be upgraded packages but do not install them.
    if ctx.get_option('fetch_only'):
        return

    if conflicts:
        operations.remove.remove_conflicting_packages(conflicts)

    operations.remove.remove_obsoleted_packages()

    for path in paths:
        ctx.ui.info(util.colorize(_("Installing %d / %d") % (paths.index(path)+1, len(paths)), "yellow"))
        install_op = atomicoperations.Install(path, ignore_file_conflicts = True)
        install_op.install(True)

def plan_upgrade(A, force_replaced=True, replaces=None):
    # FIXME: remove force_replaced
    # try to construct a pisi graph of packages to
    # install / reinstall

    packagedb = pisi.db.packagedb.PackageDB()

    G_f = pgraph.PGraph(packagedb)               # construct G_f

    A = set(A)
    
    # Force upgrading of installed but replaced packages or else they will be removed (they are obsoleted also).
    # This is not wanted for a replaced driver package (eg. nvidia-X).
    #
    # FIXME: this is also not nice. this would not be needed if replaced packages are not written as obsoleted also.
    # But if they are not written obsoleted "pisi index" indexes them
    if force_replaced:
        if replaces is None:
            replaces = packagedb.get_replaces()
        A |= set(sum(replaces.values(), []))

    # find the "install closure" graph of G_f by package
    # set A using packagedb
    for x in A:
        G_f.add_package(x)
    B = A

    installdb = pisi.db.installdb.InstallDB()

    def add_runtime_deps(pkg, Bp):
        for dep in pkg.runtimeDependencies():
            # add packages that can be upgraded
            if installdb.has_package(dep.package) and dep.satisfied_by_installed():
                continue

            if dep.satisfied_by_repo():
                if not dep.package in G_f.vertices():
                    Bp.add(str(dep.package))
                    G_f.add_dep(pkg.name, dep)
            else:
                ctx.ui.error(_('Dependency %s of %s cannot be satisfied') % (dep, pkg.name))
                raise Exception(_("Upgrade is not possible."))

    def add_broken_revdeps(pkg, Bp):
        # Search reverse dependencies to see if anything
        # should be upgraded
        rev_deps = installdb.get_rev_deps(pkg.name)
        for rev_dep, depinfo in rev_deps:
            # add only installed but unsatisfied reverse dependencies
            if rev_dep in G_f.vertices() or \
                    depinfo.satisfied_by_installed() or \
                    not is_upgradable(rev_dep):
                continue

            if not depinfo.satisfied_by_repo():
                raise Exception(_('Reverse dependency %s of %s cannot be satisfied') % (rev_dep, pkg.name))

            Bp.add(rev_dep)
            G_f.add_plain_dep(rev_dep, pkg.name)

    def add_needed_revdeps(pkg, Bp):
        # Search for reverse dependency update needs of to be upgraded packages
        # check only the installed ones.
        version, release, build = installdb.get_version(pkg.name)
        actions = pkg.get_update_actions(release)

        for action_name, action_package in actions:
            if action_name == "reverseDependencyUpdate":
                target_package = action_package or pkg.name
                for name, dep in installdb.get_rev_deps(target_package):
                    if name in G_f.vertices() or not is_upgradable(name):
                        continue

                    Bp.add(name)
                    G_f.add_plain_dep(name, target_package)

    while B:
        Bp = set()

        for x in B:
            pkg = packagedb.get_package(x)

            add_runtime_deps(pkg, Bp)

            if installdb.has_package(x):
                add_broken_revdeps(pkg, Bp)
                add_needed_revdeps(pkg, Bp)

        B = Bp

    if ctx.config.get_option('debug'):
        G_f.write_graphviz(sys.stdout)

    order = G_f.topological_sort()
    order.reverse()
    return G_f, order

def upgrade_base(A = set()):
    installdb = pisi.db.installdb.InstallDB()
    componentdb = pisi.db.componentdb.ComponentDB()
    ignore_build = ctx.get_option('ignore_build_no')
    if not ctx.config.values.general.ignore_safety and not ctx.get_option('ignore_safety'):
        if componentdb.has_component('system.base'):
            systembase = set(componentdb.get_union_component('system.base').packages)
            extra_installs = filter(lambda x: not installdb.has_package(x), systembase - set(A))
            extra_installs = pisi.blacklist.exclude_from(extra_installs, ctx.const.blacklist)
            if extra_installs:
                ctx.ui.warning(_('Safety switch: Following packages in system.base will be installed: ') +
                               util.strlist(extra_installs))
            G_f, install_order = operations.install.plan_install_pkg_names(extra_installs)
            extra_upgrades = filter(lambda x: is_upgradable(x, ignore_build), systembase - set(install_order))
            upgrade_order = []

            extra_upgrades = pisi.blacklist.exclude_from(extra_upgrades, ctx.const.blacklist)

            if ctx.get_option('exclude_from'):
                extra_upgrades = pisi.blacklist.exclude_from(extra_upgrades, ctx.get_option('exclude_from'))

            if ctx.get_option('exclude'):
                extra_upgrades = pisi.blacklist.exclude(extra_upgrades, ctx.get_option('exclude'))

            if extra_upgrades:
                ctx.ui.warning(_('Safety switch: Following packages in system.base will be upgraded: ') +
                               util.strlist(extra_upgrades))
                G_f, upgrade_order = plan_upgrade(extra_upgrades, force_replaced=False)
            # return packages that must be added to any installation
            return set(install_order + upgrade_order)
        else:
            ctx.ui.warning(_('Safety switch: the component system.base cannot be found'))
    return set()

def is_upgradable(name, ignore_build = False):

    installdb = pisi.db.installdb.InstallDB()

    if not installdb.has_package(name):
        return False

    (i_version, i_release, i_build, i_distro, i_distro_release) = installdb.get_version_and_distro_release(name)

    packagedb = pisi.db.packagedb.PackageDB()

    try:
        version, release, build, distro, distro_release = packagedb.get_version_and_distro_release(name, packagedb.which_repo(name))
    except KeyboardInterrupt:
        raise
    except Exception: #FIXME: what exception could we catch here, replace with that.
        return False

    if distro == i_distro and \
            pisi.version.make_version(distro_release) > pisi.version.make_version(i_distro_release):
        return True
    elif ignore_build or (not i_build) or (not build):
        return int(i_release) < int(release)
    else:
        return i_build < build
