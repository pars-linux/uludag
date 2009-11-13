from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Pending
    (r'^pending/$', 'noan.repository.views.page_pending_index'),
    (r'^pending/(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/$', 'noan.repository.views.list_pending_packages'),

    # Index
    (r'^$', 'noan.repository.views.repository_index'),
    # List all source pakages
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/$', 'noan.repository.views.list_source_packages'),
    # Details of <Source> section in pspec.xml
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/$', 'noan.repository.views.view_source_detail'),
    # Details of <Package> section in pspec.xml
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/$', 'noan.repository.views.view_package_detail'),
    # Binary package (*.pisi) detail
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)-(?P<binaryNo>\d+)/$', 'noan.repository.views.view_binary_detail'),
)
