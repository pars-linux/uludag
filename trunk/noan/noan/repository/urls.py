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
"""
(r'^packages/(?P<maintainer>[^/]+)/$', 'noan.repository.views.packages'),
#
(r'^releases/$', 'noan.repository.views.releases'),
(r'^releases/(?P<maintainer>[^/]+)/(?P<resolution>[^/]+)/$', 'noan.repository.views.releases'),
#
(r'^package/(?P<packageName>[^/]+)/$', 'noan.repository.views.package'),
(r'^package/(?P<packageName>[^/]+)/(?P<version>[^/]+)/$', 'noan.repository.views.release'),
#
(r'^package/(?P<packageName>[^/]+)/(?P<version>[^/]+)/(?P<result>[^/]+)/(?P<caseNo>[^/]+)/$', 'noan.repository.views.vote'),
#
(r'^releases-ack/$', 'noan.repository.views.releases_ack'),
(r'^releases-nack/$', 'noan.repository.views.releases_nack'),
#
#(r'^ajax/packages/(?P<maintainer>[^/]+)/$', 'noan.repository.views.ajax_packages'),
#(r'^ajax/releases/(?P<maintainer>[^/]+)/(?P<resolution>[^/]+)/$', 'noan.repository.views.ajax_releases'),
"""
