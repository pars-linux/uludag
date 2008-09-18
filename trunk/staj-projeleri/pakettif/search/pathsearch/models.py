from django.db import models

class Entry(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'files'
        ordering = ['package', 'path']
 
    
    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)
    
    
class Entry2007(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'files2007'
        ordering = ['package', 'path']

    
    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)
    
class Entry2008(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'files2008'
        ordering = ['package', 'path']

    
    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)