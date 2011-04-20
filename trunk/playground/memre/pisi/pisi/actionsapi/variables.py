# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

# Standard Python Modules
import os

# Pisi-Core Modules
import pisi.context as ctx

# Set individual information, that are generally needed for ActionsAPI

def exportFlags():
    '''General flags used in actions API.'''

    # first reset environ
    os.environ.clear()
    os.environ.update(ctx.config.environ)

    # Build systems depend on these environment variables. That is why
    # we export them instead of using as (instance) variables.
    values = ctx.config.values
    sysroot = values.general.destinationdirectory
    crosscompiling = ctx.config.values.build.crosscompiling

    os.environ['BUILD']    = values.build.build
    os.environ['HOST']     = values.build.host
    os.environ['TARGET']   = values.build.target
    os.environ['CFLAGS']   = values.build.cflags
    os.environ['CXXFLAGS'] = values.build.cxxflags
    os.environ['CPPFLAGS'] = values.build.cppflags or ""
    os.environ['LDFLAGS']  = values.build.ldflags
    os.environ['USER_LDFLAGS'] = values.build.ldflags
    os.environ['JOBS'] = values.build.jobs

    # http://liste.pardus.org.tr/gelistirici/2009-January/016442.html
    os.environ['CC']  = "%s-gcc" % values.build.host
    os.environ['CPP'] = "%s-gcc -E" % values.build.host
    os.environ['CXX'] = "%s-g++" % values.build.host

    # if we are crosscompiling, some extra flags and variables has to be defined.
    if values.build.crosscompiling:
        os.environ["AR"]      = "%s-ar" % values.build.host
        os.environ["AS"]      = "%s-as" % values.build.host
        os.environ["LD"]      = "%s-ld" % values.build.host
        os.environ['NM']      = "%s-nm" % values.build.host
        os.environ["STRIP"]   = "%s-strip"   % values.build.host
        os.environ["RANLIB"]  = "%s-ranlib"  % values.build.host
        os.environ["OBJDUMP"] = "%s-objdump" % values.build.host
        os.environ["OBJCOPY"] = "%s-objcopy" % values.build.host
        os.environ['FORTRAN'] = "%s-gfortran" % values.build.host
        # FIXME: sb2 has a libtool too, do not export this unless it is neccessary
        # os.environ['LIBTOOL']   = "%s-libtool" % values.build.host

        # FIXME: PATH environmental variable should be changed in sb2
        # os.environ['PATH']  = "%(sysroot)s/bin:%(sysroot)s/sbin:%(sysroot)s/usr/bin:%(sysroot)s/usr/sbin:%(path)s" % { 'sysroot' : sysroot, 'path' : os.environ['PATH'] }
        os.environ['PYTHON_PREFIX'] = "%s/usr" % sysroot
        os.environ['PYTHON']    = "%s/usr/bin/python" % sysroot
        # FIXME: sometimes perl fails with qemu.
        # os.environ['PERL']      = "%s/usr/bin/perl" % sysroot
        os.environ['SBOX_TARGET_ROOT'] = sysroot
        os.environ['SYSROOT']   = sysroot
        os.environ['BUILDARCH'] = os.popen('uname -m').read().strip()
        os.environ['ARCH']      = values.general.architecture

        os.environ['ASFLAGS']   = ""
        os.environ['CPPFLAGS'] += " -isystem%s/usr/include" % sysroot
        os.environ['CFLAGS']   += " -I%s/usr/include" % sysroot
        os.environ['CXXFLAGS'] += " -I%s/usr/include" % sysroot
        os.environ['LDFLAGS']  += " -L%(sysroot)s/lib -Wl,-rpath-link,%(sysroot)s/lib \
                                    -L%(sysroot)s/usr/lib -Wl,-rpath-link,%(sysroot)s/usr/lib \
                                    " % { 'sysroot' : sysroot, }

        os.environ['PKG_CONFIG_SYSROOT_DIR']  = sysroot
        os.environ['PKG_CONFIG_PATH']  = "%s/usr/lib/pkgconfig:%s/usr/qt/4/lib/pkgconfig" % (sysroot, sysroot)
        os.environ['PKGCONFIG']        = "/opt/toolchain/armv7l/bin/pkg-config"

    if crosscompiling:
        print " ==> cross compiling <== "
    else:
        print " ==> native compiling <== "

class Env(object):
    '''General environment variables used in actions API'''
    def __init__(self):

        exportFlags()

        self.__vars = {
            'pkg_dir'     : 'PKG_DIR',
            'work_dir'    : 'WORK_DIR',
            'install_dir' : 'INSTALL_DIR',
            'build_type'  : 'PISI_BUILD_TYPE',

            'src_name'    : 'SRC_NAME',
            'src_version' : 'SRC_VERSION',
            'src_release' : 'SRC_RELEASE',

            'build'       : 'BUILD',
            'host'        : 'HOST',
            'target'      : 'TARGET',

            'cppflags'    : 'CPPFLAGS',
            'cflags'      : 'CFLAGS',
            'cxxflags'    : 'CXXFLAGS',
            'ldflags'     : 'LDFLAGS',

            'jobs'        : 'JOBS',
            'preload'     : 'LD_PRELOAD'
        }

    def __getattr__(self, attr):

        # Using environment variables is somewhat tricky. Each time
        # you need them you need to check for their value.
        if self.__vars.has_key(attr):
            return os.getenv(self.__vars[attr])
        else:
            return None

class Dirs:
    '''General directories used in actions API.'''
    # TODO: Eventually we should consider getting these from a/the
    # configuration file
    doc = 'usr/share/doc'
    sbin = 'usr/sbin'
    man = 'usr/share/man'
    info = 'usr/share/info'
    data = 'usr/share'
    conf = 'etc'
    localstate = 'var'
    libexec = 'usr/libexec'
    defaultprefix = 'usr'

    # These should be owned by object not the class. Or else Python
    # will bug us with NoneType errors because of uninitialized
    # context (ctx) because of the import in build.py.
    def __init__(self):
        self.values = ctx.config.values
        self.kde = self.values.dirs.kde_dir
        self.qt = self.values.dirs.qt_dir

class Generals:
    '''General informations from /etc/pisi/pisi.conf'''

    def __init__(self):
        self.values = ctx.config.values
        self.architecture = self.values.general.architecture
        self.distribution = self.values.general.distribution
        self.distribution_release = self.values.general.distribution_release

# As we import this module from build.py, we can't init glb as a
# singleton here.  Or else Python will bug us with NoneType errors
# because of uninitialized context (ctx) because of exportFlags().
#
# We import this modue from build.py becase we need to reset/init glb
# for each build.
# See bug #2575
glb = None

def initVariables():
    global glb
    ctx.env = Env()
    ctx.dirs = Dirs()
    ctx.generals = Generals()
    glb = ctx

