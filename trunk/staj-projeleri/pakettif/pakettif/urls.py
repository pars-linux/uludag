from django.conf.urls.defaults import *
from pakettif.settings import DOCUMENT_ROOT


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pakettif/', include('pakettif.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^$', 'pakettif.pathsearch.views.index'),
    (r'^admin/(.*)', admin.site.root),
    (r'^search/', include('pakettif.pathsearch.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),

)
