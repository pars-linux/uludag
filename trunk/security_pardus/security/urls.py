from django.conf.urls.defaults import *
from security.settings import WEB_ROOT

urlpatterns = patterns('',
    (r'^mudur/', include('django.contrib.admin.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/media' % WEB_ROOT, 'show_indexes': True}),
    (r'^(?P<lang_code>\w{2,})/(?P<plsa_id>\d{4}-\d{1,})/text/$', 'security.advisory.views.advisory_text'),
    (r'^(?P<lang_code>\w{2,})/(?P<plsa_id>\d{4}-\d{1,})/$', 'security.advisory.views.advisory_details'),
    (r'^(?P<lang_code>\w{2,})/(?P<year>\d{4})/$', 'security.advisory.views.archive_year'),
    (r'^(?P<lang_code>\w{2,})/$', 'security.advisory.views.index_language'),
    (r'^$', 'security.advisory.views.index'),
    (r'^(?P<lang_code>\w{2,})/rss/$', 'security.advisory.views.feed'),
)
