#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2009, TÜBİTAK UEKAE
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

from django.db import models

class Tag(models.Model):
    name = models.CharField('Etiket', max_length=32, blank=False, unique=True)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return "/etiket/%s/" % self.name

    class Meta:
        ordering = ['name']
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"

class OtherFile(models.Model):
    desc = models.TextField('Açıklama')
    file = models.FileField(upload_to='dosya/')
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return unicode(self.file)

    class Meta:
        verbose_name = "Dosya"
        verbose_name_plural = "Dosyalar"
