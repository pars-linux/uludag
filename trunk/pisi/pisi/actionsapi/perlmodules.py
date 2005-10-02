#!/usr/bin/python
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

# standard python modules
import os

# Pisi Modules
import pisi.context as ctx

# ActionsAPI Modules
import pisi.actionsapi
import pisi.actionsapi.get as get
from pisi.actionsapi.shelltools import system, can_access_file, export

class ConfigureError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

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

def configure(parameters = ''):
    '''configure source with given parameters.'''
    export('PERL_MM_USE_DEFAULT', '1')
    if can_access_file('Build.PL'):
        if system('perl Build.PL installdirs=vendor destdir=%s' % get.installDIR()):
            raise CompileError, '!!! Configure failed...\n'
    else:
        if system('perl Makefile.PL %s PREFIX=/usr INSTALLDIRS=vendor DESTDIR=%s' % (parameters, get.installDIR())):
            raise CompileError, '!!! Configure failed...\n'

def make(parameters = ''):
    '''make source with given parameters.'''
    if can_access_file('Makefile'):
        if system('make %s' % parameters):                  
            raise MakeError, '!!! Make failed...\n'
    else:
        if system('perl Build build'):
            raise MakeError, '!!! Make failed...\n'

def install(parameters = 'install'):
    '''install source with given parameters.'''
     if can_access_file('Makefile'):
        if system('make %s' % parameters):                  
            raise InstallError, '!!! Install failed...\n'
     else:
        if system('perl Build install'):
            raise MakeError, '!!! Install failed...\n'

# FIXME: fix_local_pod % update_pod
