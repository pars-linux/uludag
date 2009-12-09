#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

class ProfileEditForm(forms.Form):
    firstname = forms.CharField(label='Adı', max_length=30)
    lastname = forms.CharField(label='Soyadı', max_length=30)
