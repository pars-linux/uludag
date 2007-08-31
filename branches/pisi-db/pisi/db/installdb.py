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
#
# installation database
#

import os
import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# PiSi
import pisi
import pisi.context as ctx
import pisi.files
import pisi.util

class InstallDBError(pisi.Error):
    pass

class InstallInfo:

    state_map = { 'i': _('installed'), 'ip':_('installed-pending') }

    def __init__(self, state, version, release, build, distribution, time):
        self.state = state
        self.version = version
        self.release = release
        self.build = build
        self.distribution = distribution
        self.time = time

    def one_liner(self):
        import time
        time_str = time.strftime("%d %b %Y %H:%M", self.time)
        s = '%2s|%10s|%6s|%6s|%8s|%12s' % (self.state, self.version, self.release,
                                   self.build, self.distribution,
                                   time_str)
        return s

    def __str__(self):
        s = _("State: %s\nVersion: %s, Release: %s, Build: %s\n") % \
            (InstallInfo.state_map[self.state], self.version,
             self.release, self.build)
        import time
        time_str = time.strftime("%d %b %Y %H:%M", self.time)
        s += _('Distribution: %s, Install Time: %s\n') % (self.distribution,
                                                          time_str)
        return s

class InstallDB:

    # TODO: configpending
    def __init__(self):

        packages_path = os.path.join(ctx.config.lib_dir(), "package")
        self.installed_pkgs = dict(map(lambda x:pisi.util.parse_package_name(x),
                                       os.listdir(packages_path)))

        self.config_pending = []
        pending_info_path = os.path.join(ctx.config.lib_dir(), ctx.const.info_dir, ctx.const.config_pending)
        if os.path.exists(pending_info_path):
            self.config_pending = open(pending_info_path, "r").read().split()

    def list_installed(self):
        packages_path = os.path.join(ctx.config.lib_dir(), "package")
        return map(lambda x:pisi.util.parse_package_name(x)[0], os.listdir(packages_path))

    def has_package(self, package):
        return self.installed_pkgs.has_key(package)

    def get_files(self, package):
        files = pisi.files.Files()
        files_xml = os.path.join(self.__package_path(package), ctx.const.files_xml)
        files.read(files_xml)
        return files

    def get_info(self, package):
        files_xml = os.path.join(self.__package_path(package), ctx.const.files_xml)
        ctime = pisi.util.creation_time(files_xml)
        pkg = self.get_package(package)
        info = InstallInfo("i", 
                           pkg.version,
                           pkg.release,
                           pkg.build,
                           pkg.distribution,
                           ctime)
        return info

    # FIXME: notused is for pgraph.py:get_package
    def get_package(self, package, notused=None):
        metadata = pisi.metadata.MetaData()
        metadata_xml = os.path.join(self.__package_path(package), ctx.const.metadata_xml)
        metadata.read(metadata_xml)
        return metadata.package

    def mark_pending(self, package):
        if package not in self.config_pending:
            self.config_pending.append(package)
            self.__write_config_pending()

    def list_pending(self):
        return self.config_pending

    def clear_pending(self, package):
        if package not in self.config_pending:
            self.config_pending.remove(package)
            self.__write_config_pending()

    def __write_config_pending(self):
        pending_info_dir = os.path.join(ctx.config.lib_dir(), ctx.const.info_dir)
        if not os.path.exists(pending_info_dir):
            os.makedirs(pending_info_dir)

        pending_info_file = os.path.join(pending_info_dir, ctx.const.config_pending)
        pending = open(pending_info_file, "w")
        for pkg in set(self.config_pending):
            pending.write("%s\n" % pkg)
        pending.close()

    def __package_path(self, package):

        packages_path = os.path.join(ctx.config.lib_dir(), "package")

        if self.installed_pkgs.has_key(package):
            return os.path.join(packages_path, "%s-%s" % (package, self.installed_pkgs[package]))

        raise Exception(_('Package %s is not installed') % package)
