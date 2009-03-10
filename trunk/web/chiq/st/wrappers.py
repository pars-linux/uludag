#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.core.mail import *

# wrapper to use context_instance automatically

def render_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)
