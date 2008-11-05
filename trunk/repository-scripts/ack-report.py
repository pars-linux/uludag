#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import time

from pisi.package import Package

# Generates detailed statistics about pisi files

test_path = "/var/www/localhost/htdocs/pardus-2008-test/"
stable_path = "/var/www/localhost/htdocs/pardus-2008/"

template = """\
Modification time: %s
    by %s
Version: %s
Release: %s
Type: %s
Changes:

%s\n
"""

def get_package_name(filename):
    return filename.rstrip(".pisi").rsplit("-", 3)[0]

def get_package_build(filename):
    return int(filename.rstrip(".pisi").rsplit("-", 3)[3])

def get_package_release(filename):
    if filename:
        return int(filename.rstrip(".pisi").rsplit("-", 3)[2])
    else:
        return 0

def get_latest_package(package):
    """ Returns the file name corresponding to the
    latest release of the package 'package_name' found in 'path'."""

    file_list = glob.glob1(stable_path, "%s-[0-9]*-[0-9]*-[0-9]*.pisi" % get_package_name(package))
    file_list.sort(cmp=lambda x,y:get_package_build(x)-get_package_build(y), reverse=True)
    try:
        name = file_list[0]
        return name
    except IndexError:
        return ""

def main(file_list):

    files = open(file_list, "rb").read().strip().split("\n")

    d = {}

    for f in files:

        if os.path.exists(os.path.join(test_path, f)):

            name = get_package_name(f)
            latest_package = get_latest_package(f)
            current_release = get_package_release(f)
            stable_release = get_package_release(latest_package)

            if f != latest_package:

                metadata = Package(os.path.join(test_path, f)).get_metadata()
                packager = "%s <%s>" % (metadata.source.packager.name, metadata.source.packager.email.replace('@', '_at_'))

                changes = ""
                for h in metadata.package.history[0:current_release-stable_release]:
                    changes += template % (h.date, ("%s <%s>" % (h.name, h.email.replace('@', '_at_'))),
                                           h.version, h.release, h.type,
                                           "\n".join([l.strip() for l in h.comment.split('\n')]))

                d[name] = [current_release, stable_release, packager, changes]

    # Generate statistics file
    stats = open("stats-%s" % "-".join([str(i) for i in time.localtime()[:3]]), "wb")

    stats.write("Testing->Stable merge reports for %s\n%s\n\n" % (time.asctime(), '-'*60))

    new_packages = []
    security_updates = []

    for package in d.keys():
        if d[package][1] == 0:
            new_packages.append(package)
        if "Type: security" in d[package][3]:
            security_updates.append(package)

    stats.write("** Total new packages: %d\n" % len(new_packages))
    for p in new_packages:
        stats.write("   * %s\n" % p)
    stats.write("\n** Total security updates: %d\n" % len(security_updates))
    for p in security_updates:
        stats.write("   * %s\n" % p)

    stats.close()


    for p in d.keys():
        print "\nName: %s\nPackager: %s" % (p, d[p][2])
        print "-"*55
        print d[p][3],

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Usage: %s <file_list>" % sys.argv[0]
        sys.exit(1)

    else:
        file_list = sys.argv[1]
        if not os.path.exists(file_list):
            print "%s doesn't exist!" % file_list
            sys.exit(1)

        sys.exit(main(file_list))



