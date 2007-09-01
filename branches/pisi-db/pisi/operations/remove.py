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
import pisi.context as ctx
import pisi.atomicoperations as atomicoperations
import pisi.dependency as dependency
import pisi.pgraph as pgraph
import pisi.util as util
import pisi.ui as ui

def remove(A, ignore_dep = False, ignore_safety = False):
    """remove set A of packages from system (A is a list of package names)"""

    A = [str(x) for x in A]

    # filter packages that are not installed
    A_0 = A = set(A)

    if not ctx.get_option('ignore_safety') and not ignore_safety:
        if ctx.componentdb.has_component('system.base'):
            systembase = set(ctx.componentdb.get_union_comp('system.base').packages)
            refused = A.intersection(systembase)
            if refused:
                ctx.ui.warning(_('Safety switch: cannot remove the following packages in system.base: ') +
                               util.strlist(refused))
                A = A - systembase
        else:
            ctx.ui.warning(_('Safety switch: the component system.base cannot be found'))

    Ap = []
    for x in A:
        if ctx.installdb.has_package(x):
            Ap.append(x)
        else:
            ctx.ui.info(_('Package %s does not exist. Cannot remove.') % x)
    A = set(Ap)

    if len(A)==0:
        ctx.ui.info(_('No packages to remove.'))
        return False

    if not ctx.config.get_option('ignore_dependency') and not ignore_dep:
        G_f, order = plan_remove(A)
    else:
        G_f = None
        order = A

    ctx.ui.info(_("""The following minimal list of packages will be removed
in the respective order to satisfy dependencies:
""") + util.strlist(order))
    if len(order) > len(A_0):
        if not ctx.ui.confirm(_('Do you want to continue?')):
            ctx.ui.warning(_('Package removal declined'))
            return False

    if ctx.get_option('dry_run'):
        return

    ctx.ui.notify(ui.packagestogo, order = order)

    for x in order:
        if ctx.installdb.has_package(x):
            atomicoperations.remove_single(x)
        else:
            ctx.ui.info(_('Package %s is not installed. Cannot remove.') % x)

def plan_remove(A):
    # try to construct a pisi graph of packages to
    # install / reinstall

    G_f = pgraph.PGraph(ctx.packagedb, pisi.db.installed)               # construct G_f

    # find the (install closure) graph of G_f by package
    # set A using packagedb
    for x in A:
        G_f.add_package(x)
    B = A
    while len(B) > 0:
        Bp = set()
        for x in B:
            rev_deps = ctx.packagedb.get_rev_deps(x, pisi.db.installed)
            for (rev_dep, depinfo) in rev_deps:
                # we don't deal with uninstalled rev deps
                # and unsatisfied dependencies (this is important, too)
                if ctx.installdb.has_package(rev_dep) and \
                   dependency.installed_satisfies_dep(depinfo):
                    if not rev_dep in G_f.vertices():
                        Bp.add(rev_dep)
                        G_f.add_plain_dep(rev_dep, x)
        B = Bp
    if ctx.config.get_option('debug'):
        G_f.write_graphviz(sys.stdout)
    order = G_f.topological_sort()
    return G_f, order

# FIXME: this should be done in atomicoperations automatically.
def remove_replaced_packages(order, replaces):

    replaced = []
    inorder = set(order).intersection(replaces.values())

    if inorder:
        for pkg in replaces.keys():
            if replaces[pkg] in inorder:
                replaced.append(pkg)

    if replaced:
        if remove(replaced, ignore_dep=True, ignore_safety=True):
            raise Exception(_("Replaced package remains"))

def remove_conflicting_packages(conflicts):
    if remove(conflicts, ignore_dep=True, ignore_safety=True):
        raise Exception(_("Conflicts remain"))

def remove_obsoleted_packages():
    obsoletes = filter(ctx.installdb.has_package, ctx.packagedb.get_obsoletes())
    if obsoletes:
        if remove(obsoletes, ignore_dep=True, ignore_safety=True):
            raise Exception(_("Obsoleted packages remaining"))
