#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.contrib import admin

from chiq.st.models import Tag, OtherFile

class StSimpleAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    ordering = ['-name']
    search_fields = ['name']

class FileAdmin(admin.ModelAdmin):
    list_display = ('file', 'desc')
    ordering = ['-id']
    search_fields = ['file', 'desc']

admin.site.register(Tag, StSimpleAdmin)
admin.site.register(OtherFile, FileAdmin)
