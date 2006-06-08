#!/usr/bin/python

# Standard Python Modules
import gettext
from optparse import OptionParser
import sys

# PISI Modules
import pisi
import pisi.context as ctx
from pisi.fetcher import fetch_url
from pisi.uri import URI
from pisi.file import File

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

def printPLSA(id, title, summary, up=[], fix=[], no_fix=[]):
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

    #if options.long:
    #    print colorize("    %s" % summary, "brightblack")

    if options.packages:
        if len(up) and not options.affected:
            print colorize("    a: %s" % ", ".join(up), color_list["A"])
        if len(fix):
            print colorize("    u: %s" % ", ".join(fix), color_list["U"])
        if len(no_fix):
            print colorize("    x: %s" % ", ".join(no_fix), color_list["X"])

def main():
    # Show package details in --long
    if options.long:
        options.packages = True

    # Init PISI API
    pisi.api.init(database=True, comar=False, write=False)

    if options.fetch:
        # Fetch PLSA database
        print _("Downloading PLSA database...")
        fetch_url("http://cekirdek.pardus.org.tr/~bahadir/files/plsa-index.xml.bz2", "/tmp", progress=ctx.ui.Progress)

        print _("Unpacking PLSA database...")
        File.decompress("/tmp/plsa-index.xml.bz2", File.bz2)

    print _("Scanning advisories...")
    print

    # Get installed packages
    installed_packages = {}
    for package in ctx.installdb.list_installed():
        # Release comarison seems enough
        installed_packages[package] = int(ctx.installdb.get_version(package)[1])

    # Get list of reporsitories
    local_repos = {}
    for r in ctx.repodb.list():
        uri = ctx.repodb.get_repo(r).indexuri.get_uri()
        # Remove filename
        local_repos[r] = uri[0:uri.rfind("/")]

    # Update list for summary
    updates = {}

    # Parse PLSA XML
    p = piksemel.parse("/tmp/plsa-index.xml")

    adv = p.getTag("Advisory")
    while adv:
        id = adv.getAttribute("Id")
        title = adv.getTagData("Title")
        summary = adv.getTagData("Summary")

        up, fix, no_fix = [], [], []

        pack = adv.getTag("Packages").getTag("Package")
        while pack:
            package = pack.getTagData("Name")
            release = pack.getTagData("Release")
            repo = pack.getTagData("Reporsitory")

            # Pass if package is not installed
            if package not in installed_packages:
                pack = pack.nextTag()
                continue

            # Pass if package repo is different
            repo_installed_package = ctx.packagedb.get_package_repo(package)[1]
            if local_repos[repo_installed_package] != repo:
                pack = pack.nextTag()
                continue

            if release[-1] != "<":
                if int(release.split("<")[-1]) > my_packages[package]:
                    fix.append(package)
                else:
                    up.append(package)
            else:
                no_fix.append(package)
            pack = pack.nextTag()

        # Print PLSA
        if len(up + fix + no_fix):
            printPLSA(id, title, summary, up, fix, no_fix)

        adv = adv.nextTag()

    print

    # Show tips
    if not options.affected:
        print "%s means that system is not affected." % colorize("[A]", color_list["A"])
    print "%s means that you need an update." % colorize("[U]", color_list["U"])
    print "%s means that there's no fix available for that package." % colorize("[X]", color_list["X"])
    print "%s means that some packages are affected." % colorize("[P]", color_list["P"])

    # Show footnote for package details
    if not options.packages:
        print
        print _("Note: You can use --package option to see affected packages.")

    # Finalize PISI API
    pisi.api.finalize()

if __name__ == "__main__":
    parser = OptionParser(usage="%prog [options]", version="%prog 1.0")

    parser.add_option("-N", "--no-color",
                      action="store_false", dest="color", default=True,
                      help=_("don't use colors"))
    parser.add_option("-p", "--packages",
                      action="store_true", dest="packages", default=False,
                      help=_("show package names"))
    parser.add_option("-l", "--long",
                      action="store_true", dest="long", default=False,
                      help=_("show details of announcement"))
    parser.add_option("-a", "--all",
                      action="store_false", dest="affected", default=True,
                      help=_("show all announcements"))
    parser.add_option("-F", "--no-fetch",
                      action="store_false", dest="fetch", default=True,
                      help=_("don't download PLSA index"))

    (options, args) = parser.parse_args()

    sys.exit(main())
