from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Index
    (r'^$', 'noan.repository.views.page_index'),
    (r'^(?P<distName>[^/]+)/$', 'noan.repository.views.page_index'),
    # Sources
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/$', 'noan.repository.views.page_sources'),
    # Source
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/$', 'noan.repository.views.page_source'),
    # Package
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/$', 'noan.repository.views.page_package'),
    # Binary
    (r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/(?P<binaryNo>\d+)/$', 'noan.repository.views.page_binary'),
)
