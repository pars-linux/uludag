#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from chiq.flatpages.models import FlatPage
from chiq.st.wrappers import render_response

def robots(request):
    return render_response(request, 'robots.txt')

def home(request):
    pages = FlatPage.objects.all()
    return render_response(request, 'home.html', locals())

def tag_detail(request, tag):
    try:
        flatpages = FlatPage.objects.filter(tags__name__exact=tag)

    except Tag.DoesNotExist:
        raise Http404
    return render_response(request, 'tag/tag_detail.html', locals())
