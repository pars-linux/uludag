#!/usr/bin/python
# -*- coding: utf-8 -*-


#standart python modules
import  os
import glob
import shutil
from gettext import translation

__trans = translation('pisi', fallback=True)
_ = __trans.ugettext



# Pisi Modules
import pisi.context as ctx
from pisi.util  import join_path

# ActionsAPI Modules
import pisi.actionsapi
import pisi.actionsapi.get as get
from pisi.actionsapi.shelltools import system, unlink



class InstallError(pisi.actionsapi.Error):
    def __init__(self, value=''):
        pisi.actionsapi.Error.__init__(self, value)
        self.value = value
        ctx.ui.error(value)

def get_rubygemdir():
    return os.popen("ruby -rubygems -e 'puts Gem::dir' 2").read().strip()

def remove_cachedir():
    cache_dir = "%s%s/cache"  % (get.installDIR(), get_rubygemdir())
    try:
        shutil.rmtree(cache_dir)
    except OSError:
        error(_('ActionsAPI [unlinkDir]: Operation not permitted: %s') % (sourceDirectory))

def install(parameters = ''):
    installdir = join_path(get.installDIR(), get_rubygemdir())
    bindir = join_path(get.installDIR(), "/usr/bin")
    source = "%s-%s" %(get.srcNAME()[8:], get.srcVERSION())
    sourcedir = join_path(get.workDIR(), source)

    print installdir ,  bindir,  source, sourcedir 
    if system("gem install -E --local --install-dir %s  --bindir %s --force %s" % (installdir, bindir, sourcedir)):
        raise InstallError, _('Install failed.')








