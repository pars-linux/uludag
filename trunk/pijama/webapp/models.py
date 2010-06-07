from django.db import models

# Create your models here.

class SourcePktTbl(models.Model):
    pktname=models.CharField(max_length=50, primary_key=True, unique=True)
    added_date=models.DateField()
    last_change=models.DateField()

    summary=models.TextField()
    version=models.CharField(max_length=25)
    license=models.CharField(max_length=50)
    homepage=models.URLField()
    

    def __unicode__(self):
        return u'%s' % (self.pktname)

    class Meta:
        db_table="SourcePktTbl"
        ordering=["pktname"]
        get_latest_by="added_date"

class SourcePktBuildDebsTbl(models.Model):
    pktname=models.CharField(max_length=50)
    sourcepkt_name=models.ForeignKey(SourcePktTbl)

    def __unicode__(self):
        return u'%s' % (self.pktname)

    class Meta:
        db_table="SourcePktBuildDebsTbl"
        ordering=["pktname"]


class BinaryPktTbl(models.Model):
    sourcepkt_name=models.CharField(max_length=50)
    srcname=models.ForeignKey(SourcePktTbl)
    binarypkt_name=models.CharField(max_length=50)
    
    summary=models.TextField()
    version=models.CharField(max_length=25)
    
    def __unicode__(self):
        return u'%s' % (self.binarypkt_name)

    class Meta:
        db_table="BinaryPktTbl"
        ordering=["binarypkt_name"]

class PackagerTbl(models.Model):
    pktname=models.CharField(max_length=50)
    name=models.CharField(max_length=100)
    source=models.OneToOneField(SourcePktTbl)
    email=models.EmailField()

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        db_table="PackagerTbl"
        ordering=["name"]

class PatchPktTbl(models.Model):
    pktname=models.CharField(max_length=50)
    patchname=models.TextField()
    pname=models.ForeignKey(SourcePktTbl)
    patch_level=models.SmallIntegerField(null=True)

    def __unicode__(self):
        return u'%s' % (self.patchname)

    class Meta:
        db_table="PatchPktTbl"
        ordering=["patchname"]

class HistoryPktTbl(models.Model):
    pktname=models.CharField(max_length=50)
    update=models.IntegerField()
    update_date=models.DateField()
    update_version=models.CharField(max_length=100)
    comment=models.TextField()
    updater=models.CharField(max_length=100)
    history=models.ForeignKey(SourcePktTbl)

    def __unicode__(self):
        return u'%s %s' % (self.updater, self.update_date)

    class Meta:
        db_table="HistoryPktTbl"
        ordering=["-update_date"]
