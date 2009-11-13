#!/usr/bin/python
# -*- coding: utf-8 -*-

##########################
# Django related imports #
##########################

# FIXME: Remove this line when we make a decision about home page of /user/
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
#FIXME: Use {% paginate %} template tag for paginating stuff, in that way we just duplicate the code!
from django.core.paginator import Paginator, InvalidPage, EmptyPage
#FIXME: Write a wrapper for RequestContext, set a name "render_response" for it
from django.template import RequestContext

###############################
# Application related imports #
###############################

from noan.repository.models import Binary

# Main page of profile page
def main(request):
    #FIXME: Make a decision about how to deal with home-page
    return HttpResponse("Main Page")

def get_user_list(request):
    # FIXME: Developers and users/testers should be different
    # We should mark developers. Also, fix non-sense template variables such as in this file "developers"

    users = User.objects.all().order_by('first_name', 'last_name')

    # Pagination
    paginator = Paginator(users, 25)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        users = paginator.page(page)
    except (EmptyPage, InvalidPage):
        users = paginator.page(paginator.num_pages)

    context = {
        'developers': users,
    }
    return render_to_response('profile/user-list.html', context, context_instance=RequestContext(request))


def view_user_detail(request, userName):
    # FIXME: Developers and users/testers should be different

    developer = User.objects.get(username=userName)
    pending = Binary.objects.filter(resolution='pending', update__updated_by=developer)

    context = {
        'developer': developer,
        'pending': pending,
    }

    return render_to_response('profile/user-detail.html', context, context_instance=RequestContext(request))
