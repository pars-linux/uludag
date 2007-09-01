from django.conf.urls.defaults import *

import os

templatedir = os.path.join(os.getcwd(),"templates/")


urlpatterns = patterns('',
    # Example:
    # (r'^pijama/', include('pijama.apps.foo.urls.foo')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
	
	(r'^main/media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': templatedir, 'show_indexes': True}),
	(r'^main/(?P<reponame>2007)/$', 'pijama.views.showmainpage'),
	(r'^main/(?P<reponame>contrib)/$', 'pijama.views.showmainpage'),
	(r'^main/(?P<reponame>devel)/$', 'pijama.views.showmainpage'),
	(r'^main/(?P<reponame>.*)/sources/$', 'pijama.views.showsourcepkgs'),
	(r'^main/(?P<reponame>.*)/binaries/$', 'pijama.views.showbinarypkgs'),
	(r'^main/(?P<reponame>.*)/packagers/$', 'pijama.views.showpackagers', {'flag': False}),
	(r'^main/(?P<reponame>.*)/packagers_by_name/$', 'pijama.views.showpackagers', {'flag': True}),
	(r'^main/(?P<reponame>.*)/packagers/(?P<packagername>.*)/$', 'pijama.views.showpackagerdetails'),
	(r'^main/(?P<reponame>.*)/sources/(?P<packagename>.*)/$', 'pijama.views.showpkgdetails'),
	(r'^main/(?P<reponame>.*)/binaries/(?P<packagename>.*)/$', 'pijama.views.showbinarydetails'),
	(r'^main/(?P<reponame>.*)/search/$', 'pijama.views.search'),
	(r'^main/(?P<reponame>.*)/search_result/$', 'pijama.views.searchresult'),
)
