from django.conf.urls.defaults import *

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

#FIXME: Remove it on development server.
from noan.settings import DOCUMENT_ROOT

urlpatterns = patterns('',
    # Index
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'repository/'}, name="index"),

    # Repository
    url(r'^repository/', include('noan.repository.urls')),

    # Users
    url(r'^user/', include('noan.profile.urls')),

    # FIXME: This is development only. Remove it on production server.
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': DOCUMENT_ROOT + '/media', 'show_indexes': True}),

    # Admin interface
    url(r'^mudur/doc/', include('django.contrib.admindocs.urls')),
    url(r'^mudur/(.*)', admin.site.root),
)
