# -*- coding:utf-8 -*-
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

import optparse

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi.cli.command as command
import pisi.context as ctx

class Info(command.Command):
    """Display package information

Usage: info <package1> <package2> ... <packagen>

<packagei> is either a package name or a .pisi file,
"""
    __metaclass__ = command.autocommand

    def __init__(self, args):
        super(Info, self).__init__(args)

    name = ("info", None)

    def options(self):

        group = optparse.OptionGroup(self.parser, _("info options"))
        self.add_options(group)
        self.parser.add_option_group(group)

    def add_options(self, group):
        group.add_option("-f", "--files", action="store_true",
                               default=False,
                               help=_("Show a list of package files."))
        group.add_option("-c", "--component", action="append",
                               default=None, help=_("Info about the given component"))
        group.add_option("-F", "--files-path", action="store_true",
                               default=False,
                               help=_("Show only paths."))
        group.add_option("-s", "--short", action="store_true",
                               default=False, help=_("Do not show details"))
        group.add_option("--xml", action="store_true",
                               default=False, help=_("Output in xml format"))

    def run(self):

        self.init(database = True, write = False)

        components = ctx.get_option('component')
        if not components and not self.args:
            self.help()
            return

        index = pisi.index.Index()
        index.distribution = None

        # info of components
        if components:
            for name in components:
                if ctx.componentdb.has_component(name):
                    component = ctx.componentdb.get_union_comp(name)
                    if self.options.xml:
                        index.add_component(component)
                    else:
                        if not self.options.short:
                            ctx.ui.info(unicode(component))
                        else:
                            ctx.ui.info("%s - %s" % (component.name, component.summary))

        # info of packages
        for arg in self.args:
            if self.options.xml:
                index.packages.append(pisi.api.info(arg)[0].package)
            else:
                self.info_package(arg)

        if self.options.xml:
            errs = []
            index.newDocument()
            index.encode(index.rootNode(), errs)
            index.writexmlfile(sys.stdout)
            sys.stdout.write('\n')
        self.finalize()


    def info_package(self, arg):
        if arg.endswith(ctx.const.package_suffix):
            metadata, files = pisi.api.info_file(arg)
            ctx.ui.info(_('Package file: %s') % arg)
            self.print_pkginfo(metadata, files)
        else:
            if ctx.installdb.has_package(arg):
                metadata, files, repo = pisi.api.info_name(arg, None)
                if self.options.short:
                    ctx.ui.info(_('[inst] '), noln=True)
                else:
                    ctx.ui.info(_('Installed package:'))
                self.print_pkginfo(metadata, files,pisi.db.installed)
            else:
                ctx.ui.info(_("%s is not installed") % arg)

            for repo in ctx.repodb.list_repos():
                metadata, files, repo = pisi.api.info_name(arg, repo)
                if self.options.short:
                    ctx.ui.info(_('[repo] '), noln=True)
                else:
                    ctx.ui.info(_('Package found in %s repository:') % repo)
                self.print_pkginfo(metadata, files, pisi.db.repos)
            else:
                ctx.ui.info(_("%s is not found in repositories") % arg)


    def print_pkginfo(self, metadata, files, repo = None):
        if ctx.get_option('short'):
            pkg = metadata.package
            ctx.ui.info('%15s - %s' % (pkg.name, unicode(pkg.summary)))
        else:
            ctx.ui.info(unicode(metadata.package))
            if repo:
                # FIX:DB
#                 revdeps =  [x[0] for x in
#                             ctx.packagedb.get_rev_deps(metadata.package.name, repo)]
                revdeps = []
                print _('Reverse Dependencies:'), util.strlist(revdeps)
        if self.options.files or self.options.files_path:
            if files:
                print _('\nFiles:')
                files.list.sort(key = lambda x:x.path)
                for fileinfo in files.list:
                    if self.options.files:
                        print fileinfo
                    else:
                        print "/" + fileinfo.path
            else:
                ctx.ui.warning(_('File information not available'))
        if not self.options.short:
            print
