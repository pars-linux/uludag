# -*- coding: utf-8 -*-
from django.db import models

class Repo(models.Model):
    repo  = models.CharField(max_length=30)
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'packages'
        ordering = ['repo', 'package', 'path']

    
    def __unicode__(self):
        return '%s %s - %s' % (self.package, self.path)