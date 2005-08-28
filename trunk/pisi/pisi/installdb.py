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
#
# installation database
#
# Author:  Eray Ozkural <eray@uludag.org.tr>

# System
import os
import fcntl

# PiSi
import pisi
import pisi.context as ctx
import pisi.lockeddbshelve as shelve
from pisi.files import Files
import pisi.util as util


class InstallDBError(pisi.Error):
    pass


class InstallInfo:
    # some data is replicated from packagedb.inst_packagedb
    # we store as an object, hey, we can waste O(1) space.
    # this is also easier to modify in the future, without
    # requiring database upgrades! wow!
    def __init__(self, state, version, release, build, distribution):
        self.state = state
        self.version = version
        self.release = release
        self.build = build
        self.distribution = distribution
        import time
        self.time = time.localtime()

    def one_liner(self):
        import time
        time_str = time.strftime("%d %b %Y %H:%M", self.time)
        s = '%2s|%10s|%6s|%6s|%8s|%12s' % (self.state, self.version, self.release,
                                   self.build, self.distribution,
                                   time_str)
        return s
    
    state_map = { 'i': 'installed', 'ip':'installed-pending', 'r:removed'
                  'p': 'purged' }
        
    def __str__(self):
        s = "State: %s\nVersion: %s, Release: %s, Build: %s\n" % \
            (InstallInfo.state_map[self.state], self.version,
             self.release, self.build)
        import time
        time_str = time.strftime("%d %b %Y %H:%M", self.time)
        s += 'Distribution: %s, Install Time: %s\n' % (self.distribution,
                                                       time_str)
        return s


class InstallDB:

    def __init__(self):
        from os.path import join
        self.d = shelve.LockedDBShelf('install')
        self.dp = shelve.LockedDBShelf('configpending')
        self.files_dir = os.path.join(ctx.config.db_dir(), 'files')

    def files_name(self, pkg, version, release):
        from os.path import join
        pkg_dir = join(config.lib_dir(), pkg + '-' + version + '-' + release)
        return join(pkg_dir, const.files_xml)

    def files(self, pkg):
        pkg = str(pkg)
        pkginfo = self.d[pkg]
        files = Files()
        files.read(self.files_name(pkg,pkginfo.version,pkginfo.release))
        return files

    def is_recorded(self, pkg):
        pkg = str(pkg)
        return self.d.has_key(pkg)

    def is_installed(self, pkg):
        pkg = str(pkg)
        if self.is_recorded(pkg):
            info = self.d[pkg]
            return info.state=='i' or info.state=='ip'
        else:
            return False

    def list_installed(self):
        list = []
        for (pkg, info) in self.d.iteritems():
            if info.state=='i' or info.state=='ip':
                list.append(pkg)
        return list

    def list_pending(self):
        list = []
        for (pkg, x) in self.dp.iteritems():
            list.append(pkg)
        return list

    def get_info(self, pkg):
        pkg = str(pkg)
        return self.d[pkg]

    def get_version(self, pkg):
        pkg = str(pkg)
        info = self.d[pkg]
        return (info.version, info.release, info.build)

    def is_removed(self, pkg):
        pkg = str(pkg)
        if self.is_recorded(pkg):
            info = self.d[pkg]
            return info.state=='r'
        else:
            return False

    def install(self, pkg, version, release, build, distro = ""):
        """install package with specific version, release, build"""
        pkg = str(pkg)
        if self.is_installed(pkg):
            raise InstallDBError("already installed")
        if config.options and config.options.ignore_comar:
            state = 'ip'
            self.dp[pkg] = True
        else:
            state = 'i'
            
        self.d[pkg] = InstallInfo(state, version, release, build, distro)

    def remove(self, pkg):
        pkg = str(pkg)
        info = self.d[pkg]
        info.state = 'r'
        self.d[pkg] = info

    def purge(self, pkg):
        pkg = str(pkg)
        if self.d.has_key(pkg):
            del self.d[pkg]

installdb = None

def init():
    installdb = InstallDB()

