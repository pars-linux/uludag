from django.db import models
from django.core import validators
from security.advisory.utils import *

# i18n
from django.utils.translation import gettext_lazy
_ = lambda x: unicode(gettext_lazy(x))

class Language(models.Model):
    code = models.CharField(_("Code"), maxlength=5)
    name = models.CharField(_("Language"), maxlength=20)

    def __str__(self):
        return self.name

    class Admin:
        pass

    class Meta:
        db_table = "plsa_language"
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

ADVISORY_TYPES = (
    ("Local", _("Local")),
    ("Remote", _("Remote")),
)

def isValidPackageList(field_data, all_data):
    try:
        for package in field_data.split("\n"):
            if package.strip():
                name, no, year = package.split(" ")
    except ValueError:
        raise validators.ValidationError(_("Package name, version and distro version must be seperated with a whitespace."))

def isValidAdvisoryID(field_data, all_data):
    import re
    if not re.match("[0-9]{4}-[0-9]+", field_data):
        raise validators.ValidationError(_("Advisory ID must be in YEAR-NO format."))
    #if "language" in all_data and Advisory.objects.filter(language=all_data["language"], plsa_id=field_data):
    #    raise validators.ValidationError(_("Advisory ID already exists for that language."))

class Advisory(models.Model):
    publish = models.BooleanField(_("Publish"))
    release_date = models.DateField(_("Last Update"), auto_now=True)
    language = models.ForeignKey("Language", verbose_name=_("Language"))
    plsa_id = models.CharField(_("PLSA ID"), validator_list=[isValidAdvisoryID], maxlength=10, help_text=_("YEAR-NO"))
    type = models.CharField(_("Type"), maxlength=10, choices=ADVISORY_TYPES)
    severity = models.IntegerField(_("Severity"), default=1)
    title = models.CharField(_("Title"), maxlength=120)
    summary = models.TextField(_("Summary"))
    description = models.TextField(_("Description"))
    packages = models.TextField(_("Packages"), validator_list=[isValidPackageList], help_text=_("one package per row (put a whitespace between package name, version and distro version)"))
    references = models.TextField(_("References"), help_text=_("one link per row"))
    fixed = models.BooleanField(_("Ready to publish"))

    def __str__(self):
        return "[PLSA-%s] - %s" % (self.plsa_id, self.title)

    def get_packages(self):
        return [x.split(" ", 1) for x in self.packages.split("\n") if x.strip()]

    def get_distro_packages(self):
        return [x.split() for x in self.packages.split("\n") if x.strip()]

    def get_distros(self):
        distros = []
        for x in self.packages.split("\n"):
            try:
                if x.strip() and x.split()[2] not in distros:
                    distros.append(x.split()[2])
            except IndexError:
                return []
        return distros

    def get_package_names(self):
        packages = []
        for x in self.packages.split("\n"):
            if x.strip() and x.split()[0] not in packages:
                packages.append(x.split()[0])
        return packages

    def get_references(self):
        return [x.strip() for x in self.references.split("\n") if x.strip()]

    def toPrettyString(self):
        import datetime

        title = _("Pardus Linux Security Advisory %s") % self.plsa_id
        email = _("security@pardus.org.tr")
        web = _("http://security.pardus.org.tr")

        headers = [
            (_("Date"), str(self.release_date)),
            (_("Severity"), str(self.severity)),
            (_("Type"), self.type)
        ]

        tpl = []

        tpl.append("-" * 72)
        tpl.append(justify("%s  %s" % (title, email), "  ", 72))
        tpl.append("-" * 72)
        tpl.extend(calign(headers))
        tpl.append("-" * 72)
        tpl.append("")

        tpl.append(_("Summary"))
        tpl.append("=" * len(_("Summary")))
        tpl.append("")
        tpl.append(wwrap(self.summary))
        tpl.append("")
        tpl.append("")

        tpl.append(_("Description"))
        tpl.append("=" * len(_("Description")))
        tpl.append("")
        for line in self.description.split("\n"):
            if line:
                tpl.append(wwrap(line, just=len(line) > 72))
            tpl.append("")
        tpl.append("")

        tpl.append(_("Affected packages:"))
        tpl.append("")
        release = None
        release_last = None
        for package, version in self.get_packages():
            if " " in version:
                version, release = version.split()
            if release != release_last:
                tpl.append("  Pardus %s:" % release)
            msg = _("all before %s") % version
            tpl.append("    %s, %s" % (package, msg))
            if release != release_last:
                release_last = release
            else:
                tpl.append("")
        tpl.append("")
        tpl.append("")

        up_release = {}
        up_name = []
        release = None
        for package, version in self.get_packages():
            if " " in version:
                version, release = version.split()
            if release not in up_release:
                up_release[release] = []
            up_release[release].append(package)
            if package not in up_name:
                up_name.append(package)

        tpl.append(_("Resolution"))
        tpl.append("=" * len(_("Resolution")))
        tpl.append("")
        if up_release:
            tpl.append(wwrap(_("There are update(s) for %s. You can update them via Package Manager or with a single command from console:") % ", ".join(up_name)))
            tpl.append("")
            if len(up_release) == 1:
                tpl.append("    pisi up %s" % " ".join(up_name))
            else:
                for release, packages in up_release.iteritems():
                    tpl.append("  Pardus %s:" % release)
                    tpl.append("    pisi up %s" % " ".join(packages))
                    tpl.append("")
            tpl.append("")

        if self.references:
            tpl.append(_("References"))
            tpl.append("=" * len(_("References")))
            tpl.append("")
            for ref in self.get_references():
              tpl.append("  * %s" % ref)
            tpl.append("")

        tpl.append("-" * 72)

        return "\n".join(tpl)

    class Meta:
        db_table = "plsa_plsa"
        verbose_name = _("Advisory")
        verbose_name_plural = _("Advisories")
        ordering = ["-id"]

    class Admin:
        list_display = ("id", "plsa_id", "title", "publish", "fixed", "release_date", "language")
        list_display_links = ("id", "plsa_id", "title")
        search_fields = ("title", "summary", "packages", "references")
        list_filter = ("language", "publish", "fixed")
        save_as = True
        save_on_top = True
        fields = (
            (None, {
                "fields": ("publish",
                           "fixed",
                           "language",
                           "plsa_id",
                           "type",
                           "severity",
                           "title",
                           "summary",
                           "description",
                           "packages",
                           "references")
            }),
        )

