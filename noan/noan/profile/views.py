#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.http import HttpResponse

# Main page of profile page
def main(request):
    return HttpResponse("Main Page")

# Page for getting user detail
def get_user_info(request, userName):
    return HttpResponse("Page for user: %s" % userName)
