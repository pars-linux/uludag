#!/usr/bin/python

# Standard Python Modules
import gettext
from optparse import OptionParser
import os
import sys

# PISI Modules
import pisi
import pisi.context as ctx
from pisi.fetcher import fetch_url, FetchError
from pisi.uri import URI
from pisi.file import File
from pisi.util import sha1_file

# Piksemel Module
import piksemel

# Colors
from colors import colors
color_list = {"A": "brightblack",
              "U": "green",
              "P": "cyan",
              "X": "red"}

# i18n
__trans = gettext.translation("plsa", fallback=True)
_ = __trans.ugettext

def colorize(msg, color):
    """Colorize given message"""
    if color in colors and options.color:
        return "".join((colors[color], msg, colors["default"]))
    return msg

def printPLSA(repo, id, title, summary, up=[], fix=[], no_fix=[]):
    """Prints PLSA details"""
    flag = ""
    if len(no_fix):
        if len(up + fix):
            flag = "P"
        else:
            flag = "X"
    else:
        if not len(fix):
            if not options.affected:
                flag = "A"
        else:
            flag = "U"

    if not flag:
        return

    print colorize("[%s] %s - %s" % (flag, id, title), color_list[flag])

    if options.long:
        print "    %s" % colorize(_("Summary: %s") % summary, color_list[flag])

    if options.packages:
        if len(up) and not options.affected:
            print colorize("    a: %s" % ", ".join(up), color_list["A"])
        if len(fix):
            print colorize("    u: %s" % ", ".join(fix), color_list["U"])
        if len(no_fix):
            print colorize("    x: %s" % ", ".join(no_fix), color_list["X"])

def get_localtext(node, lang="en"):
    """Returns tag data with selected xml:lang attribute"""
    name = node.name()
    text = {}
    while node.name() == name:
        lng = node.getAttribute("xml:lang")
        if node.firstChild():
            text[lng] = node.firstChild().data()
        else:
            text[lng] = ""
        node = node.nextTag()
    if lang in text:
        return text[lang]
    else:
        return text["en"]

def main():
    global options

    # Parse options
    parser = OptionParser(usage="%prog [options]", version="%prog 1.0")

    parser.add_option("-N", "--no-color",
                      action="store_false", dest="color", default=True,
                      help=_("don't use colors"))
    parser.add_option("-p", "--packages",
                      action="store_true", dest="packages", default=False,
                      help=_("show package names"))
    parser.add_option("-l", "--long",
                      action="store_true", dest="long", default=False,
                      help=_("show details of advisories"))
    parser.add_option("-a", "--all",
                      action="store_false", dest="affected", default=True,
                      help=_("show all advisories"))
    parser.add_option("-F", "--no-fetch",
                      action="store_false", dest="fetch", default=True,
                      help=_("don't download PLSA index"))

    (options, args) = parser.parse_args()
    
    # Get locale
    lang = os.environ["LC_ALL"].split("_")[0]

    # Show package details in --long
    if options.long:
        options.packages = True

    # Create work directory
    if not os.access("/tmp/plsa", os.F_OK):
        os.mkdir("/tmp/plsa")

    # Init PISI API
    pisi.api.init(database=True, comar=False, write=False)

    # Get installed packages
    installed_packages = {}
    for package in ctx.installdb.list_installed():
        # Release comparison seems enough
        installed_packages[package] = int(ctx.installdb.get_version(package)[1])

    # List of orphaned packages
    orphaned = []

    # Get list of reporsitories
    plsas = {}
    for repo in ctx.repodb.list():
        uri = ctx.repodb.get_repo(repo).indexuri.get_uri()
        plsafile = "%s/plsa-index.xml.bz2" % uri[0:uri.rfind("/")]
        tmpfile = "/tmp/plsa/%s.xml" % repo

        if options.fetch:
            print _("Downloading PLSA database of %s") % repo
            try:
                fetch_url(plsafile, "/tmp/plsa", progress=ctx.ui.Progress)
            except FetchError, e:
                print _("Unable to download %s: %s") % (plsafile, e)
                continue

            print _("Checking file integrity of %s") % repo
            try:
                fetch_url("%s.sha1sum" % plsafile, "/tmp/plsa")
            except FetchError, e:
                print _("Unable to download checksum of %s") % repo
                continue

            orig_sha1sum = file("%s.sha1sum" % plsafile).readlines()[0].split()[0]
            if sha1_file(plsafile) != orig_sha1sum:
                print _("File integrity of %s compromised.") % plsafile
                continue

            print _("Unpacking PLSA database of %s") % repo
            try:
                File.decompress("/tmp/plsa/plsa-index.xml.bz2", File.bz2)
            except:
                print _("Unable to decompress %s") % plsafile
                continue
            
            os.rename("/tmp/plsa/plsa-index.xml", tmpfile)
            os.unlink("/tmp/plsa/plsa-index.xml.bz2")
            plsas[repo] = tmpfile

        elif os.access(tmpfile, os.F_OK):
            print _("Found PLSA database of %s in cache") % repo
            plsas[repo] = tmpfile

        print

    # Pass if no PLSA available
    if not len(plsas):
        print _("No PLSA database available")
        finalize()

    print _("Scanning advisories...")
    print

    # Update list for summary
    updates = {}

    # Parse PLSA databases
    for repo, plsafile in plsas.iteritems():
        p = piksemel.parse(plsafile)

        adv = p.getTag("Advisory")
        while adv:
            id = adv.getAttribute("Id")
            title = get_localtext(adv.getTag("Title"), lang)
            summary = get_localtext(adv.getTag("Summary"), lang)

            up, fix, no_fix = [], [], []

            pack = adv.getTag("Packages").getTag("Package")
            while pack:
                package = pack.getTagData("Name")
                release = pack.getTagData("Release")

                # Pass if package repo is missing
                try:
                    pack_repo = ctx.packagedb.which_repo(package)
                except:
                    if package not in orphaned:
                        orphaned.append(package)
                    pack = pack.nextTag()
                    continue

                # Pass if package does not come from current repo or
                # package is not installed
                if  pack_repo != repo or \
                    package not in installed_packages:
                    pack = pack.nextTag()
                    continue

                # Check if package is affected
                if release[-1] != "<":
                    if int(release.split("<")[-1]) > installed_packages[package]:
                        fix.append(package)
                    else:
                        up.append(package)
                else:
                    no_fix.append(package)
                pack = pack.nextTag()

            # Print PLSA
            if len(up + fix + no_fix):
                printPLSA(repo, id, title, summary, up, fix, no_fix)

            adv = adv.nextTag()
            
    print

    # Show tips
    if not options.affected:
        print _("%s means that system is not affected.") % colorize("[A]", color_list["A"])
    print _("%s means that you need an update.") % colorize("[U]", color_list["U"])
    print _("%s means that there's no fix available for that package.") % colorize("[X]", color_list["X"])
    print _("%s means that some packages are affected.") % colorize("[P]", color_list["P"])

    # Show footnote for package details
    if not options.packages:
        print
        print _("Note: You can use --package option to see affected packages.")

    finalize()

def finalize(r=0):
    pisi.api.finalize()
    sys.exit(r)

if __name__ == "__main__":
    main()
