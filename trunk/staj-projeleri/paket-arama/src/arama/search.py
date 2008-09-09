from lib import *

def index(q=None):
    """
    term in:pkg => term in pkg
    in:pkg      => paths in pkg
    p:pkg       => packages like pkg
    term        => path in all packages    
    """
    
    if q:
        s = Search()
        # A workaround here: should be improved:
        if ' in:'in q:
            # term in:pkg
            in_start = q.find('in:')
            in_end = in_start + 4
            term = q[:in_start-1]
            pkg = q[in_end-1:]
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
         return (header % 'No search terms entered.') + footer