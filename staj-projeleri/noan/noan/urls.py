from django.conf.urls.defaults import *
from noan.repository.views import log_out
# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Repository
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/repository/'}),
    (r'^repository/', include('noan.repository.urls')),

    # Enable the admin interface:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    #login
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    # logout
    (r'^logout/$',log_out),
)
