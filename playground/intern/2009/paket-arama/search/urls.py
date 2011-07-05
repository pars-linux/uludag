from django.conf.urls.defaults import *
from search.settings import DOCUMENT_ROOT


urlpatterns = patterns('',
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
    #(r'^search/', include('search.pathsearch.urls')),
    (r'^', include('search.pathsearch.urls')),

)


