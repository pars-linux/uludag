from django.conf.urls.defaults import *
from search.settings import DOCUMENT_ROOT


urlpatterns = patterns('',
    (r'^$', 'search.pathsearch.views.index'),
    (r'^search/', include('search.pathsearch.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),

)
