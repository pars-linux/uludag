#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.conf.urls.defaults import *

from chiq.settings import WEB_URL, DOCUMENT_ROOT, TAG_PER_PAGE
from chiq.st.models import Tag
from django.contrib import admin

tag_dict = {
            'queryset': Tag.objects.all().order_by('name'),
            'template_name': 'tag/tag_main.html',
            'paginate_by': TAG_PER_PAGE,
            'template_object_name': 'tag'
           }

admin.autodiscover()
urlpatterns = patterns('',

    (r'^robots.txt$', 'chiq.st.views.robots'),

    #Tags
    (r'^etiket/$', 'django.views.generic.list_detail.object_list', dict(tag_dict)),
    (r'^etiket/(?P<tag>.*)/$', 'chiq.st.views.tag_detail'),

    #Webalizer
    url(r'^admin/webalizer/', include('webalizer.urls')),

    #Django
    (r'^$', 'chiq.st.views.home'),
    (r'^admin/upload/image/tinymce/$', 'chiq.upload.views.image_upload'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root),
    (r'^media/(.*)$', 'django.views.static.serve', {'document_root': '%s/media' % DOCUMENT_ROOT, 'show_indexes': True}),
)
