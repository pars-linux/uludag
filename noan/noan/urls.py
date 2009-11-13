from django.conf.urls.defaults import *

from noan.settings import DOCUMENT_ROOT

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Repository
    # FIXME: Decide what to do with our home-page. Do not redirect it to repository app
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/repository/'}),
    (r'^repository/', include('noan.repository.urls')),

    # Users
    (r'^user/', include('noan.profile.urls')),

    # Enable the admin interface:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    # Don't handle /media/
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),

    # login
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
)
