from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^ciftci/', include('web.ciftci.urls')),
)
