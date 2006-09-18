__all__ = ["utility", "gpg", "validator"]

class Error(Exception):
    pass

import gettext
import os
import os.path

import piksemel

import plsa.gpg
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

        self.data = {"id": "",
                     "revision": {"no": "",
                                  "date": "",
                                  "name": "",
                                  "email": ""},
                     "severity": "",
                     "title": "",
                     "summary": "",
                     "description": [],
                     "packages": [],
                     "references": []}

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

        self.data["revision"] = {"no": node_rev.getAttribute("revision"),
                                 "date": node_rev.getTagData("Date"),
                                 "name": node_rev.getTagData("Name"),
                                 "email": node_rev.getTagData("Email")}

        self.data["severity"]  = node_adv.getTagData("Severity")

        self.data["title"]  = get_localized_data(node_adv, "Title", self.lang).strip()
        self.data["summary"]  = get_localized_data(node_adv, "Summary", self.lang).strip()

        self.data["description"] = []
        for node in get_localized_node(node_adv, "Description", self.lang).tags():
            if node.firstChild():
                self.data["description"].append(node.firstChild().data().strip())
            else:
                self.data["description"].append("")
        """
                     "packages": [],
                     "references": []}
        """

    def build_text(self):
        _ = self.tr

        # TODO: Get these values from user
        title = _("Pardus Linux Security Advisory")
        email = _("security@pardus.org.tr")
        web = _("http://security.pardus.org.tr")

        headers = [(_("ID"), self.data["id"]),
                   (_("Date"), self.data["revision"]["date"]),
                   (_("Revision"), self.data["revision"]["no"]),
                   (_("Severity"), self.data["severity"])]

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
        tpl.append(wwrap(self.data["summary"]))
        tpl.append("")
        tpl.append("")

        tpl.append(_("Description"))
        tpl.append("=" * len(_("Description")))
        tpl.append("")
        for i in self.data["description"]:
            tpl.append(wwrap(i, just=len(i) > 72))
            tpl.append("")
        tpl.append("")

        # TODO: Complete "Affected Packages" and Resolution headings
        """
        if tags["packages_up"]:
            tpl.append(__tr("These packages should be upgraded to specified releases:"))
            for p, r in tags["packages_up"]:
              tpl.append("  * %s-%s" % (p, r))
            tpl.append("")

        if tags["packages_rm"]:
            tpl.append(__tr("These packages should be removed from system:"))
            for p in tags["packages_rm"]:
              tpl.append("  * %s" % p)
            tpl.append("")

        if tags["references"]:
            tpl.append(__tr("References"))
            tpl.append("=" * len(__tr("References")))
            for ref, link in tags["references"]:
              tpl.append("  * " + wwrap("%s <%s>" % (ref, link), lpad=4, just=0).strip())
            tpl.append("")
        """

        tpl.append("-" * 72)

        return "\n".join(tpl)
