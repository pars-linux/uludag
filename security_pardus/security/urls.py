from django.conf.urls.defaults import *
from security.plsa.models import PLSA
from security.settings import WEB_ROOT

urlpatterns = patterns('',
    (r'^mudur/', include('django.contrib.admin.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/media' % WEB_ROOT, 'show_indexes': True}),

    (r'^(?P<lang>\w{2,})/(?P<plsa_id>\d{4}-\d{1,})/text/$', 'security.plsa.views.details_text'),
    (r'^(?P<lang>\w{2,})/(?P<plsa_id>\d{4}-\d{1,})/$', 'security.plsa.views.details'),

    (r'^(?P<lang>\w{2,})/(?P<year>\d{4})/$', 'security.plsa.views.list_year'),
    (r'^(?P<lang>\w{2,})/$', 'security.plsa.views.page_lang'),

    (r'^(?P<lang>\w{2,})/rss/$', 'security.plsa.views.feed'),

    (r'^$', 'security.plsa.views.page_index'),
)
