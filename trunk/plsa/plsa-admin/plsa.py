#!/usr/bin/python
# -*- coding: utf-8 -*-

# Standard Python Library
from optparse import OptionParser
import os
import os.path
import sys

# Utils
from utility import *

# XML Validator
from validator import validate_plsa

# piksemel
import piksemel

SUCCESS = 0
FAIL_USAGE = 1
FAIL_READ = 2
FAIL_WRITE = 3
FAIL_XML = 4
FAIL_KEY = 5
FAIL_PP = 6

def main():
    lang = os.environ["LANG"][:2]
    version = "1.0"
    usage = "%prog <options> advisory.xml"

    parser = OptionParser(usage=usage,  version="%prog " + version)
    parser.add_option("-s", "--sign", dest="sign",
                      help="sign advisory with KEY", metavar="KEY")
    parser.add_option("-p", "--pass", dest="passphrase",
                      help="use PASS as passphrase", metavar="PASS")
    parser.add_option("-l", "--language", dest="language",
                      help="set advisory language (default: %s)" % lang, metavar="LANG")
    parser.add_option("-o", "--output", dest="output",
                      help="save advisory text to FILE", metavar="FILE")
    options, args = parser.parse_args()

    if len(args) == 0:
        parser.print_help()
        return FAIL_USAGE

    if not os.path.isfile(args[0]) or not os.access(args[0], os.R_OK):
        print "Unable to read %s" % args[0]
        return FAIL_READ

    if not options.language:
        options.language = lang

    # Validate advisory xml
    xml_val = validate_plsa()
    xml_val.validate(args[0])
    if len(xml_val.errors):
        print "XML file has errors:"
        for i in xml_val.errors:
            print "  " + i
        return FAIL_XML

    # Generate advisory text
    xml_doc = piksemel.parse(args[0])
    adv = xml_doc.getTag("Advisory")

    nodes = [x.name() for x in adv.tags() if "xml:lang" in x.attributes() and x.getAttribute("xml:lang") == options.language and x.firstChild()]
    missing = set(["Title", "Summary", "Description"]) - set(nodes)
    if missing:
        print "XML has missing tags for locale '%s': %s" % (options.language, ", ".join(missing))
        return FAIL_XML

    # TODO: need cleanup here
    tags = {"id": adv.getAttribute("id"),
            "date": adv.getTagData("ReleaseDate"),
            "severity": adv.getTagData("Severity"),
            "title": localized_node(adv, "Title", options.language),
            "summary": localized_node(adv, "Summary", options.language),
            "description": localized_node(adv, "Description", options.language),
            "references": [],
            "packages_up": [],
            "packages_rm": []
            }

    ref = adv.getTag("References")
    if ref:
        node = ref.getTag("Reference")
        while node:
            tags["references"].append([node.getTagData("Name"), \
                                      node.getTagData("Link")])
            node = node.nextTag()

    pck = adv.getTag("Packages")
    if pck:
        node = pck.getTag("Package")
        while node:
            if "Release" in [i.name() for i in node.tags()]:
                tags["packages_up"].append([node.getTagData("Name"), \
                                            node.getTagData("Release")])
            else:
                tags["packages_rm"].append(node.getTagData("Name"))
            node = node.nextTag()

    headers = [("ID", tags["id"]),
               ("Title", tags["title"]),
               ("Severity", tags["severity"])]

    text = gen_advisory(headers, tags)

    # Sign advisory
    if options.sign:
        from getpass import getpass
        from gpg import GPG
        gnupg = GPG()
        if options.sign not in [x["keyid"][-8:] for x in gnupg.list_keys(secret=True)]:
            print "Key not found in GnuPG database."
            print "Available keys are:"
            for i in gnupg.list_keys(secret=1):
                print "  %s - %s" % (i["keyid"][-8:], i["uids"][1])
            return FAIL_KEY
        else:
            if not options.passphrase:
                options.passphrase = getpass("Passphrase: ")
            text_signed = gnupg.sign(text, options.sign, options.passphrase)
            if not str(text_signed):
                print "Invalid passphrase."
                return FAIL_PP
            else:
                text = text_signed

    if options.output:
        try:
            open(options.output, "w").write(text)
        except IOError:
            print "Unable to write advisory text to %s" % options.output
            return FAIL_WRITE
    else:
        print text

    return SUCCESS

if __name__ == "__main__":
    sys.exit(main())
