from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^choose/$', 'web.ciftci.views.choose_repository'),
    (r'^list/$', 'web.ciftci.views.list_repository'),
    (r'^list/(?P<repo_name>.*)/$', 'web.ciftci.views.list_repository')
)
