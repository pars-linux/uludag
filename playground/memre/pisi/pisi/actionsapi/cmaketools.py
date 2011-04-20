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

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# Pisi Modules
import pisi.context as ctx
from pisi.util import join_path

# ActionsAPI Modules
import pisi.actionsapi
import pisi.actionsapi.get as get
from pisi.actionsapi.shelltools import system
from pisi.actionsapi.shelltools import export
from pisi.actionsapi.shelltools import can_access_file
from pisi.actionsapi.shelltools import unlink

crosscompiling = ctx.config.values.build.crosscompiling
if crosscompiling:
    ctx.ui.info(_("cross compiling"))
    export('QTDIR', "%s/usr/qt/4" % get.sysroot())

    export('QMAKE_PLATFORM', "linux-g++")
    export('QMAKESPEC',      "%s/usr/qt/4/mkspecs/linux-g++" % get.sysroot())

    export('QMAKE_CC',   get.CC())
    export('QMAKE_AR',   get.AR())
    export('QMAKE_CXX',  get.CXX())
    export('QMAKE_LINK', get.CXX())
    export('QMAKE_LINK_SHLIB', get.CXX())

    export('QMAKE_CFLAGS',   "%s %s -Wno-psabi -I%s/usr/qt/4/include" % (get.CPPFLAGS(), get.CFLAGS(), get.sysroot()))
    export('QMAKE_CXXFLAGS', "%s %s -Wno-psabi -fno-exceptions -fno-rtti -I%s/usr/qt/4/include" % (get.CPPFLAGS(), get.CXXFLAGS(), get.sysroot()))
    export('QMAKE_LDFLAGS',   "%s" % get.LDFLAGS())
    export('QMAKE_RPATH',     "-Wl,-rpath-link,")

    export('QMAKE_INCDIR',        "%s/usr/qt/4/include" % get.sysroot())
    export('QMAKE_INCDIR_QT',     "%s/usr/qt/4/include" % get.sysroot())
    export('QMAKE_INCDIR_X11',    "%s/usr/include/X11" % get.sysroot())
    export('QMAKE_INCDIR_OPENGL', "%s/usr/include" % get.sysroot())
    export('QMAKE_LIBS',          "%s/usr/qt/4/lib" % get.sysroot())
    export('QMAKE_LIBS_QT',       "qt")
    export('QMAKE_LIBS_X11',      "")
    export('QMAKE_LIBS_OPENGL',   "%s/usr/lib" % get.sysroot())

    export('INCLUDEPATH', "%s/usr/qt/4/include" % get.sysroot())
    export('INCLUDE',     "%s/usr/qt/4/include" % get.sysroot())
    export('LIB',         "%s/usr/qt/4/include" % get.sysroot())

    export('QMAKE_QMAKE', "/usr/qt/4/bin/qmake")
    export('QMAKE_MOC',   "/usr/qt/4/bin/moc")
    export('QMAKE_UIC',   "/usr/qt/4/bin/uic")
    export('QMAKE_UIC3',  "/usr/qt/4/bin/uic3")
    export('QMAKE_LRELEASE',      "/usr/qt/4/bin/lrelease")
    export('QMAKE_LUPDATE',       "/usr/qt/4/bin/lupdate")
    export('QMAKE_QDBUSCPP2XML',  "/usr/qt/4/bin/qdbuscpp2xml4")
    export('QMAKE_QDBUSXML2CPP',  "/usr/qt/4/bin/qdbusxml2cpp4")

    export('QMAKE_STRIP', "true") # we dont want qmake to strip executables, pisi does this if neccessary.

else:
    ctx.ui.info(_("native compiling"))


class ConfigureError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)
        if can_access_file('config.log'):
            ctx.ui.error(_('Please attach the config.log to your bug report:\n%s/config.log') % os.getcwd())

class MakeError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

class InstallError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

class RunTimeError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

def configure(parameters = '', installPrefix = '/%s' % get.defaultprefixDIR(), sourceDir = '.'):
    '''configure source with given cmake parameters = "-DCMAKE_BUILD_TYPE -DCMAKE_CXX_FLAGS ... "'''
    if can_access_file(join_path(sourceDir, 'CMakeLists.txt')):
        args = 'cmake -Wdev \
                      -DCMAKE_BUILD_TYPE=Release \
                      -DCMAKE_INSTALL_PREFIX=%s \
                      -DCMAKE_C_FLAGS="%s" \
                      -DCMAKE_CXX_FLAGS="%s" \
                      -DCMAKE_CPP_FLAGS="%s" \
                      -DCMAKE_LD_FLAGS="%s" \
                      %s %s' % (installPrefix, get.CFLAGS(), get.CXXFLAGS(), get.CPPFLAGS(), get.LDFLAGS(), parameters, sourceDir)

        if crosscompiling:
            args = "sb2 %s \
                     -DCMAKE_TOOLCHAIN_FILE=/opt/toolchain/armv7l/c2_parm.cmake \
                     " % args

        if system(args):
            raise ConfigureError(_('Configure failed.'))
    else:
        raise ConfigureError(_('No configure script found for cmake.'))

def make(parameters = ''):
    '''build source with given parameters'''
    if ctx.config.get_option("verbose") and ctx.config.get_option("debug"):
        command = 'make VERBOSE=1 %s %s' % (get.makeJOBS(), parameters)
    else:
        command = 'make %s %s' % (get.makeJOBS(), parameters)

    if crosscompiling:
        command = "sb2 %s" % command

    if system(command):
        raise MakeError(_('Make failed.'))

def fixInfoDir():
    infoDir = '%s/usr/share/info/dir' % get.installDIR()
    if can_access_file(infoDir):
        unlink(infoDir)

def install(parameters = '', argument = 'install'):
    '''install source into install directory with given parameters'''
    # You can't squeeze unix paths with things like 'bindir', 'datadir', etc with CMake
    # http://public.kitware.com/pipermail/cmake/2006-August/010748.html
    args = 'make DESTDIR="%(destdir)s" \
                 %(parameters)s \
                 %(argument)s' % {
                                     'destdir'      : get.installDIR(),
                                     'parameters'   : parameters,
                                     'argument'     : argument,
                                 }

    if crosscompiling:
        args = "sb2 %s" % args

    if system(args):
        raise InstallError(_('Install failed.'))
    else:
        fixInfoDir()

def rawInstall(parameters = '', argument = 'install'):
    '''install source into install directory with given parameters = PREFIX=%s % get.installDIR()'''
    if can_access_file('makefile') or can_access_file('Makefile') or can_access_file('GNUmakefile'):
        if system('make %s %s' % (parameters, argument)):
            raise InstallError(_('Install failed.'))
        else:
            fixInfoDir()
    else:
        raise InstallError(_('No Makefile found.'))
