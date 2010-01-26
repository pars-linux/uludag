#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """Profile model for each User. It will allow us to collect and manage more data about users"""
    user = models.ForeignKey(User, unique=True)
    # only admins are able to edit title
    title = models.CharField("Title", max_length=32, blank=True, help_text="Eg: Developer, Maintainer")

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return '/noan/user/detail/%s' % self.user.username
