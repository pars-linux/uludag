from django.conf.urls.defaults import *


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('pakettif.pathsearch.views',
    (r'^$', 'index'),
    (r'^package/(?P<package_name>[-.0-9A-Za-z]+)/list/$', 'list_package_contents'),
    (r'^package/(?P<package_name>[-.0-9A-Za-z]+)/(?P<term>[-.0-9A-Za-z]+)/$', 'search_in_package'),
    (r'^package/(?P<package_name>[-.0-9A-Za-z]+)/$', 'search_for_package'),
    (r'^(?P<term>[-.0-9A-Za-z]+)/$', 'search_in_all_packages'),
    
)

"""
/search/package/glibc/test.py -> search for test.py in glibc package.

/search/package/sahip -> search for package named sahip.

1. /search/package/{packagename}/{term} > search for term in a package
2. /search/package/{packagename} > search for package
3. /search/{term} > search for term in all packages. post:group->only package names, clicked -> 3.
"""