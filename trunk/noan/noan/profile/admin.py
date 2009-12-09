#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from noan.profile.models import *

class ProfileAdmin(admin.ModelAdmin):
    verbose_name = "User Profile"
    verbose_name_plural = "User Profiles"
    search_fields = ['user']

admin.site.register(Profile, ProfileAdmin)
