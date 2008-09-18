from django.conf.urls.defaults import *

urlpatterns = patterns('pakettif.pathsearch.views',
    (r'^$', 'index'),
    (r'^(?P<version>[0-9]+)/$', 'index'),
    (r'^(?P<version>[0-9]+)/package/(?P<package_name>[-.0-9A-Za-z]+)/list/$', 'list_package_contents'),
    (r'^(?P<version>[0-9]+)/package/(?P<package_name>[-.0-9A-Za-z]+)/(?P<term>[-.0-9A-Za-z]+)/$', 'search_in_package'),
    (r'^(?P<version>[0-9]+)/package/(?P<package_name>[-.0-9A-Za-z]+)/$', 'search_for_package'),
    (r'^(?P<version>[0-9]+)/(?P<term>[-.0-9A-Za-z]+)/$', 'search_in_all_packages'),
    
)

"""
/search/2008/package/glibc/test.py -> search for test.py in glibc package.

/search/2008/package/sahip -> search for package named sahip.

1. /search/2008/package/{packagename}/{term} > search for term in a package
2. /search/2008/package/{packagename} > search for package
3. /search/2008/{term} > search for term in all packages. post:group->only package names, clicked -> 3.
"""