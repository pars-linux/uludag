from django.db import models
from security.advisory.utils import *

class Language(models.Model):
    code = models.CharField(_("Code"), maxlength=5)
    name = models.CharField(_("Language"), maxlength=20)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "plsa_language"
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")

    class Admin:
        pass

class Advisory(models.Model):
    publish = models.BooleanField(_("Publish"))
    release_date = models.DateField(_("Last Update"), auto_now=True)
    language = models.ForeignKey("Language", verbose_name=_("Language"))
    plsa_id = models.CharField(_("PLSA ID"), maxlength=10, help_text=_("YEAR-NO"))
    type = models.CharField(_("Type"), maxlength=10, default="Local", help_text=_("Local or Remote"))
    severity = models.IntegerField(_("Severity"), default=1)
    title = models.CharField(_("Title"), maxlength=120)
    summary = models.TextField(_("Summary"))
    description = models.TextField(_("Description"))
    packages = models.TextField(_("Packages"), help_text=_("one package per row (put a whitespace between package name and version)"))
    references = models.TextField(_("References"), help_text=_("one link per row"))
    fixed = models.BooleanField(_("Ready to publish"))

    def __str__(self):
        return "[PLSA-%s] - %s" % (self.plsa_id, self.title)

    def plsaId(self):
        return "[%s] [PLSA %s] %s" % (self.language.code, self.plsa_id, self.title)

    def get_packages(self):
        return [x.split() for x in self.packages.split("\n")]

    def get_references(self):
        return self.references.split("\n")

    def toPrettyString(self):
        import datetime

        from django.utils.translation import gettext_lazy
        _ = lambda x: unicode(gettext_lazy(x))

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
        for package in self.packages.split("\n"):
            name, version = package.split()
            msg = _("all before %s") % version
            tpl.append("    %s, %s" % (name, msg))
        tpl.append("")
        tpl.append("")

        up = [p.split()[0] for p in self.packages.split("\n")]

        tpl.append(_("Resolution"))
        tpl.append("=" * len(_("Resolution")))
        tpl.append("")
        if up:
            tpl.append(wwrap(_("There are update(s) for %s. You can update them via Package Manager or with a single command from console:") % ", ".join(up)))
            tpl.append("")
            tpl.append("    pisi up %s" % " ".join(up))
            tpl.append("")

        if self.references:
            tpl.append(_("References"))
            tpl.append("=" * len(_("References")))
            tpl.append("")
            for ref in self.references.split("\n"):
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
        list_display = ("plsaId", "publish", "fixed", "release_date", "language")
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

