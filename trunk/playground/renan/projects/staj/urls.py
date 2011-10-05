from django.conf.urls.defaults import *
from staj.form.views import *
from django.conf import settings

path = "/home/pars/workspace/staj"

urlpatterns = patterns('',
        #(r'^staj/$', intern_form),
        (r'^staj/$', end),
        (r'^$', end),

        (r'^internshop/$', scoring_form),

        #(r'^kayit/$', thanks),

        #(r'^mentor/$', mentor_form),
        #(r'^mentor/done$', mentor_done),
        (r'^[A-Za-z/]*dosyalar/cv/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '%s/uploads/cv' % path, 'show_indexes': False}),
        (r'^[A-Za-z/]*dosyalar/kod/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '%s/uploads/code/' % path, 'show_indexes': False}),

        (r'^[A-Za-z/]*js/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '%s/templates/media_files/js/' % path, 'show_indexes': False}),
        (r'^[A-Za-z/]*img/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '%s/templates/media_files/img/' % path, 'show_indexes': False}),
        (r'^[A-Za-z/]*css/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '%s/templates/media_files/css/' % path, 'show_indexes': False}),
        #(r'^projeler/$', projeler),
        url(r'^captcha/', include('captcha.urls')),
)
