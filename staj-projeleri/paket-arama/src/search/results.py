#/usr/bin/python
# -*- coding: utf-8 -*-

from lib import *
from lib import _
#import gettext
#__trans = gettext.translation('arama', fallback=True)
#_ = __trans.ugettext

def escape(text):
    return text.replace('\\','').replace('--','').replace('/*','').\
    replace("'", "").replace("\"", "").replace('=','').replace('(','').\
    replace(')','').replace('%','').replace(";", "").replace('$', '').\
    replace('^', '').replace('#', '').replace('?', '')

def index(v=2008, q=None):
    """
    term in:pkg => term in pkg
    in:pkg      => paths in pkg
    p:pkg       => packages like pkg
    term        => path in all packages    
    """
    if v not in versions:
        v = 2008
        
    if q:
        q = escape(q)
        s = Search(v)
        # A workaround here: should be improved:
        if ' in:' in q:
            # term in:pkg
            in_start = q.find('in:')
            in_end = in_start + 4
            term = q[:in_start-1]
            pkg = q[in_end-1:]
            if term == ' ':
                term = '" "'
            return s.search_in_package(pkg, term)
        elif q.strip().startswith('in:'):
            # in:pkg
            pkg = q[3:].strip()
            return  s.list_package_contents(pkg)
        elif q.strip().startswith('p:'):
            # p:pkg
            pkg = q[2:].strip()
            return s.search_for_package(pkg)
        else:
            # term
            return s.search_in_all_packages(q)
    else:
         return (header(v) % _('No search terms entered.')) + footer()