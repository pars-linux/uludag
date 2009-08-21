from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Pending
    (r'^pending/$', 'noan.repository.views.page_pending_index'),
    (r'^pending/(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/$', 'noan.repository.views.page_pending'),

    # Users
    (r'^users/$', 'noan.repository.views.page_users'),
    (r'^users/(?P<userName>[^/]+)/$', 'noan.repository.views.page_user'),

    # Index
    (r'^$', 'noan.repository.views.page_index'),
    # Sources
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/$', 'noan.repository.views.page_sources'),
    # Source
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/$', 'noan.repository.views.page_source'),
    # Package
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/$', 'noan.repository.views.page_package'),
    # Binary
    (r'^(?P<distName>[^/]+)-(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/(?P<binaryNo>\d+)/$', 'noan.repository.views.page_binary'),
    # search
    (r'^search/$', 'noan.repository.views.search_form'),
    # Maintainer ack/nack list
    (r'^ack_nack/$','noan.repository.views.AckNackList'),
    # all list of ack/nack
    (r'^statelist/$','noan.repository.views.ListAllAckNack'),
)
