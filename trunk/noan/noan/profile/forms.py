#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

class ProfileEditForm(forms.Form):
    firstname = forms.CharField(label='Adı', max_length=30)
    lastname = forms.CharField(label='Soyadı', max_length=30)

class PasswordChangeForm(forms.Form):
    current_pass = forms.CharField(label="Current Password", max_length=32, widget=forms.PasswordInput)
    new_pass = forms.CharField(label="New Password", max_length=32, widget=forms.PasswordInput)
    new_pass_again = forms.CharField(label="New Password Again", widget=forms.PasswordInput)

    def setUser(self, u):
        """ Get current user from view """
        self.user = u

    def clean_current_pass(self):
        field_data = self.cleaned_data['current_pass']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Password can not have blank chars.")

        if len(field_data) > 32:
            raise forms.ValidationError(u"Password can be 32 characters most.")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Password can not be less than 5 chars.")

        u = User.objects.get(username=self.user.username)
        if not u.check_password(field_data):
            raise forms.ValidationError(u"The current password is wrong")

        return field_data


    def clean_new_pass(self):
        field_data = self.cleaned_data['new_pass']

        if len(field_data.split(' ')) != 1:
            raise forms.ValidationError(u"Password can not have blank chars.")

        if len(field_data) > 32:
            raise forms.ValidationError(u"Password can be 32 characters most.")

        if len(field_data) < 5:
            raise forms.ValidationError(u"Password can not be less than 5 chars.")

        return field_data

    def clean_new_pass_again(self):
        field_data = self.cleaned_data['new_pass_again']

        if not self.cleaned_data.has_key('new_pass') or not self.cleaned_data.has_key('current_pass'):
            return
        else:
            new_pass = self.cleaned_data['new_pass']
            current_pass = self.cleaned_data['current_pass']

        if field_data or new_pass or current_pass:

            if len(field_data.split(' ')) != 1:
                raise forms.ValidationError(u"Password can not have blank chars.")

            if len(field_data) > 32:
                raise forms.ValidationError(u"Password can be 32 characters most.")

            if len(field_data) < 5:
                raise forms.ValidationError(u"Password can not be less than 5 chars.")

            if (new_pass or field_data) and new_pass != field_data:
                raise forms.ValidationError(u"Re-typed password do not match.")

            return field_data
        else:
            return ''
