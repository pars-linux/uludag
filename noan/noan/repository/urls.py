from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Pending
    (r'^pending/$', 'noan.repository.views.page_pending_index'),
    (r'^pending/(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/$', 'noan.repository.views.list_pending_packages'),

    # Users
    (r'^users/$', 'noan.repository.views.page_users'),
    (r'^users/(?P<userName>[^/]+)/$', 'noan.repository.views.page_user'),

    # Index
    (r'^$', 'noan.repository.views.repository_index'),
    # Sources
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/$', 'noan.repository.views.list_source_packages'),
    # Source
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/$', 'noan.repository.views.view_source_package_detail'),
    # Package
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/$', 'noan.repository.views.page_package'),
    # Binary
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/(?P<binaryNo>\d+)/$', 'noan.repository.views.page_binary'),
)
