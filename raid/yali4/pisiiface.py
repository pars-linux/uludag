# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# PiSİ module for YALI

import os
import time

import dbus
import pisi
import yali4.postinstall
from yali4.constants import consts

repodb = pisi.db.repodb.RepoDB()

def initialize(ui, with_comar = False, nodestDir = False):
    options = pisi.config.Options()
    if not nodestDir:
        options.destdir = consts.target_dir
    options.yes_all = True
    # wait for chroot_dbus to initialize
    # generally we don't need this but I think this is safer
    for i in range(20):
        try:
            bus = dbus.SystemBus()
            break
        except dbus.DBusException:
            time.sleep(1)
    pisi.api.set_dbus_sockname("%s/var/run/dbus/system_bus_socket" % options.destdir)

    try:
        pisi.api.set_dbus_timeout(1200)
    except AttributeError, e:
        # An old pisi running on disc, forget the dbus
        pass

    pisi.api.set_userinterface(ui)
    pisi.api.set_options(options)
    pisi.api.set_comar(with_comar)
    pisi.api.set_signal_handling(False)

def add_repo(name=None, uri=None):
    if name and uri:
        pisi.api.add_repo(name, uri)

def add_cd_repo():
    cd_repo_name = consts.cd_repo_name
    cd_repo_uri = consts.cd_repo_uri
    if not repodb.has_repo(cd_repo_name):
        add_repo(cd_repo_name, cd_repo_uri)
        update_repo(cd_repo_name)

def add_remote_repo(name, uri):
    if not repodb.has_repo(name):
        add_repo(name, uri)
        update_repo(name)

def switch_to_pardus_repo():
    cd_repo_name = consts.cd_repo_name
    pardus_repo_name = consts.pardus_repo_name
    pardus_repo_uri = consts.pardus_repo_uri

    remove_repo(cd_repo_name)
    add_repo(pardus_repo_name, pardus_repo_uri)

def update_repo(name):
    pisi.api.update_repo(consts.cd_repo_name)

def remove_repo(name):
    pisi.api.remove_repo(name)

def finalize():
    pass

def install(pkg_name_list):
    pisi.api.install(pkg_name_list)

def install_all():
    install(get_available())

def get_available():
    return pisi.api.list_available()

def get_available_len():
    return len(get_available())

def get_pending():
    return pisi.db.installdb.InstallDB().list_pending()

def get_pending_len():
    return len(get_pending())

def configure_pending():
    # dirty hack for COMAR to find scripts.
    os.symlink("/",consts.target_dir + consts.target_dir)
    pisi.api.configure_pending()
    os.unlink(consts.target_dir + consts.target_dir)

def check_package_hash(pkg_name):
    repo_path = os.path.dirname(consts.cd_repo_uri)

    pkg = pisi.db.packagedb.PackageDB().get_package(pkg_name)
    file_name = pisi.util.package_name(pkg.name,
                                       pkg.version,
                                       pkg.release,
                                       pkg.build)
    file_hash = pisi.util.sha1_file(
        os.path.join(repo_path, file_name))

    if pkg.packageHash == file_hash:
        return True

    return False
