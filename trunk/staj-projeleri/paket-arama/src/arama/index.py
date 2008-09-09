from lib import *
import gettext
__trans = gettext.translation('paketarama', fallback=True)
_ = __trans.ugettext

def index():
    help = TableGenerator((_('Usage'), _('Meaning')),
                          (
                            ('term in:pkg  ' , 'term in pkg'),
                            ('in:pkg'      , 'all paths in pkg'),
                            ('p:pkg'       , 'packages like pkg'),
                            ('p:'          , 'all packages'), 
                            ('term'        , 'path in all packages'),  
                           )
                          ).table.code
 
    return header % 'Usage' + help +footer