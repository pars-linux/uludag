from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    (r'^ciftci/', include('web.ciftci.urls')),
    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
