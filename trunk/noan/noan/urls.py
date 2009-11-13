from django.conf.urls.defaults import *

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

    # login
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
)
