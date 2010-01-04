#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

def render_response(req, *args, **kwargs):
    """
        Wrapper function that automatically adds "context_instance" to render_to_response
    """

    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)
