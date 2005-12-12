# -*- coding:utf-8 -*-
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

import sys
from optparse import OptionParser
    
import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

import pisi
import pisi.cli
import pisi.context as ctx
from pisi.uri import URI
import pisi.util as util
import pisi.api as api
import pisi.packagedb as packagedb

class Error(pisi.Error):
    pass


class Command(object):
    """generic help string for any command"""

    # class variables

    cmd = []
    cmd_dict = {}

    def commands_string():
        s = ''
        list = [x.name[0] for x in Command.cmd]
        list.sort()
        for x in list:
            s += x + '\n'
        return s
    commands_string = staticmethod(commands_string)
    
    def get_command(cmd, fail=False):
    
        if Command.cmd_dict.has_key(cmd):
            return Command.cmd_dict[cmd]()
    
        if fail:
            raise Error(_("Unrecognized command: %s") % cmd)
        else:
            return None
    get_command = staticmethod(get_command)

    # instance variabes

    def __init__(self):
        # now for the real parser
        import pisi
        self.comar = False
        self.parser = OptionParser(usage=getattr(self, "__doc__"),
                                   version="%prog " + pisi.__version__)
        self.options()
        self.commonopts()
        (self.options, self.args) = self.parser.parse_args()
        self.args.pop(0)                # exclude command arg
        
        self.process_opts()

    def commonopts(self):
        '''common options'''
        p = self.parser
        p.add_option("-D", "--destdir", action="store", default = None,
                     help = _("change the system root for pisi commands"))
        p.add_option("-y", "--yes-all", action="store_true",
                     default=False, help = _("assume yes in all yes/no queries"))
        p.add_option("-u", "--username", action="store")
        p.add_option("-p", "--password", action="store")
        p.add_option("-P", action="store_true", dest="getpass", default=False,
                     help=_("get password from the command line"))
        p.add_option("-v", "--verbose", action="store_true",
                     dest="verbose", default=False,
                     help=_("detailed output"))
        p.add_option("-d", "--debug", action="store_true",
                     default=False, help=_("show debugging information"))
        p.add_option("-N", "--no-color", action="store_true", default=False,
                     help = _("print like a man"))
        return p

    def options(self):
        """This is a fall back function. If the implementer module provides an
        options function it will be called"""
        pass

    def process_opts(self):
        self.check_auth_info()
        
        # make destdir absolute
        if self.options.destdir:
            dir = str(self.options.destdir)
            import os.path
            if not os.path.exists(dir):
                pisi.cli.printu(_('Destination directory %s does not exist. Creating directory.\n') % dir)
                os.makedirs(dir)
            self.options.destdir = os.path.realpath(dir)


    def check_auth_info(self):
        username = self.options.username
        password = self.options.password

        # TODO: We'll get the username, password pair from a configuration
        # file from users home directory. Currently we need user to
        # give it from the user interface.
        #         if not username and not password:
        #             if someauthconfig.username and someauthconfig.password:
        #                 self.authInfo = (someauthconfig.username,
        #                                  someauthconfig.password)
        #                 return
        if username and password:
            self.authInfo = (username, password)
            return
        
        if username and self.options.getpass:
            from getpass import getpass
            password = getpass(_("Password: "))
            self.authInfo = (username, password)
        else:
            self.authInfo = None

    def init(self, database = True):
        """initialize PiSi components"""
        
        # NB: command imports here or in the command class run fxns
        import pisi.api
        pisi.api.init(database = database, options = self.options,
                      comar = self.comar)

    def finalize(self):
        """do cleanup work for PiSi components"""
        pisi.api.finalize()
        
    def get_name(self):
        return self.__class__.name

    def format_name(self):
        (name, shortname) = self.get_name()
        if shortname:
            return "%s (%s)" % (name, shortname)
        else:
            return name

    def help(self):
        """print help for the command"""
        ctx.ui.info(self.format_name() + ': ')
        trans = gettext.translation('pisi', fallback=True)
        ctx.ui.info(trans.ugettext(self.__doc__) + '\n')
        ctx.ui.info(self.parser.format_option_help())

    def die(self):
        """exit program"""
        #FIXME: not called from anywhere?
        ctx.ui.error(_('Command terminated abnormally.'))
        sys.exit(-1)


class autocommand(type):
    def __init__(cls, name, bases, dict):
        super(autocommand, cls).__init__(name, bases, dict)
        Command.cmd.append(cls)
        name = getattr(cls, 'name', None)
        if name is None:
            raise pisi.cli.Error(_('Command lacks name'))
        longname, shortname = name
        def add_cmd(cmd):
            if Command.cmd_dict.has_key(cmd):
                raise pisi.cli.Error(_('Duplicate command %s') % cmd)
            else:
                Command.cmd_dict[cmd] = cls
        add_cmd(longname)
        if shortname:
            add_cmd(shortname)
            

class Help(Command):
    """Prints help for given commands.

Usage: help [ <command1> <command2> ... <commandn> ]

If run without parameters, it prints the general help."""

    __metaclass__ = autocommand

    def __init__(self):
        #TODO? Discard Help's own usage doc in favor of general usage doc
        #self.__doc__ = usage_text
        #self.__doc__ += commands_string()
        super(Help, self).__init__()

    name = ("help", "h")

    def run(self):
        if not self.args:
            self.parser.set_usage(usage_text)
            pisi.cli.printu(self.parser.format_help())
            return
            
        self.init(database = False)
        
        for arg in self.args:
            obj = Command.get_command(arg, True)
            obj.help()
            ctx.ui.info('')
        
        self.finalize()


class Clean(Command):
    """Clean stale locks."""

    __metaclass__ = autocommand

    def __init__(self):
        super(Clean, self).__init__()

    name = ("clean", None)

    def run(self):
        self.init()
        pisi.util.clean_locks()
        self.finalize()


class DeleteCache(Command):
    """Delete cache files"""

    __metaclass__ = autocommand

    def __init__(self):
        super(DeleteCache, self).__init__()

    name = ("delete-cache", None)

    def run(self):
        self.init(database=False)
        pisi.api.delete_cache()


class Graph(Command):
    """Graph package relations.
Usage: graph [<package1> <package2> ...]

Write a graph of package relations, tracking dependency and
conflicts relations starting from given packages.
"""

    __metaclass__ = autocommand

    def __init__(self):
        super(Graph, self).__init__()
    
    def options(self):
        self.parser.add_option("-a", "--all", action="store_true",
                               default=False,
                               help=_("graph all available packages"))
        self.parser.add_option("-o", "--output", action="store",
                               default='pgraph.dot',
                               help=_("dot output file"))

    name = ("graph", None)

    def all_packages(self):
        a = set()
        from pisi import packagedb
        for repo in ctx.repodb.list():
            pkg_db = packagedb.get_db(repo)
            a = a.union(pkg_db.list_packages())
        return a

    def run(self):
        self.init()
        if ctx.get_option('all'):
            ctx.ui.info(_('Plotting a graph of relations among all available packages'))
            a = self.all_packages()
        else:
            if self.args:
                a = self.args
            else:
                # if A is empty, then graph all packages
                ctx.ui.info(_('Plotting a graph of relations among all installed packages'))
                a = ctx.installdb.list_installed()
        g = pisi.api.package_graph(a)
        g.write_graphviz(file(ctx.get_option('output'), 'w'))
        self.finalize()

# option mixins

def buildno_opts(self):
    self.parser.add_option("", "--ignore-build-no", action="store_true",
                           default=False,
                           help=_("do not take build no into account."))

def ignoredep_opt(self):
    p = self.parser
    p.add_option("-E", "--ignore-dependency", action="store_true",
                 default=False,
                 help=_("do not take dependency information into account"))


class Build(Command):
    """Build a PISI package using a pspec.xml file

Usage: build <pspec.xml>

You can give a URI of the pspec.xml file. PISI will
fetch all necessary files and build the package for you.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Build, self).__init__()

    name = ("build", "bi")

    def options(self):
        buildno_opts(self)
        ignoredep_opt(self)
        self.parser.add_option("-O", "--output-dir", action="store", default=".",
                               help=_("output directory for produced packages"))
        self.parser.add_option("-A", "--ignore-action-errors",
                               action="store_true", default=False,
                               help=_("bypass errors from ActionsAPI"))
        self.parser.add_option("-B", "--ignore-comar", action="store_true",
                               default=False, help=_("bypass comar configuration agent"))

    def run(self):
        if not self.args:
            self.help()
            return

        self.init(database = True)
        ctx.ui.info(_('Output directory: %s') % ctx.config.options.output_dir)
        for arg in self.args:
            pisi.api.build(arg, self.authInfo)
        self.finalize()


class PackageOp(Command):
    """Abstract package operation command"""

    def __init__(self):
        super(PackageOp, self).__init__()
        self.comar = True

    def options(self):
        p = self.parser
        p.add_option("-B", "--ignore-comar", action="store_true",
                     default=False, help=_("bypass comar configuration agent"))
        p.add_option("-S", "--bypass-safety", action="store_true",
                     default=False, help=_("bypass safety switch"))
        p.add_option("-n", "--dry-run", action="store_true", default=False,
                     help = _("do not perform any action, just show what would be done"))
        ignoredep_opt(self)

    def init(self):
        super(PackageOp, self).init(True)
                
    def finalize(self):
        #self.finalize_db()
        pass


class Install(PackageOp):
    """Install PISI packages

Usage: install <package1> <package2> ... <packagen>

You may use filenames, URIs or package names for packages. If you have
specified a package name, it should exist in a specified repository.

You can also specify components instead of package names, which will be
expanded to package names.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Install, self).__init__()

    name = "install", "it"

    def options(self):
        super(Install, self).options()
        p = self.parser
        p.add_option("", "--bypass-ldconfig", action="store_true",
                     default=False, help=_("Bypass ldconfig phase"))
        p.add_option("", "--reinstall", action="store_true",
                     default=False, help=_("Reinstall already installed packages"))
        buildno_opts(self)

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        pisi.api.install(self.args, ctx.get_option('reinstall'))
        self.finalize()


class Upgrade(PackageOp):
    """Upgrade PISI packages

Usage: Upgrade [<package1> <package2> ... <packagen>]

<packagei>: package name

Upgrades the entire system if no package names are given

You may use only package names to specify packages because
the package upgrade operation is defined only with respect 
to repositories. If you have specified a package name, it
should exist in the package repositories. If you just want to
reinstall a package from a pisi file, use the install command.

You can also specify components instead of package names, which will be
expanded to package names.
"""

    __metaclass__ = autocommand

    def __init__(self):
        super(Upgrade, self).__init__()

    name = ("upgrade", "up")

    def options(self):
        super(Upgrade, self).options()
        buildno_opts(self)
        p = self.parser
        p.add_option("", "--bypass-ldconfig", action="store_true",
                              default=False, help=_("Bypass ldconfig phase"))
        self.parser.add_option("-e", "--eager", action="store_true",
                               default=False, help=_("eager upgrades"))

    def run(self):
        self.init()
 
        if not self.args:
            packages = ctx.installdb.list_installed()
        else:
            packages = self.args

        pisi.api.upgrade(packages)
        self.finalize()


class Remove(PackageOp):
    """Remove PISI packages

Usage: remove <package1> <package2> ... <packagen>

Remove package(s) from your system. Just give the package names to remove.

You can also specify components instead of package names, which will be
expanded to package names.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Remove, self).__init__()

    name = ("remove", "rm")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        pisi.api.remove(self.args)
        self.finalize()


class ConfigurePending(PackageOp):
    """configure pending packages
    """
    
    __metaclass__ = autocommand

    def __init__(self):
        super(ConfigurePending, self).__init__()

    name = ("configure-pending", "cp")

    def run(self):

        self.init()
        pisi.api.configure_pending()
        self.finalize()


class Info(Command):
    """Display package information

Usage: info <package1> <package2> ... <packagen>

"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Info, self).__init__()

    name = ("info", "i")

    def options(self):
        self.parser.add_option("-f", "--files", action="store_true",
                               default=False,
                               help=_("show a list of package files."))
        self.parser.add_option("-F", "--files-path", action="store_true",
                               default=False,
                               help=_("Show only paths."))

    def run(self):
        if not self.args:
            self.help()
            return

        self.init(True)
        for arg in self.args:
            if ctx.componentdb.has_component(arg):
                component = ctx.componentdb.get_component(arg)
                #if self.options.long:
                ctx.ui.info(unicode(component))
            else: # then assume it was a package
                self.printinfo_package(arg)
        self.finalize()

    def printinfo_package(self, arg):
        import os.path

        metadata, files = pisi.api.info(arg)
        ctx.ui.info(unicode(metadata.package))
        revdeps =  [x[0] for x in packagedb.get_rev_deps(arg)]
        print _('Reverse Dependencies:'), util.strlist(revdeps)
        if self.options.files or self.options.files_path:
            if files:
                print _('\nFiles:')
                for fileinfo in files.list:
                    if self.options.files:
                        print fileinfo
                    else:
                        print fileinfo.path
            else:
                ctx.ui.warning(_('File information not available'))


class Check(Command):
    """Verify installation

Usage: check <package1> <package2> ... <packagen>
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Check, self).__init__()

    name = ("check", "c")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init(True)
        for arg in self.args:
            pisi.api.check(arg)
        self.finalize()


class Index(Command):
    """Index PISI files in a given directory

Usage: index <directory>

This command searches for all PiSi files in a directory, collects PiSi
tags from them and accumulates the information in an output XML file,
named by default 'pisi-index.xml'. In particular, it indexes both
source and binary packages.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Index, self).__init__()

    name = ("index", "ix")

    def options(self):
        self.parser.add_option("-a", "--absolute-uris", action="store_true",
                               default=False,
                               help=_("store absolute links for indexed files."))
        self.parser.add_option("-o", "--output", action="store",
                               default='pisi-index.xml',
                               help=_("index output file"))

    def run(self):
        
        self.init()
        from pisi.api import index
        if len(self.args)>0:
            index(self.args, ctx.get_option('output'))
        elif len(self.args)==0:
            ctx.ui.info(_('Indexing current directory.'))
            index('.', ctx.get_option('output'))
        self.finalize()


class ListInstalled(Command):
    """Print the list of all installed packages  

Usage: list-installed

"""

    __metaclass__ = autocommand

    def __init__(self):
        super(ListInstalled, self).__init__()

    name = ("list-installed", "li")

    def options(self):
        self.parser.add_option("-l", "--long", action="store_true",
                               default=False, help=_("show in long format"))
        self.parser.add_option("-i", "--install-info", action="store_true",
                               default=False, help=_("show detailed install info"))

    def run(self):
        self.init(True)
        list = ctx.installdb.list_installed()
        list.sort()
        if self.options.install_info:
            ctx.ui.info(_('Package Name     |St|   Version|  Rel.| Build|  Distro|             Date'))
            print         '========================================================================'
        for pkg in list:
            package = pisi.packagedb.inst_packagedb.get_package(pkg)
            inst_info = ctx.installdb.get_info(pkg)
            if self.options.long:
                ctx.ui.info(unicode(package))
                ctx.ui.info(unicode(inst_info))
            elif self.options.install_info:
                ctx.ui.info('%-15s  |%s' % (package.name, inst_info.one_liner()))
            else:
                ctx.ui.info('%15s - %s' % (package.name, package.summary))
        self.finalize()

class RebuildDb(Command):
    """Rebuild Databases

Usage: rebuilddb [ <package1> <package2> ... <packagen> ]

Rebuilds the PiSi databases

If package specs are given, they should be the names of package dirs under /var/lib/pisi
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(RebuildDb, self).__init__()

    name = ("rebuild-db", "rdb")

    def run(self):
            
        if self.args:
            self.init(database=True)
            for package_fn in self.args:
                pisi.api.resurrect_package(package_fn)
        else:
            self.init(database=False)
            if ctx.ui.confirm(_('Rebuild PISI databases?')):
                self.finalize()
                import os
                #FIXME: how good is deleting *all* databases?
                for db in os.listdir(ctx.config.db_dir()):
                    os.unlink(pisi.util.join_path(ctx.config.db_dir(), db))
                self.init(database=True)
                self.rebuild_db()
                verfn = util.join_path(pisi.context.config.db_dir(), 'dbversion')
                verfile = file(verfn, 'w')
                verfile.write(pisi.__dbversion__)
                verfile.close()

        self.finalize()

    def rebuild_db(self):
        import os
        for package_fn in os.listdir(ctx.config.lib_dir()):
            if not package_fn == "scripts":
                ctx.ui.debug('Resurrecting %s' % package_fn)
                pisi.api.resurrect_package(package_fn)

class UpdateRepo(Command):
    """Update repository databases

Usage: update-repo [<repo1> <repo2> ... <repon>]

<repoi>: repository name
Synchronizes the PiSi databases with the current repository.
If no repository is given, all repositories are updated.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(UpdateRepo, self).__init__()

    name = ("update-repo", "ur")

    def run(self):
        self.init(database = True)

        if self.args:
            repos = self.args
        else:
            repos = ctx.repodb.list()

        for repo in repos:
            pisi.api.update_repo(repo)
        self.finalize()


class AddRepo(Command):
    """Add a repository

Usage: add-repo <repo> <indexuri>

<repo>: name of repository to add
<indexuri>: URI of index file

If no repo is given, add-repo pardus-devel repo is added by default

NB: We support only local files (e.g., /a/b/c) and http:// URIs at the moment
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(AddRepo, self).__init__()

    name = ("add-repo", "ar")

    def run(self):

        if len(self.args)==2 or len(self.args)==0:
            self.init()
            if len(self.args)==2:
                name = self.args[0]
                indexuri = self.args[1]
            else:
                name = 'pardus-devel'
                indexuri = 'http://paketler.uludag.org.tr/pardus-devel/pisi-index.xml'
            pisi.api.add_repo(name, indexuri)
            if ctx.ui.confirm(_('Update PISI database for repository %s?') % name):
                pisi.api.update_repo(name)
            self.finalize()
        else:
            self.help()
            return


class RemoveRepo(Command):
    """Remove repositories

Usage: remove-repo <repo1> <repo2> ... <repon>

Remove all repository information from the system.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(RemoveRepo, self).__init__()

    name = ("remove-repo", "rr")

    def run(self):

        if len(self.args)>=1:
            self.init()
            for repo in self.args:
                pisi.api.remove_repo(repo)
            self.finalize()
        else:
            self.help()
            return


class ListRepo(Command):
    """List repositories

Usage: list-repo

Lists currently tracked repositories.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(ListRepo, self).__init__()

    name = ("list-repo", "lr")

    def run(self):

        self.init()
        for repo in ctx.repodb.list():
            ctx.ui.info(repo)
            print '  ', ctx.repodb.get_repo(repo).indexuri.get_uri()
        self.finalize()


class ListAvailable(Command):
    """List available packages in the repositories

Usage: list-available [ <repo1> <repo2> ... repon ]

Gives a brief list of PiSi packages published in the repository.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(ListAvailable, self).__init__()

    name = ("list-available", "la")

    def options(self):
        self.parser.add_option("-l", "--long", action="store_true",
                               default=False, help=_("show in long format"))
        self.parser.add_option("-U", "--uninstalled", action="store_true",
                               default=False, help=_("show uninstalled packages only"))

    def run(self):

        self.init(True)

        if self.args:
            for arg in self.args:
                self.print_packages(arg)
        else:
            # print for all repos
            for repo in ctx.repodb.list():
                ctx.ui.info(_("Repository : %s\n") % repo)
                self.print_packages(repo)
        self.finalize()

    def print_packages(self, repo):
        from pisi import packagedb
        from colors import colorize

        pkg_db = packagedb.get_db(repo)
        list = pkg_db.list_packages()
        installed_list = ctx.installdb.list_installed()
        list.sort()
        for p in list:
            package = pkg_db.get_package(p)
            if self.options.long:
                ctx.ui.info(unicode(package))
            else:
                lenp = len(p)
                if p in installed_list:
                    if ctx.config.get_option('uninstalled'):
                        continue
                    p = colorize(p, 'cyan')
                p = p + ' ' * max(0, 15 - lenp)
                ctx.ui.info('%s - %s ' % (p, unicode(package.summary)))

class ListComponents(Command):
    """List available components

Usage: list-components

Gives a brief list of PiSi components published in the repositories.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(ListComponents, self).__init__()

    name = ("list-components", "lc")

    def options(self):
        self.parser.add_option("-l", "--long", action="store_true",
                               default=False, help=_("show in long format"))

    def run(self):

        self.init(True)

        list = ctx.componentdb.list_components()
        list.sort()
        for p in list:
            component = ctx.componentdb.get_component(p)
            if self.options.long:
                ctx.ui.info(unicode(component))
            else:
                lenp = len(p)
                #if p in installed_list:
                #    p = colorize(p, 'cyan')
                p = p + ' ' * max(0, 15 - lenp)
                ctx.ui.info('%s - %s ' % (component.name, unicode(component.summary)))
        self.finalize()


class ListUpgrades(Command):
    """List packages to be upgraded

Usage: list-upgrades [ <repo1> <repo2> ... repon ]

"""
    __metaclass__ = autocommand

    def __init__(self):
        super(ListUpgrades, self).__init__()

    name = ("list-upgrades", "lu")

    def options(self):
        self.parser.add_option("-l", "--long", action="store_true",
                               default=False, help=_("show in long format"))
        self.parser.add_option("-i", "--install-info", action="store_true",
                               default=False, help=_("show detailed install info"))
        buildno_opts(self)
                               
    def run(self):
        self.init(True)
        list = pisi.api.list_upgradable()
        list.sort()
        if self.options.install_info:
            ctx.ui.info(_('Package Name     |St|   Version|  Rel.| Build|  Distro|             Date'))
            print         '========================================================================'
        for pkg in list:
            package = pisi.packagedb.inst_packagedb.get_package(pkg)
            inst_info = ctx.installdb.get_info(pkg)
            if self.options.long:
                ctx.ui.info(package)
                print inst_info
            elif self.options.install_info:
                ctx.ui.info('%-15s | %s ' % (package.name, inst_info.one_liner()))
            else:
                ctx.ui.info('%15s - %s ' % (package.name, package.summary))
        self.finalize()


class ListPending(Command):
    """List pending packages"""

    __metaclass__ = autocommand

    def __init__(self):
        super(ListPending, self).__init__()
    
    name = ("list-pending", "lp")

    def run(self):
        self.init(True)

        list = ctx.installdb.list_pending()
        for p in list.keys():
            print p
        self.finalize()


class Search(Info):
    """Search packages

Usage: search <term1> <term2> ... <termn>

Finds a package in repository containing specified search terms
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(Search, self).__init__()
        
    name = ("search", "s")

    def options(self):
        super(Search, self).options()
        self.parser.add_option("-l", "--language", action="store",
                               help=_("set search language"))

    def get_lang(self):
        lang = ctx.get_option('language')
        if not lang:
            lang = pisi.pxml.autoxml.LocalText.get_lang()
        if not lang in ['en', 'tr']:
            lang = 'en'
        return lang


    def run(self):

        self.init(True)

        if not self.args:
            self.help()
            return

        r = pisi.api.search_package_terms(self.args, self.get_lang())

        for pkg in r:
            self.printinfo_package(pkg)

        self.finalize()

class SearchFile(Command):
    """Search for a file

Usage: search-file <path1> <path2> ... <pathn>

Finds the installed package which contains the specified file.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(SearchFile, self).__init__()
    
    name = ("search-file", "sf")

    def options(self):
        self.parser.add_option("-l", "--long", action="store_true",
                               default=False, help=_("show in long format"))
        self.parser.add_option("-f", "--fuzzy", action="store_true",
                               default=False, help=_("fuzzy search"))
    
    # what does exact mean? -- exa
    @staticmethod
    def search_exact(path):
        files = []
        path = path.lstrip('/') #FIXME: this shouldn't be necessary :/

        if not ctx.config.options.fuzzy:
            if ctx.filesdb.has_file(path):
                files.append(ctx.filesdb.get_file(path))
        else:
            #FIXME: this linear search thing is not working well -- exa
            files = ctx.filesdb.match_files(path)

        if files:
            for (pkg_name, file_info) in files:
                ctx.ui.info(_("Package %s has file %s") % (pkg_name, file_info.path))
                if ctx.config.options.long:
                    ctx.ui.info(_('Type: %s, Hash: %s') % (file_info.type,
                                                           file_info.hash))
        else:
            ctx.ui.error(_("Path '%s' does not belong to an installed package") % path)

    def run(self):

        self.init(True)

        if not self.args:
            self.help()
            return        
       
        # search among existing files
        for path in self.args:
            ctx.ui.info(_('Searching for %s') % path)
            import os.path
            if os.path.exists(path):
                path = os.path.realpath(path)
            self.search_exact(path)

        self.finalize()


# Partial build commands        


class BuildUntil(Build):
    """Run the build process partially

Usage: -sStateName build-until <pspec file>

where states are:
unpack, setupaction, buildaction, installaction, buildpackages

You can give an URI of the pspec.xml file. PISI will fetch all
necessary files and unpack the source and prepare a source directory
for you.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(BuildUntil, self).__init__()

    name = ("build-until", "bu")

    def options(self):
        super(BuildUntil, self).options()        
        self.parser.add_option("-s", action="store", dest="state")

    def run(self):

        if not self.args:
            self.help()
            return

        self.init()
        state = self.options.state

        for arg in self.args:
            pisi.api.build_until(arg, state, self.authInfo)
        self.finalize()


class BuildUnpack(Build):
    """Unpack the source archive

Usage: build-unpack <pspec file>

TODO: desc.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(BuildUnpack, self).__init__()

    name = ("build-unpack", "biu")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        for arg in self.args:
            pisi.api.build_until(arg, "unpack", self.authInfo)
        self.finalize()


class BuildSetup(Build):
    """Setup the source

Usage: build-setup <pspec file>

TODO: desc.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(BuildSetup, self).__init__()

    name = ("build-setup", "bis")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        for arg in self.args:
            pisi.api.build_until(arg, "setupaction",
                                      self.authInfo)
        self.finalize()


class BuildBuild(Build):
    """Setup the source

Usage: build-build <pspec file>

TODO: desc.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(BuildBuild, self).__init__()

    name = ("build-build", "bib")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        for arg in self.args:
            pisi.api.build_until(arg, "buildaction", self.authInfo)
        self.finalize()


class BuildInstall(Build):
    """Install to the sandbox

Usage: build-install <pspec file>

TODO: desc.
"""
    __metaclass__ = autocommand

    def __init__(self):
        super(BuildInstall, self).__init__()

    name = ("build-install", "bii")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        for arg in self.args:
            pisi.api.build_until(arg, "installaction",
                                      self.authInfo)
        self.finalize()


class BuildPackage(Build):
    """Setup the source

Usage: build-build <pspec file>

TODO: desc.
"""

    __metaclass__ = autocommand

    def __init__(self):
        super(BuildPackage, self).__init__()

    name = ("build-package", "bip")

    def run(self):
        if not self.args:
            self.help()
            return

        self.init()
        for arg in self.args:
            pisi.api.build_until(arg, "buildpackages", self.authInfo)
        self.finalize()

usage_text1 = _("""%prog [options] <command> [arguments]

where <command> is one of:

""")

usage_text2 = _("""
Use \"%prog help <command>\" for help on a specific command.
""")

usage_text = (usage_text1 + Command.commands_string() + usage_text2)
