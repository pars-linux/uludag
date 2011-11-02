# -*- coding: utf-8 -*-
#
# Copyright (C) 2010 TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import os
import glob
import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# Pisi Modules
import pisi.context as ctx

# ActionsAPI Modules
import pisi.actionsapi

# ActionsAPI Modules
from pisi.actionsapi import get
from pisi.actionsapi import cmaketools
from pisi.actionsapi import pisitools
from pisi.actionsapi import shelltools
from pisi.actionsapi.shelltools import export

basename = "qt4"

prefix = "/%s" % get.defaultprefixDIR()
libdir = "%s/lib" % prefix
bindir = "%s/bin" % prefix
datadir = "%s/share/%s" % (prefix, basename)
includedir = "%s/include" % prefix
docdir = "/%s/%s" % (get.docDIR(), basename)
examplesdir = "%s/%s/examples" % (libdir, basename)
demosdir = "%s/%s/demos" % (libdir, basename)
importdir = "%s/%s/imports" % (libdir, basename)
plugindir = "%s/%s/plugins" % (libdir, basename)
translationdir = "%s/translations" % datadir
sysconfdir= "/etc"
qmake = "%s/qmake-qt4" % bindir

crosscompiling = ctx.config.values.build.crosscompiling
if crosscompiling:
    ctx.ui.info(_("cross compiling qt4 application"))
    qmake_environment = {
            'QTDIR'          : "%s/usr/qt/4" % get.sysroot(),
            'QMAKESPEC'      : "%s/usr/qt/4/mkspecs/linux-g++" % get.sysroot(),
            'QMAKE_PLATFORM' : "linux-g++",

            'QMAKE_CC'       : get.CC(),
            'QMAKE_AR'       : get.AR(),
            'QMAKE_CXX'      : get.CXX(),
            'QMAKE_LINK'     : get.CXX(),
            'QMAKE_LINK_SHLIB' : get.CXX(),

            'QMAKE_CFLAGS'   : "%s %s -Wno-psabi -I%s/usr/qt/4/include" % (get.CPPFLAGS(), get.CFLAGS(), get.sysroot()),
            'QMAKE_CXXFLAGS' : "%s %s -Wno-psabi -fno-exceptions -fno-rtti -I%s/usr/qt/4/include" % (get.CPPFLAGS(), get.CXXFLAGS(), get.sysroot()),
            'QMAKE_LDFLAGS'  : "%s" % get.LDFLAGS(),
            'QMAKE_RPATH'    : "-Wl,-rpath-link,",

            'QMAKE_INCDIR'     : "%s/usr/qt/4/include" % get.sysroot(),
            'QMAKE_INCDIR_QT'  : "%s/usr/qt/4/include" % get.sysroot(),
            'QMAKE_INCDIR_X11' : "%s/usr/include/X11" % get.sysroot(),
            'QMAKE_INCDIR_OPENGL' : "%s/usr/include" % get.sysroot(),
            'QMAKE_LIBS'       : "-L%s/usr/qt/4/lib" % get.sysroot(),
            'QMAKE_LIBS_QT'    : "qt",
            # 'QMAKE_LIBS_X11' :      ""
            'QMAKE_LIBS_OPENGL' : "%s/usr/lib" % get.sysroot(),

            'INCLUDEPATH'      : "%s/usr/qt/4/include" % get.sysroot(),
            'INCLUDE'          : "%s/usr/qt/4/include" % get.sysroot(),
            'LIB'              : "%s/usr/qt/4/lib" % get.sysroot(),

            'QMAKE_QMAKE'      : "%s/usr/qt/4/bin/qmake" % get.sysroot(),
            'QMAKE_MOC'        : "%s/usr/qt/4/bin/moc" % get.sysroot(),
            'QMAKE_UIC'        : "%s/usr/qt/4/bin/uic" % get.sysroot(),
            'QMAKE_UIC3'       : "%s/usr/qt/4/bin/uic3" % get.sysroot(),
            'QMAKE_LRELEASE'   : "%s/usr/qt/4/bin/lrelease" % get.sysroot(),
            'QMAKE_LUPDATE'    : "%s/usr/qt/4/bin/lupdate" % get.sysroot(),
            'QMAKE_QDBUSCPP2XML' : "%s/usr/qt/4/bin/qdbuscpp2xml4" % get.sysroot(),
            'QMAKE_QDBUSXML2CPP' : "%s/usr/qt/4/bin/qdbusxml2cpp4" % get.sysroot(),

            'QMAKE_STRIP'      : "true", # we dont want qmake to strip executables, pisi does this if neccessary.
            'QT_INCLUDE_DIR'   : '%s/usr/qt/4' % get.sysroot(),
            'QT_LIBRARY_DIR'   : '%s/usr/qt/4/lib' % get.sysroot(),
            'QT_LIBRARIES'     : '%s/usr/qt/4/lib' % get.sysroot()
    } # qmake_environment

    for k, v in qmake_environment.items():
        export(k, v)

else:
    ctx.ui.info(_("native compiling qt4 application"))


class ConfigureError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

def configure(projectfile='', parameters='', installPrefix=prefix):
    if projectfile != '' and not shelltools.can_access_file(projectfile):
        raise ConfigureError(_("Project file '%s' not found.") % projectfile)

    profiles = glob.glob("*.pro")
    if len(profiles) > 1 and projectfile == '':
        raise ConfigureError(_("It seems there are more than one .pro file, you must specify one. (Possible .pro files: %s)") % ", ".join(profiles))

    shelltools.system("%s -makefile %s PREFIX='%s' %s %s" % (qmake, projectfile, installPrefix, get_qmake_environment(), parameters ))
    if crosscompiling:
        pisitools.dosed('Makefile', r'\-(L|I)\/usr(\S*)', '-\\1%s/usr\\2' % get.sysroot())

def make(parameters=''):
    cmaketools.make(parameters)

def install(parameters='', argument='install'):
    cmaketools.install('INSTALL_ROOT="%s" %s' % (get.installDIR(), parameters), argument)

def get_qmake_environment():
    return " ".join( [ "%s='%s'" % (k, v) for k, v in qmake_environment.items() ] )

# def sip_generate():
#    sip_modules = os.popen('find . -name sip/\*.sip').read().split()
#
#    for module in sip_modules:
#        shelltools.system('install -d %s' % module)
#        shelltools.system('sip -I sip -c %(module)s %(module)s/%(module)s.sbf \
#                sip/%(module)s/%(module)s.sip' % 

