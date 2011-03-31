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

# standard python modules
import os
import glob

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# Pisi Modules
import pisi.context as ctx

# ActionsAPI Modules
import pisi.actionsapi
import pisi.actionsapi.get as get
from pisi.actionsapi.shelltools import system
from pisi.actionsapi.shelltools import can_access_file
from pisi.actionsapi.shelltools import export
from pisi.actionsapi.shelltools import unlink

crosscompiling = ctx.config.values.build.crosscompiling
native_arch_dir = '%s-linux-thread-multi' % get.BUILD().split('-')[0]
target_arch_dir = "" # neccessary only with cross-build
perl_cmd = 'perl'
make_cmd = 'make'

if crosscompiling:
    ctx.ui.info(_("cross compiling"))
    if get.ARCH().startswith('arm'):
        pisi.actionsapi.variables.glb.generals.architecture = 'arm'
        target_arch_dir = "arm-linux-thread-multi"
        # pisi.actionsapi.variables.glb.generals.architecture = 'arm'
        # perl_cmd = 'sb2 %s/usr/bin/perl' % get.sysroot() # perl_cmd
        # perl_cmd = 'sb2 %s' % perl_cmd
        # make_cmd = 'sb2 %s' % make_cmd
else:
    ctx.ui.info(_("native compiling"))

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
        if system('%s Build.PL installdirs=vendor destdir=%s' % (perl_cmd, get.installDIR())):
            raise ConfigureError, _('Configure failed.')
    else:
        if system('%s Makefile.PL %s PREFIX=/usr INSTALLDIRS=vendor DESTDIR=%s' % (perl_cmd, parameters, get.installDIR())):
            raise ConfigureError, _('Configure failed.')

def make(parameters = ''):
    '''make source with given parameters.'''
    if can_access_file('Makefile'):
        if system('%s %s' % (make_cmd, parameters)):
            raise MakeError, _('Make failed.')
    else:
        if system('%s Build %s' % (make_cmd, parameters)):
            raise MakeError, _('perl build failed.')

def install(parameters = 'install'):
    '''install source with given parameters.'''
    if can_access_file('Makefile'):
        if system('%s %s' % (make_cmd, parameters)):
            raise InstallError, _('Make failed.')
    else:
        if system('%s Build install' % perl_cmd):
            raise MakeError, _('perl install failed.')

    # temporary fix
    if crosscompiling:
        print " ==> Cross build!!!!!!!!!!!"
        fix_dir_list = os.popen("find %s -name 'x86_64-linux-thread-multi'" % get.installDIR()).read().split()
        for dir in fix_dir_list:
            print 'mv %s %s/%s' % (dir, "/".join(dir.split('/')[:-1]), target_arch_dir)
            os.system('mv %s %s/%s' % (dir, "/".join(dir.split('/')[:-1]), target_arch_dir))

    removePacklist()

def removePacklist():
    ''' cleans .packlist file from perl packages '''
    path = '%s/%s' % (get.installDIR(), "/usr/lib/perl5/vendor_perl/%s/%s-linux-thread-multi/auto/" % (get.curPERL(), get.HOST().split("-")[0]))
    for root, dirs, files in os.walk(path):
        for packFile in files:
            if packFile == ".packlist":
                if can_access_file('%s/%s' % (root, packFile)):
                    unlink('%s/%s' % (root, packFile))
