from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from noan.middleware.threadlocals import get_current_lang
import datetime

TEST_TIMEOUT = 24 # hours
TEST_RESULTS = (
    ('yes', _('Yes')),
    ('no', _('No')),
)

RELEASE_RESOLUTIONS = (
    ('pending', _('Pending')),
    ('released', _('Released')),
    ('reverted', _('Reverted')),
)


class Distribution(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))
    release = models.CharField(max_length=64, verbose_name=_('release'))

    def __unicode__(self):
        return u'%s %s' % (self.name, self.release)

    def get_url(self):
        return '/repository/%s/%s' % (self.name, self.release)

    class Meta:
        verbose_name = _('distribution')
        verbose_name_plural = _('distributions')
        ordering = ['name', 'release']
        unique_together = ('name', 'release')


class Source(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))
    distribution = models.ForeignKey(Distribution, verbose_name=_('distribution'))
    maintained_by = models.ForeignKey(User, verbose_name=_('maintained by'))

    def __unicode__(self):
        return self.name

    def get_url(self):
        return '%s/%s' % (self.distribution.get_url(), self.name)

    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')
        ordering = ['name']
        unique_together = ('name', 'distribution')


class Package(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))
    source = models.ForeignKey(Source, verbose_name=_('source'))

    def __unicode__(self):
        return _('%(package)s (source: %(source)s)') % {'package': self.name, 'source': self.source}

    def get_url(self):
        return '%s/%s' % (self.source.get_url(), self.name)

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        ordering = ['name']
        unique_together = ('name', 'source')


class Update(models.Model):
    no = models.IntegerField(verbose_name=_('release no'))
    source = models.ForeignKey(Source, verbose_name=_('source'))
    version_no = models.CharField(max_length=16, verbose_name=_('version no'))
    updated_by = models.ForeignKey(User, verbose_name=_('updated by'))
    updated_on = models.DateField(verbose_name=_('updated on'))
    comment = models.TextField(max_length=512, verbose_name=_('comment'))

    def __unicode__(self):
        return _('%(version)s-%(release)s by %(updater)s on %(date)s') % {'version': self.version_no, 'release': self.no, 'updater': self.updated_by, 'date': self.updated_on}

    class Meta:
        verbose_name = _('update')
        verbose_name_plural = _('updates')
        ordering = ['-no']
        unique_together = ('no', 'source')


class Binary(models.Model):
    no = models.IntegerField(verbose_name=_('build no'))
    package = models.ForeignKey(Package, verbose_name=_('package'))
    update = models.ForeignKey(Update, verbose_name=_('update'))
    resolution = models.CharField(max_length=32, choices=RELEASE_RESOLUTIONS, verbose_name=_('resolution'))

    def __unicode__(self):
        return u'%s-%s-%s-%s' % (self.package.name, self.update.version_no, self.update.no, self.no)

    def get_url(self):
        return '%s/%s' % (self.package.get_url(), self.no)

    def get_filename(self):
        return '%s.pisi' % unicode(self)

    def get_difference(self):
        binaries = self.package.binary_set.filter(no__lt=self.no).order_by('-no')
        if len(binaries) == 0:
            update_last = 0
        else:
            update_last = binaries[0].update.no
        return self.package.source.update_set.filter(no__lte=self.update.no, no__gt=update_last)

    class Meta:
        verbose_name = _('binary')
        verbose_name_plural = _('binaries')
        ordering = ['package__name', '-no']
        unique_together = ('no', 'package')
