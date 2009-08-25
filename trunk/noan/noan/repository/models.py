from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from noan.middleware.threadlocals import get_current_lang
import datetime
from pisi.version import Version as Pisi_Version

TEST_RESULTS = (
    ('yes', _('Can go to stable')),
    ('no', _('Package has problems')),
    ('unknown', _('Tests are incomplete')),
)

RELEASE_RESOLUTIONS = (
    ('pending', _('Pending')),
    ('released', _('Released')),
    ('reverted', _('Reverted')),
    ('removed', _('Removed')),
)


class Distribution(models.Model):
    """
        Database model for distributions.

        name: Name of distribution (Pardus, Pardus x64, ...)
        release: Distribution release (2008, 2009, ...)
    """
    name = models.CharField(max_length=64, verbose_name=_('name'))
    release = models.CharField(max_length=64, verbose_name=_('release'))

    def __unicode__(self):
        return u'%s %s' % (self.name, self.release)

    def get_url(self):
        return '/repository/%s-%s' % (self.name, self.release)

    class Meta:
        verbose_name = _('distribution')
        verbose_name_plural = _('distributions')
        ordering = ['name', 'release']
        unique_together = ('name', 'release')


class Source(models.Model):
    """
        Database model for sources in repository.

        name: Name of the source
        distribution: Distribution that contains the source
        maintained_by: Source maintainer
    """
    name = models.CharField(max_length=64, verbose_name=_('name'))
    distribution = models.ForeignKey(Distribution, verbose_name=_('distribution'))
    maintained_by = models.ForeignKey(User, verbose_name=_('maintained by'))

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.distribution)

    def get_url(self):
        return '%s/%s' % (self.distribution.get_url(), self.name)

    class Meta:
        verbose_name = _('source')
        verbose_name_plural = _('sources')
        ordering = ['name']
        unique_together = ('name', 'distribution')


class Package(models.Model):
    """
        Database model for package in repository.

        name: Name of the package
        source: Source that contains the package
    """
    name = models.CharField(max_length=64, verbose_name=_('name'))
    source = models.ForeignKey(Source, verbose_name=_('source'))

    def __unicode__(self):
        return _('%(package)s (source: %(source)s, distro: %(distro)s)') % {'package': self.name, 'source': self.source.name, 'distro': self.source.distribution}

    def get_url(self):
        return '%s/%s' % (self.source.get_url(), self.name)

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        ordering = ['name']
        unique_together = ('name', 'source')


class BuildDependency(models.Model):
    """
        Database model for build dependencies of a source.

        name: Package name of the dependency
        version*: Version range
        release*: Release range
        source: Dependent source
    """
    name = models.CharField(max_length=64, verbose_name=_('name'))
    version = models.CharField(max_length=32, verbose_name=_('version'), default='', blank=True)
    version_from = models.CharField(max_length=32, verbose_name=_('version from'), default='', blank=True)
    version_to = models.CharField(max_length=32, verbose_name=_('version to'), default='', blank=True)
    release = models.IntegerField(verbose_name=_('release'), default=0, blank=True)
    release_from = models.IntegerField(verbose_name=_('release from'), default=0, blank=True)
    release_to = models.IntegerField(verbose_name=_('release to'), default=0, blank=True)
    source = models.ForeignKey(Source, verbose_name=_('dependent source'))

    def __unicode__(self):
        if self.release != 0:
            return u'%s == r%s' % (self.name, self.release)
        if self.version != '':
            return u'%s == %s' % (self.name, self.version)
        dep = []
        if self.version_from != '':
            dep.append('>= %s' % self.version_from)
        if self.version_to != '':
            dep.append('<= %s' % self.version_to)
        if self.release_from != 0:
            dep.append('>= r%s' % self.release_from)
        if self.release_to != 0:
            dep.append('<= r%s' % self.release_to)
        return u'%s %s' % (self.name, ' '.join(dep))

    class Meta:
        verbose_name = _('build dependency')
        verbose_name_plural = _('build depencencies')
        ordering = ['name']


class RuntimeDependency(models.Model):
    """
        Database model for runtime depencencies of a package.

        name: Package name of the depencency
        version*: Version range
        release*: Release range
        package: Dependent package
    """
    name = models.CharField(max_length=64, verbose_name=_('name'))
    version = models.CharField(max_length=32, verbose_name=_('version'), default='', blank=True)
    version_from = models.CharField(max_length=32, verbose_name=_('version from'), default='', blank=True)
    version_to = models.CharField(max_length=32, verbose_name=_('version to'), default='', blank=True)
    release = models.IntegerField(verbose_name=_('release'), default=0, blank=True)
    release_from = models.IntegerField(verbose_name=_('release from'), default=0, blank=True)
    release_to = models.IntegerField(verbose_name=_('release to'), default=0, blank=True)
    package = models.ForeignKey(Package, verbose_name=_('dependent package'))

    def __unicode__(self):
        if self.release != 0:
            return u'%s == r%s' % (self.name, self.release)
        if self.version != '':
            return u'%s == %s' % (self.name, self.version)
        dep = []
        if self.version_from != '':
            dep.append('>= %s' % self.version_from)
        if self.version_to != '':
            dep.append('<= %s' % self.version_to)
        if self.release_from != 0:
            dep.append('>= r%s' % self.release_from)
        if self.release_to != 0:
            dep.append('<= r%s' % self.release_to)
        return u'%s %s' % (self.name, ' '.join(dep))

    class Meta:
        verbose_name = _('runtime dependency')
        verbose_name_plural = _('runtime depencencies')
        ordering = ['name']


class Update(models.Model):
    """
        Database model for updates of a source.

        no: Release number
        source: Source
        version_no: Version string
        updated_by: Updater
        updated_on: Update date
        comment: Updater's comment
    """
    no = models.IntegerField(verbose_name=_('release no'))
    source = models.ForeignKey(Source, verbose_name=_('source'))
    version_no = models.CharField(max_length=32, verbose_name=_('version no'))
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
    """
        Database model for binary package.

        no: Build no
        package: Package
        update: Update
        resolution: 'pending', 'released' or 'reverted'. Import scripts set this value.
    """
    no = models.IntegerField(verbose_name=_('build no'))
    package = models.ForeignKey(Package, verbose_name=_('package'))
    update = models.ForeignKey(Update, verbose_name=_('update'))
    resolution = models.CharField(max_length=32, choices=RELEASE_RESOLUTIONS, verbose_name=_('resolution'))
    linked_binary = models.ManyToManyField('Binary')

    def __unicode__(self):
        return u'%s-%s-%s-%s' % (self.package.name, self.update.version_no, self.update.no, self.no)

    def get_url(self):
        return '%s/%s' % (self.package.get_url(), self.no)

    def get_filename(self):
        return '%s.pisi' % unicode(self)

    def get_difference(self):
        """
            Find next to last binary and generates a list of update difference between these two binaries.

            This is an expensive method. Don't use this in pacakge lists.
        """
        binaries = self.package.binary_set.filter(no__lt=self.no).order_by('-no')
        if len(binaries) == 0:
            update_last = 0
        else:
            update_last = binaries[0].update.no
        return self.package.source.update_set.filter(no__lte=self.update.no, no__gt=update_last)

    def get_pending_dependencies(self):
        return self.linked_binary.all()

    def get_result(self):
        if self.testresult_set.count() == 0:
            return "unknown"
        for dep in self.get_pending_dependencies():
            if dep.testresult_set.count() == 0:
                return "unknown"
            if dep.get_result() == "no":
                return "no"
        for result in self.testresult_set.all():
            if result.result == "no":
                return "no"
        for result in self.testresult_set.all():
            if result.result == "yes":
                return "yes"
        return "unknown"

    def get_result_str(self):
        result = self.get_result()
        for name, label in TEST_RESULTS:
            if name == result:
                return label
        return result

    class Meta:
        verbose_name = _('binary')
        verbose_name_plural = _('binaries')
        ordering = ['package__name', '-no']
        unique_together = ('no', 'package')


class TestResult(models.Model):
    """
        Database model for test results.

        binary: Binary
        created_by: Tester
        created_on: Test date
        result: Test result
        comment: Tester's comment
    """
    binary = models.ForeignKey(Binary, verbose_name=_('binary'))
    created_by = models.ForeignKey(User, verbose_name=_('created by'))
    created_on = models.DateField(verbose_name=_('created on'), auto_now=True)
    result = models.CharField(max_length=32, choices=TEST_RESULTS, verbose_name=_('result'))
    comment = models.CharField(max_length=256, verbose_name=_('comment'), default='')

    def __unicode__(self):
        return _('%(result)s (binary: %(binary)s source: %(source)s, distro: %(distro)s)') % {'result': self.result, 'binary': self.binary, 'source': self.binary.package.source.name, 'distro': self.binary.package.source.distribution}

    class Meta:
        ordering = ['-created_on']
        verbose_name = _('test result')
        verbose_name_plural = _('test results')
