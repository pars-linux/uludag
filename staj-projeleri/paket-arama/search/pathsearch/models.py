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

class Pardus2007(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'pardus_2007'
        ordering = ['package', 'path']

    
    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)
    
class Pardus2008(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'pardus_2008'
        ordering = ['package', 'path']

    
    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)

class Contrib2008(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)

    class Meta:
        db_table = 'contrib_2008'
        ordering = ['package', 'path']

    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)
