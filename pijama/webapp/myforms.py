#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.util import ErrorList

class KeyWordForm(forms.Form):

    keyword = forms.CharField(max_length=25, label="Anahtar Kelime", error_messages={'required': 'Lütfen bir kelime giriniz'})
    searchinbinpackages = forms.BooleanField(label="İkilik Paketlerde Ara", error_messages={'required': False})
    searchinsourcepackages = forms.BooleanField(label="Kaynak Paketlerde Ara", error_messages={'required': False})
    searchinpatches = forms.BooleanField(label="Yamalarda Ara", error_messages={'required': False})
    searchinfiles = forms.BooleanField(label="Paketin Dosyalarında Ara", error_messages={'required': False})

    def clean(self):
        cleaned_data = self.cleaned_data
        searchinbinpackages = cleaned_data.get("searchinbinpackages")
        searchinsourcepackages = cleaned_data.get("searchinsourcepackages")
        searchinpatches = cleaned_data.get("searchinpatches")
        searchinfiles = cleaned_data.get("searchinfiles")

        li = [searchinbinpackages, searchinsourcepackages, searchinpatches, searchinfiles]
        result = filter(lambda x: x, li)

        if len(result) == 0:
            msg=u'Bir eylem seçiniz!'
            self._errors["keyword"]=ErrorList([msg])
            try:
                del cleaned_data["keyword"]
            except:
                pass

        try:
            del self._errors["searchinbinpackages"]
        except:
            pass
        try:
            del self._errors["searchinsourcepackages"]
        except:
            pass
        try:
            del self._errors["searchinpatches"]
        except:
            pass
        try:
            del self._errors["searchinfiles"]
        except:
            pass

        return cleaned_data
