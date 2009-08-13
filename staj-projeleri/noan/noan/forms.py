#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

STATEMENT = (
        ('ack', 'Ack'),
        ('nack', 'Nack'),
        ('', 'Null'),
)


class AckNackForm(forms.Form):
    state = forms.ChoiceField(choices=STATEMENT, required= False)
    comment = forms.CharField(max_length=256, help_text=_('256 characters max.'), required= False)
    binary = forms.CharField(widget = forms.HiddenInput())
    distro = forms.CharField(widget = forms.HiddenInput())

