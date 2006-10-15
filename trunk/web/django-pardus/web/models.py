from django.db import models

LANG_CHOICES = (
    ('TR','Turkce'),
    ('EN','English'),
)

class Pages (models.Model):
    ID = models.AutoField('ID', primary_key=True)
    Lang = models.CharField(maxlength=2,choices=LANG_CHOICES)
    Title = models.CharField(maxlength=250)
    NiceTitle = models.CharField(maxlength=250)
    Content = models.TextField()
    Modules = models.CharField(maxlength=200,blank=True)

    def __str__(self):
        return self.Title
    class Admin:
        list_display = ('Title','NiceTitle','Lang','Modules')
        search_fields = ['Title','NiceTitle']
        #list_filter = ['Lang']

class News(models.Model):   
    ID = models.AutoField('ID',primary_key=True)
    Lang = models.CharField(maxlength=2,choices=LANG_CHOICES) 
    Title = models.CharField(maxlength=250)
    Content = models.TextField()

    def __str__(self):
        return self.Title

    class Admin:
        list_display = ('Title','Content','Lang')
        search_fields = ['Title','Content']
        list_filter = ['Lang']

