#!/usr/bin/python
# -*- coding: utf-8 -*-

# DJANGO RELATED IMPORTS
# FIXME: Remove this line when we make a decision about home page of /user/
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# we use generic view for listing as it handles pagination easily. so we don't duplicate the code.
from django.views.generic.list_detail import object_list

# APP RELATED IMPORTS
from noan.repository.models import Binary
from noan.wrappers import render_response
from noan.profile.forms import ProfileEditForm, PasswordChangeForm

from noan.settings import USERS_PER_PAGE

# Main page of profile page
def main(request):
    #FIXME: Make a decision about how to deal with home-page
    return HttpResponse("Main Page")

#  Profile page where developers can change their informations(/user/profile)
@login_required
def user_profile(request):
    # form is posted
    if request.method == 'POST':
        form = ProfileEditForm(request.POST)
        if form.is_valid():
            u = request.user
            u.first_name = form.cleaned_data["firstname"]
            u.last_name = form.cleaned_data["lastname"]
            u.save()

            return render_response(request, "profile/user-profile-edit.html", {"profile_updated": True})
        else:
            return render_response(request, "profile/user-profile-edit.html", {"form": form})

    else:
        unbound_form = ProfileEditForm({"firstname": request.user.first_name, "lastname": request.user.last_name})
        return render_response(request, "profile/user-profile-edit.html", {"form": unbound_form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        form.setUser(request.user)
        if form.is_valid():
            request.user.set_password(form.cleaned_data["new_pass"])
            request.user.save()
            return render_response(request, "profile/password-change.html", {"form": form, "password_updated": True})
        else:
            return render_response(request, "profile/password-change.html", {"form": form})
    else:
        form = PasswordChangeForm()
        return render_response(request, "profile/password-change.html", {"form": form})

# List of the registered developers, (/user/list)
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
