from django.conf.urls.defaults import *

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Users
    (r'^$', 'noan.profile.views.main'),
    (r'^info/(?P<userName>[\w-]+)/$', 'noan.profile.views.get_user_info'),
)
