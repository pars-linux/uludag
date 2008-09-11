from django.db import models

class Entry(models.Model):
    package = models.CharField(max_length=60)
    path    = models.CharField(max_length=200)
    
    class Meta:
        db_table = 'files'
    
    def __unicode__(self):
        return '%s - %s' % (self.package, self.path)
    