from django.conf.urls.defaults import *
from pakettif.settings import DOCUMENT_ROOT


urlpatterns = patterns('',
    (r'^$', 'pakettif.pathsearch.views.index'),
    (r'^search/', include('pakettif.pathsearch.urls')),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),

)
