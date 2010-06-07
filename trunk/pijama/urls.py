from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pijama/', include('pijama.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),
    (r'^pijama/', 'webapp.views.index'),
    (r'^sources/', 'webapp.views.sources'),
    (r'^binaries/', 'webapp.views.binaries'),
    (r'^packagers/$', 'webapp.views.packagers'),
    (r'^search/$', 'webapp.views.search'),
    (r'^searchresult/$', 'webapp.views.searchresult'),
    (r'^packagers/(?P<packagername>.*)/$', 'webapp.views.packagersdetails'),
    (r'^source/(?P<packagename>[a-z-A-Z0-9]*)/', 'webapp.views.sourcedetails'),
    (r'^binary/(?P<packagename>[a-z-A-Z0-9]*)/', 'webapp.views.binarydetails'),
)
