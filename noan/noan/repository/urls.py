from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Index
    url(r'^$', 'noan.repository.views.repository_index', name="repo-index"),

    # Pending packages
    url(r'^pending/$', 'noan.repository.views.page_pending_index', name="repo-pending-index"),
    url(r'^pending/(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/$', 'noan.repository.views.list_pending_packages', name="repo-pending"),

    # List all source pakages
    url(r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/$', 'noan.repository.views.list_source_packages', name="repo-source-list"),
    # Details of <Source> section in pspec.xml
    url(r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/$', 'noan.repository.views.view_source_detail', name="repo-source-info"),
    # List of isa packages
    url(r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<repoType>[^/]+)/isa/(?P<isA>[^/]+)/$', 'noan.repository.views.view_isa_info', name="isa-source-info"),
    # List of partOf packages
    url(r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<repoType>[^/]+)/partof/(?P<partOf>[^/]+)/$', 'noan.repository.views.view_partof_info', name="partof-source-info"),
    # Binary package (*.pisi) detail
    url(r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)-(?P<binaryNo>\d+)/$', 'noan.repository.views.view_binary_detail', name="repo-binary-info"),
    # Details of <Package> section in pspec.xml
    url(r'^(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/(?P<sourceName>[^/]+)/(?P<packageName>[^/]+)/$', 'noan.repository.views.view_package_detail', name="repo-package-info"),
    # search
    url(r'^search/$', 'noan.repository.views.search', name="search"),
    # orphan
    url(r'^orphan/$', 'noan.repository.views.orphan', name="orphan"),
    # List of orphan packages
    url(r'^orphan/(?P<distName>[^/]+)/(?P<distRelease>[^/]+)/list/all/$', 'noan.repository.views.list_orphan_packages', name="list-orphan"),
)
