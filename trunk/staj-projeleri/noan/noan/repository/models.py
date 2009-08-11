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
        return '/repository/%s-%s' % (self.name, self.release)

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
        return u'%s (%s)' % (self.name, self.distribution)

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
        return _('%(package)s (source: %(source)s, distro: %(distro)s)') % {'package': self.name, 'source': self.source.name, 'distro': self.source.distribution}

    def get_url(self):
        return '%s/%s' % (self.source.get_url(), self.name)

    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')
        ordering = ['name']
        unique_together = ('name', 'source')


class BuildDependency(models.Model):
    source = models.ForeignKey(Source, verbose_name=_('dependent'))
    dep_package = models.CharField(max_length=64, verbose_name=_('package'))
    version = models.CharField(max_length=32, verbose_name=_('version'), default='', blank=True)
    version_from = models.CharField(max_length=32, verbose_name=_('version from'), default='', blank=True)
    version_to = models.CharField(max_length=32, verbose_name=_('version to'), default='', blank=True)
    release = models.IntegerField(verbose_name=_('release'), default=0, blank=True)
    release_from = models.IntegerField(verbose_name=_('release from'), default=0, blank=True)
    release_to = models.IntegerField(verbose_name=_('release to'), default=0, blank=True)

    def __unicode__(self):
        if self.release != 0:
            return u'%s == r%s' % (self.dep_package, self.release)
        if self.version != '':
            return u'%s == %s' % (self.dep_package, self.version)
        dep = []
        if self.version_from != '':
            dep.append('>= %s' % self.version_from)
        if self.version_to != '':
            dep.append('<= %s' % self.version_to)
        if self.release_from != 0:
            dep.append('>= r%s' % self.release_from)
        if self.release_to != 0:
            dep.append('<= r%s' % self.release_to)
        return u'%s %s' % (self.dep_package, ' '.join(dep))

    class Meta:
        verbose_name = _('build dependency')
        verbose_name_plural = _('build depencencies')
        ordering = ['dep_package']


class RuntimeDependency(models.Model):
    package = models.ForeignKey(Package, verbose_name=_('dependent'))
    dep_package = models.CharField(max_length=64, verbose_name=_('package'))
    version = models.CharField(max_length=32, verbose_name=_('version'), default='', blank=True)
    version_from = models.CharField(max_length=32, verbose_name=_('version from'), default='', blank=True)
    version_to = models.CharField(max_length=32, verbose_name=_('version to'), default='', blank=True)
    release = models.IntegerField(verbose_name=_('release'), default=0, blank=True)
    release_from = models.IntegerField(verbose_name=_('release from'), default=0, blank=True)
    release_to = models.IntegerField(verbose_name=_('release to'), default=0, blank=True)

    def __unicode__(self):
        if self.release != 0:
            return u'%s == r%s' % (self.dep_package, self.release)
        if self.version != '':
            return u'%s == %s' % (self.dep_package, self.version)
        dep = []
        if self.version_from != '':
            dep.append('>= %s' % self.version_from)
        if self.version_to != '':
            dep.append('<= %s' % self.version_to)
        if self.release_from != 0:
            dep.append('>= r%s' % self.release_from)
        if self.release_to != 0:
            dep.append('<= r%s' % self.release_to)
        return u'%s %s' % (self.dep_package, ' '.join(dep))

    class Meta:
        verbose_name = _('runtime dependency')
        verbose_name_plural = _('runtime depencencies')
        ordering = ['dep_package']


class Update(models.Model):
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


class Task(models.Model):
    package = models.ForeignKey(Package, verbose_name=_('package'))
    description_en = models.CharField(max_length=256, verbose_name=_('description [en]'))

    def __unicode__(self):
        return u'[%s] - %s' % (self.package.name, self.get_description())

    def get_description(self):
        lang = get_current_lang()
        if lang == 'en':
            return self.description_en
        descriptions = self.taskdescription_set.filter(language__code=lang)
        if len(descriptions) > 0:
            return descriptions[0].description
        return self.description_en

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')


class Language(models.Model):
    code = models.CharField(max_length=6, verbose_name=_('code'))
    name = models.CharField(max_length=32, verbose_name=_('name'))

    def __unicode__(self):
        return u'[%s] %s' % (self.code, self.name)

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')


class TaskDescription(models.Model):
    task = models.ForeignKey(Task, verbose_name=_('task'))
    language = models.ForeignKey(Language, verbose_name=_('language'))
    description = models.CharField(max_length=256, verbose_name=_('description'))

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = _('task description')
        verbose_name_plural = _('task descriptions')


class StateOfTest(models.Model):
    binary = models.OneToOneField(Binary, verbose_name=_('binary'))
    maintained_by = models.ForeignKey(User, verbose_name=_('maintained by'))
    update = models.ForeignKey(Update, verbose_name=_('update'), default='',  blank=True)
    #updated_on = models.DateField(verbose_name=_('updated on'),blank=True)
    state = models.CharField(max_length=4, verbose_name=_('state'), default='', blank=True)

    def __unicode__(self):
        return _('%(state)s (%(binary)s source: %(source)s, distro: %(distro)s)') % {'state': self.state, 'binary': self.binary, 'source': self.binary.package.source.name, 'distro': self.binary.package.source.distribution}

    class Meta:
        ordering = ['id']
        #ordering = ['binary__package__name']
        verbose_name = _('state')
        verbose_name_plural = _('states')
#    def GetAck(self):

