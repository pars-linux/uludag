from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^choose/$', 'web.ciftci.views.choose_repository'),
    (r'^transfer/$', 'web.ciftci.views.transfer_packages'),
    (r'^sync/$', 'web.ciftci.views.sync_repositories'),
    (r'^list/$', 'web.ciftci.views.list_repository'),
    (r'^list/(?P<repo_name>.*)/$', 'web.ciftci.views.list_repository')
)
