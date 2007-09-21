from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^list/$', 'web.ciftci.views.list_repository'),
)
