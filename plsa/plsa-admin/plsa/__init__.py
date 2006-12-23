__all__ = ["utility", "gpg", "validator"]

class Error(Exception):
    pass

import gettext
import os
import os.path
import datetime

import piksemel

import plsa.validator
from plsa.utility import *
from plsa.xml import *

class advisory:
    def __init__(self, lang="en"):
        try:
            trans = gettext.translation("plsa", languages=[lang], fallback=lang=="en")
            self.tr = trans.ugettext
        except:
            raise Error, "'%s' locale not supported." % lang

        self.lang = lang

        self.data = {
            "id": "",
            "revision": {
                "no": "",
                "date": "",
                "name": "",
                "email": ""
            },
            "severity": "",
            "title": "",
            "summary": "",
            "description": [],
            "packages": [],
            "references": []
        }

    def import_xml(self, xmlfile):
        self.xml_doc = None
        self.errors = []

        try:
            self.xml_doc = piksemel.parse(xmlfile)
        except:
            self.errors.append("XML file has errors.")
            return

        # Validate advisory.xml
        val = plsa.validator.validate_plsa()
        val.validate(self.xml_doc)
        self.errors = val.errors

        if self.errors:
            raise Error, "XML file has errors."

        # TODO: Make this check in validator.py
        required_tags = ["Title", "Summary", "Description"]
        node_adv = self.xml_doc.getTag("Advisory")
        nodes = [x.name() for x in node_adv.tags() if "xml:lang" in x.attributes() and x.getAttribute("xml:lang") == self.lang and x.firstChild()]
        missing = set(required_tags) - set(nodes)
        if missing:
            self.errors.append("XML has missing tags for locale '%s': %s" % (self.lang, ", ".join(missing)))

        if self.errors:
            raise Error, "XML file has errors."

        # Get data from xml
        node_rev = self.xml_doc.getTag("History").getTag("Update")

        self.data["id"]  = node_adv.getAttribute("id")

        rev = self.data["revision"]
        rev["no"] = node_rev.getAttribute("revision")
        rev["date"] = node_rev.getTagData("Date")
        rev["name"] = node_rev.getTagData("Name")
        rev["email"] = node_rev.getTagData("Email")

        self.data["severity"]  = node_adv.getTagData("Severity")

        self.data["title"]  = get_localized_data(node_adv, "Title", self.lang).strip()
        self.data["summary"]  = get_localized_data(node_adv, "Summary", self.lang).strip()

        self.data["description"] = []
        for node in get_localized_node(node_adv, "Description", self.lang).tags():
            if node.firstChild():
                self.data["description"].append(node.firstChild().data().strip())
            else:
                self.data["description"].append("")

        self.data["packages"] = []
        for node in node_adv.getTag("Packages").tags():
            package = [node.firstChild().data(), ""]
            if "fixedAt" in node.attributes():
                package[1] = node.getAttribute("fixedAt")
            self.data["packages"].append(package)

        self.data["references"] = []
        for node in node_adv.getTag("References").tags():
            self.data["references"].append(node.firstChild().data())

    def build_text(self):
        _ = self.tr

        # TODO: Get these values from user
        title = _("Pardus Linux Security Advisory %s-%s" % (datetime.date.today().year,self.data["id"]))
        email = _("security@pardus.org.tr")
        web = _("http://security.pardus.org.tr")

        headers = [
            (_("Date"), self.data["revision"]["date"]),
            (_("Revision"), self.data["revision"]["no"]),
            (_("Severity"), self.data["severity"])
        ]

        tpl = []

        tpl.append("-" * 85)
        tpl.append(justify("%s  %s" % (title, email), "  ", 72))
        tpl.append("-" * 85)
        tpl.extend(calign(headers))
        tpl.append("-" * 85)
        tpl.append("")

        tpl.append(_("Summary"))
        tpl.append("=" * len(_("Summary")))
        tpl.append("")
        tpl.append(wwrap(self.data["summary"]))
        tpl.append("")
        tpl.append("")

        tpl.append(_("Description"))
        tpl.append("=" * len(_("Description")))
        tpl.append("")
        for i in self.data["description"]:
            tpl.append(wwrap(i, just=len(i) > 72))
            tpl.append("")

        tpl.append(_("Affected packages:"))
        tpl.append("")
        for package, version in self.data["packages"]:
            msg = _("all versions")
            if version:
                msg = _("all before %s") % version
            tpl.append("    %s, %s" % (package, msg))
        tpl.append("")
        tpl.append("")

        up = [p[0] for p in self.data["packages"]]

        tpl.append(_("Resolution"))
        tpl.append("=" * len(_("Resolution")))
        tpl.append("")
        if up:
            tpl.append(wwrap(_("There are update(s) for %s. You can update them via Package Manager or with a single command from console:") % ", ".join(up)))
            tpl.append("")
            tpl.append("    pisi up %s" % " ".join(up))
            tpl.append("")

        if self.data["references"]:
            tpl.append(_("References"))
            tpl.append("=" * len(_("References")))
            tpl.append("")
            for ref in self.data["references"]:
              tpl.append("  * %s" % ref)
            tpl.append("")

        tpl.append("-" * 85)

        return "\n".join(tpl)
