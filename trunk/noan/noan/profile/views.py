#!/usr/bin/python
# -*- coding: utf-8 -*-

##########################
# Django related imports #
##########################

# FIXME: Remove this line when we make a decision about home page of /user/
from django.http import HttpResponse
from django.contrib.auth.models import User

# we use generic view for listing as it handles pagination easily. so we don't duplicate the code.
from django.views.generic.list_detail import object_list

###############################
# Application related imports #
###############################

from noan.repository.models import Binary
from noan.wrappers import render_response

from noan.settings import USERS_PER_PAGE

# Main page of profile page
def main(request):
    #FIXME: Make a decision about how to deal with home-page
    return HttpResponse("Main Page")

def get_user_list(request):
    # FIXME: Developers and users/testers should be different
    # We should mark developers. Also, fix non-sense template variables such as in this file "developers"

    users = User.objects.all().order_by('first_name', 'last_name')

    # - generate dict to use in object_list
    # - django appends _list suffix to template_object_name, see: http://docs.djangoproject.com/en/1.0/ref/generic-views/
    object_dict = {
            'queryset': users,
            'paginate_by': USERS_PER_PAGE,
            'template_name': 'profile/user-list.html',
            'template_object_name': 'user'
            }

    return object_list(request, **object_dict)

def view_user_detail(request, userName):
    # FIXME: Developers and users/testers should be different

    developer = User.objects.get(username=userName)
    pending = Binary.objects.filter(resolution='pending', update__updated_by=developer)

    context = {
        'developer': developer,
        'pending': pending,
    }

    return render_response(request, 'profile/user-detail.html', context)
