from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^pijama/', include('pijama.apps.foo.urls.foo')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
	
	(r'^main/$', 'pijama.views.showmainpage'),
)
