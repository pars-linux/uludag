from django.conf.urls.defaults import *

urlpatterns = patterns('chiq.flatpages.views', (r'^(?P<url>.*)$', 'flatpage'),)
