from django.conf.urls.defaults import *

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Users
    (r'^$', 'noan.profile.views.main'),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'profile/login.html'}),
    (r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'profile/logout.html'}),

    (r'^list/$', 'noan.profile.views.get_user_list'),
    #FIXME: After logged in, users are redirected to profile page. It has not been implemented yet.
    #FIXME: Now just redirect them to main page.
    (r'^profile/$', 'noan.profile.views.user_profile'),
    (r'^detail/(?P<userName>[\w-]+)/$', 'noan.profile.views.view_user_detail'),
)
