from django.conf.urls.defaults import *

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Users
    (r'^$', 'noan.profile.views.main'),
    (r'^list/$', 'noan.profile.views.get_user_list'),
    (r'^detail/(?P<userName>[\w-]+)/$', 'noan.profile.views.view_user_detail'),
)
