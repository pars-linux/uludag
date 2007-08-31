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

    def list_installed(self):
        packages_path = os.path.join(ctx.config.lib_dir(), "package")
        return map(lambda x:pisi.util.parse_package_name(x)[0], os.listdir(packages_path))

    def has_package(self, package):
        return self.installed_pkgs.has_key(package)

    def get_files(self, package):
        files = pisi.files.Files()
        files_xml = os.path.join(self._package_path(package), ctx.const.files_xml)
        files.read(files_xml)
        return files

    def get_info(self, package):
        files_xml = os.path.join(self._package_path(package), ctx.const.files_xml)
        ctime = pisi.util.creation_time(files_xml)
        pkg = self.get_package(package)
        info = InstallInfo("i", 
                           pkg.version,
                           pkg.release,
                           pkg.build,
                           pkg.distribution,
                           ctime)
        return info

    def get_package(self, package):
        metadata = pisi.metadata.MetaData()
        metadata_xml = os.path.join(self._package_path(package), ctx.const.metadata_xml)
        metadata.read(metadata_xml)
        return metadata.package

    def list_pending(self):
        raise Exception(_('Not implemented'))

    def clear_pending(self, package):
        raise Exception(_('Not implemented'))

    def _package_path(self, package):

        if installed_pkgs.has_key(package):
            return os.path.join(packages_path, "%s-%s" % (package, installed_pkgs[package]))

        raise Exception(_('Package %s is not installed') % package)
