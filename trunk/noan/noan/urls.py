from django.conf.urls.defaults import *

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Index
    url(r'^$', 'django.views.generic.simple.redirect_to', {'url': 'repository/'}, name="index"),

    # Repository
    url(r'^repository/', include('noan.repository.urls')),

    # Users
    url(r'^user/', include('noan.profile.urls')),

    # Admin interface
    url(r'^mudur/doc/', include('django.contrib.admindocs.urls')),
    url(r'^mudur/(.*)', admin.site.root),
)
