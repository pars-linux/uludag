#/usr/bin/python
# -*- coding: utf-8 -*-
from settings import *
from lib import *
from lib import _

#import gettext
#__trans = gettext.translation('arama', fallback=True)
#_ = __trans.ugettext


def index():
    help = TableGenerator((_('Usage'), _('Meaning')),
                          (
                            (_('term in:package  ')  , _('search for "term" in "package"')),
                            (_('in:package')         , _('list all paths in "package"')),
                            (_('p:package')          , _('search for packages like "package"')),
                            (_('p:')                 , _('list all packages')), 
                            (_('term')               , _('search for "term" in all package contents')),  
                           )
                          ).table.code
 
    return header % _('Usage') + help +footer