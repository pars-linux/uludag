from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # neden bilmiyorum bunu açınca digerlerni sallamıyo :(
    #(r'^pardus/', 'pardus.web.views.index'),
    (r'^Node/(?P<nice_title>.*)', 'pardus.web.views.detail'),
    #(r'^(?P<page_title>\d+)/results/$', 'pardus.web.views.results'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/rat/django/pardus/web/'}),
    # Uncomment this for admin:
    (r'^admin/', include('django.contrib.admin.urls')),
)
