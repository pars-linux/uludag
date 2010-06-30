#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms

from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList

from noan.repository.models import Distribution

def fill_dist_name():
    dist_li = []
    dists = Distribution.objects.all().values('name')
    for dist in dists:
        if dist['name'] not in dist_li: dist_li.append(dist['name'])
    name_li = map(lambda x: (x,x), dist_li)

    return name_li

def fill_dist_release():
    dists = Distribution.objects.all().distinct()
    release_li = []
    for distribution in dists:
        release_li.append((distribution.release,  distribution.release))

    return release_li

class SearchForm(forms.Form):

    keyword = forms.CharField(max_length=25, label=_('Keyword'), help_text=_('The keyword entered will be search in package names, summaries and descriptions by default'), required=True)
    exact = forms.BooleanField(label=_('Exact'), help_text=_('Search in exact names in packages'), required=False)
    name = forms.BooleanField(label=_('Name'), help_text=_('Search in package names'), initial=True, required=False)
    summary = forms.BooleanField(label=_('Summary'), help_text=_('Search in package summaries'), initial=True, required=False)
    description = forms.BooleanField(label=_('Description'), help_text=_('Seacrh in package descriptions'), initial=True, required=False)
    #source = forms.BooleanField(label=_('Source Packages'), help_text=_('Search in source packages'), required=False)
    #binary = forms.BooleanField(label=_('Binary Packages'), help_text=_('Search in binary packages'), initial=True, required=False)
    in_package = forms.TypedChoiceField(coerce=bool, 
                                        choices=(('Source', 'Source'), ('Binary', 'Binary')), 
                                        widget=forms.RadioSelect,
                                        help_text=_('Search in source/binary packages'),
                                        label=_('Source/Binary Packages'),
                                        initial='Binary'
                                    )

    dist_name = forms.ChoiceField(label=_('Distribution'), help_text=_('Choose the distribution'), choices=fill_dist_name())
    dist_release = forms.ChoiceField(label=_('Release'), help_text=_('Choose the release'), choices=fill_dist_release())

    def clean(self):
        cleaned_data = self.cleaned_data
        data = cleaned_data.get("keyword", '')

        if not data:
            msg = _('Keyword is required')
            self._errors["keyword"] = ErrorList([msg])
            if cleaned_data.has_key("keyword"): del cleaned_data["keyword"]

        exact = cleaned_data.get('exact', '')
        if exact:
            name = cleaned_data.get('name', '')
            if not name:
                msg = _('For exact search, select name option')
                self._errors["name"] = ErrorList([msg])
                if cleaned_data.has_key("name"): del cleaned_data["name"]

        return cleaned_data
