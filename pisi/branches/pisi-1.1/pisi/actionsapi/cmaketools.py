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
from pisi.actionsapi.shelltools import can_access_file
from pisi.actionsapi.shelltools import unlink

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
        args = 'cmake -DCMAKE_INSTALL_PREFIX=%s %s %s' % (installPrefix, parameters, sourceDir)

        if system(args):
            raise ConfigureError(_('Configure failed.'))
    else:
        raise ConfigureError(_('No configure script found for cmake.'))

def make(parameters = ''):
    '''build source with given parameters'''
    if can_access_file('Makefile'):
        if system('make %s %s' % (get.makeJOBS(), parameters)):
            raise MakeError(_('Make failed.'))
    else:
        raise InstallError(_('No Makefile found.'))

def fixInfoDir():
    infoDir = "%s/usr/share/info/dir" % get.installDIR()
    if can_access_file(infoDir):
        unlink(infoDir)

def install(parameters = '', argument = 'install'):
    '''install source into install directory with given parameters'''
    if can_access_file('makefile') or can_access_file('Makefile') or can_access_file('GNUmakefile'):
        args = 'make prefix=%(prefix)s/%(defaultprefix)s \
                datadir=%(prefix)s/%(data)s \
                infodir=%(prefix)s/%(info)s \
                localstatedir=%(prefix)s/%(localstate)s \
                mandir=%(prefix)s/%(man)s \
                sysconfdir=%(prefix)s/%(conf)s \
                %(parameters)s \
                %(argument)s' % {'prefix': get.installDIR(),
                            'defaultprefix': get.defaultprefixDIR(),
                            'man': get.manDIR(),
                            'info': get.infoDIR(),
                            'localstate': get.localstateDIR(),
                            'conf': get.confDIR(),
                            'data': get.dataDIR(),
                            'parameters': parameters,
                            'argument':argument}

        if system(args):
            raise InstallError(_('Install failed.'))
        else:
            fixInfoDir()
    else:
        raise InstallError(_('No Makefile found.'))

def rawInstall(parameters = '', argument = 'install'):
    '''install source into install directory with given parameters = PREFIX=%s % get.installDIR()'''
    if can_access_file('makefile') or can_access_file('Makefile') or can_access_file('GNUmakefile'):
        if system('make %s %s' % (parameters, argument)):
            raise InstallError(_('Install failed.'))
        else:
            fixInfoDir()
    else:
        raise InstallError(_('No Makefile found.'))
