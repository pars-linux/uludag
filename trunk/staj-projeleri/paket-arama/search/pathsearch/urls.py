# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('search.pathsearch.views',
    (r'^$', 'index'),
    (r'^(?P<version>[-0-9A-Za-z]+)/$', 'index'),
    (r'^(?P<version>[-0-9A-Za-z]+)/package/(?P<package_name>[-_.0-9A-Za-z]+)/$', 'list_package_contents'),
    (r'^(?P<version>[-0-9A-Za-z]+)/package/(?P<package_name>[-_.0-9A-Za-z]+)/(?P<term>[-/_.0-9A-Za-z]+)', 'search_in_package'),
    (r'^(?P<version>[-0-9A-Za-z]+)/packages/$', 'search_for_package'),
    (r'^(?P<version>[-0-9A-Za-z]+)/packages/(?P<package_name>[-_.0-9A-Za-z]+)/$', 'search_for_package'),
    (r'^(?P<version>[-0-9A-Za-z]+)/(?P<term>[-_.0-9A-Za-z]+)/$', 'search_in_all_packages'),
    
)

"""
/search/pardus-2009/package/glibc/test.py -> search for test.py in glibc package.

/search/pardus-2009/packages/sahip -> search for package named sahip.

1. /search/pardus-2009/package/{packagename}/{term} > search for term in a package
2. /search/pardus-2009/package/{packagename} -> contents of package
3. /search/pardus-2009/packages/{packagename} > search for package
4. /search/pardus-2009/{term} > search for term in all packages. post:group->only package names, clicked -> 3.
"""
