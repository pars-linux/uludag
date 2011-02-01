#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Executable file that takes a file and files a security bug.
#

import sys
import os
import logging

from bugspy.bugzilla import Bugzilla
from bugspy.config import BugspyConfig

# Files to edit
TRACKER_PARDUS_2009 = "./data/Pardus/tracker.2009.ini"
TRACKER_PARDUS_2008 = "./data/Pardus/tracker.2008.ini"
TRACKER_PARDUS_CORPORATE2 = "./data/Pardus/tracker.corporate2.ini"

TRACKER_MAP = {"2009": TRACKER_PARDUS_2009,
               "Corporate2": TRACKER_PARDUS_CORPORATE2}

# Global variable that is used when asked for which pardus versions are affected
PARDUS_RELEASES = {"1": "2009",
                   "2": "Corporate2",
                   "3": "2011"}

log = logging.getLogger("bugzilla")
log.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter("\033[35m%(levelname)s: %(name)s: %(message)s\033[0m"))

log.addHandler(ch)

def readFile(filename):
    """Reads a file and returns an array containing title and description

    Args:
        filename: File name to open

    Returns:
        Array containing title and description. First item in the list is title, second is description.
    """

    if not os.path.exists(os.path.expanduser(filename)):
        print "[-] File does not exist. Exiting..."
        sys.exit()

    data = open(filename, "r").read()

    try:
        # get title
        title = data.split("\n")[0]

        # read everything after title.
        # +2 is for \n and blank char that comes after title
        description = data[len(title)+2:]

        return (title, description)
    except:
        print "[-] Error while parsing file."
        sys.exit()

def main(filename):
    title, description = readFile(filename)

    c = BugspyConfig()
    bugzilla = Bugzilla(c.bugzillaurl, c.username, c.password)

    new_bug = {}
    new_bug["title"] = title
    new_bug["description"] = description
    new_bug["product"] = "Güvenlik / Security"

    print "Proessing bug: %s" % title
    print description

    print ''

    print "Component for bug [Enter=General, k=Kernel]: ",
    comp = sys.stdin.readline()
    component = ""
    if comp[0] == "g" or comp[0] == "\n":
        component = "guvenlik/security"
    elif comp[0] == "k":
        component = "cekirdek / kernel"
    else:
        component = "guvenlik/security"

    new_bug["component"] = component

    print ''

    print "Which Pardus versions are affected?"
    print "1- Pardus 2009"
    print "2- Pardus Corporate2"
    print "3- Pardus 2011\n"

    affected_pardus_versions = []
    while 1:
        print "Append Pardus version [r=Revert, q=Quit]: ",
        answer = sys.stdin.readline()
        answer = answer[0]
        if answer == "q":
            if len(affected_pardus_versions) > 0:
                break
            else:
                print "You need to specify at least 1 version"
                continue

        if answer == "r":
            affected_pardus_versions = []
            continue

        if answer == "\n":
            print affected_pardus_versions
            continue

        if not answer in PARDUS_RELEASES.keys():
            print "Invalid entry"
        else:
            if PARDUS_RELEASES.get(answer) in affected_pardus_versions:
                print "This is already selected"
            else:
                affected_pardus_versions.append(PARDUS_RELEASES.get(answer))
                print affected_pardus_versions

    print ''
    print "Assign this bug to [Enter=default]: ",
    answer = sys.stdin.readline()
    if answer[0] != "\n":
        assigned_to = answer.replace("\n", "")
        print "Bug is assigned and CCed to: %s" % assigned_to
        new_bug["cc"] = assigned_to
    else:
        assigned_to = None
        print "Not assigning. Assignee is default."

    print ''
    print "Add CC [Enter=none]: ",
    answer = sys.stdin.readline()
    if answer[0] != "\n":
        cc_address = answer.replace("\n", "")
        print "Address CCed: %s" % cc_address
    else:
        cc_address = None

    print ''
    print "Make his bug private? [Y/n]: ",
    answer = sys.stdin.readline()
    if answer[0] == "y" or answer[0] == "\n":
        new_bug["security"] = 1
    elif answer[0] == "n":
        new_bug["security"] = 0

    print '\n!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    print '!!!!!!!!!!!!!!!!!!!!!!!!!!!'
    print "Title     : %s" % title
    print "Component : %s" % component
    print "Affected  : %s" % ', '.join(affected_pardus_versions)
    print "Private?  : %s" % new_bug["security"]
    print "Assigned  : %s" % assigned_to
    print "CCed      : %s" % cc_address
    print description + "\n"

    print "\nWill file this bug [Y/n]: ",

    answer = sys.stdin.readline()
    if answer[0] == "y" or answer[0] == "Y" or answer[0] == "\n":
        print "Filing the bug..."

        bugzilla.login()
        bugno = bugzilla.new(**new_bug)

        if bugno:
            print "Success! http://bugs.pardus.org.tr/%s" % (bugno)
            print "   %s" % title

            # add each entry to files and file a bug
            for affected_version in affected_pardus_versions:
                bug_title = "%s - Pardus %s" % (title.replace("\n",""), affected_version)
                bug_desc = "Pardus %s is affected from bug #%s" % (affected_version, bugno)

                no = bugzilla.new(title=bug_title,
                                  description=bug_desc,
                                  security=1,
                                  component=component,
                                  status="ASSIGNED",
                                  assigned_to=assigned_to,
                                  cc=cc_address,
                                  version=affected_version,
                                  product="Güvenlik / Security",
                                  blocks=bugno)

                print "Success! http://bugs.pardus.org.tr/%s" % no
                print "   %s" % bug_title

                # FIXME: Add them to tracker file when we move to new tracker system
                #file = TRACKER_MAP.get(affected_version)
                #ini = SecurityINI(file)

                # redhat enterprise_linux: multiple integer overflows (CVE-2010-0727)
                # will be: multiple integer overflows (CVE-2010-0727)
                #mini_description = title.split(":")[1]

                #ini.addEntry("in bugzilla not fixed", self.bugs_atom.lstrip(), "%s: %s: qa?" % (bugno, severity), mini_description)
                #ini.save()

if __name__ == '__main__':
    if not len(sys.argv) > 1:
        print "[-] Missing argument. File is needed to read from."
        sys.exit()

    main(sys.argv[1])
