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


# Pisi Modules
import pisi.context as ctx

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.ugettext

# ActionsAPI Modules
import pisi.actionsapi
import pisi.actionsapi.get as get
from pisi.actionsapi.shelltools import system

scons_cmd = "scons" if not get.ARCH().startswith('arm') else "sb2 %s/usr/bin/scons" % get.sysroot()

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

def make(parameters = ''):
    if system('%s %s %s' % (scons_cmd, get.makeJOBS(), parameters)):
        raise MakeError(_('Make failed.'))

def install(parameters = 'install', prefix = get.installDIR(), argument='prefix'):
    if system('%s %s=%s %s' % (scons_cmd, argument, prefix, parameters)):
        raise InstallError(_('Install failed.'))
