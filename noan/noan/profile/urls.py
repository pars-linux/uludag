from django.conf.urls.defaults import *

# Enable the admin interface:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Users
    url(r'^$', 'noan.profile.views.main', name="profile"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'profile/login.html'}, name="profile-login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'profile/logout.html'}, name="profile-logout"),

    url(r'^list/$', 'noan.profile.views.get_user_list', name="profile-list"),
    url(r'^profile/$', 'noan.profile.views.user_profile', name="profile-edit"),
    url(r'^change-password/$', 'noan.profile.views.change_password', name="profile-password"),
    url(r'^detail/(?P<userName>[\w-]+)/$', 'noan.profile.views.view_user_detail', name="profile-info"),
)
