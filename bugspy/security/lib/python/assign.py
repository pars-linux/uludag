#!/usr/bin/python
# Copyright 1999-2009 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

# Written by Robert Buchholz <rbu@gentoo.org>

import sys
import os
import re
try:
    import xml.etree.ElementTree as et
except ImportError:
    import elementtree.ElementTree as et

PORTDIR = "/usr/portage"
HERDS = PORTDIR + "/metadata/herds.xml"
heXML = None

def uniq(seq):
    """ order preserving unique """
    seen = {}
    result = []
    for item in seq:
        if not item in seen:
            seen[item] = 1
            result.append(item)
    return result

def get_pkg_cat(string):
    """ returns a list with packages or categories found that exist in portdir """
    metadatadirs = []
    
    matches = re.findall(r"(?#start:   )(?:^|\s)[<>~=]*(?#\
                              cat:     )([A-Za-z0-9+_][A-Za-z0-9+_.-]*/(?#\
                              pnv:     )[A-Za-z0-9+_][A-Za-z0-9+_.:@-]*)", string)

    for name in matches:
        # remove versions at the end
        name = re.sub(r"(?#version:   )-[0-9.]+[a-z]?(?#\
                           additions: )(_(alpha|beta|pre|rc|p)[0-9]*)?(?#\
                           revisions: )(-r[0-9]*)?(?#\
                           usedeps:   )(\[[!=?A-Za-z0-9+_@-]+\])?(?#\
                           slot deps: )(:[A-Za-z0-9+_.-]*)?$", "", name)

        if os.path.isdir("%s/%s" % (PORTDIR, name)):
            metadatadirs.append(name)
        else:
            (cat, _) = name.split('/', 1)
            if os.path.isdir("%s/%s" % (PORTDIR, cat)):
                metadatadirs.append(cat)

    return metadatadirs

def get_maintainer_for(directory):
    """ returns a priority-sorted list of maintainers for a given CAT or CAT/PN """
    cc = []
    try:
        if not heXML:
            globals()['heXML'] = et.parse(HERDS)
        meXML = et.parse("%s/%s/metadata.xml" % (PORTDIR, directory))

        for elem in meXML.getiterator():
            if elem.tag == "herd":
                for thisherd in heXML.findall("/herd"):
                    if thisherd.findtext("name") == elem.text:
                        herdmail = thisherd.findtext("email")
                        if herdmail:
                            cc.append(herdmail)
            elif elem.tag == "maintainer":
                email = elem.findtext("email")
                if not email:
                    continue
                if elem.get('ignoreauto') == "1" and elem.get('role'):
                    if email in cc:
                        cc.remove(email)
                else:
                    cc.append(email)

    except Exception:
        pass
    return cc

def get_cc_from_string(string):
    """ returns an ordered list of bug assignees / ccs for an arbitrary string such as
        a bug title. the first element of the tuple (if present) is supposed to be the
        assignee of the bug. """
    
    ccs = []
    
    """ replace ':' in "category/packet:", as it will prevent finding the correct maintainer(s) """
    string=string.replace(':','')

    metadatadirs = get_pkg_cat(string)
    for dir in metadatadirs:
        ccs.extend(get_maintainer_for(dir))

    # remove dupes
    ccs = uniq(ccs)
    return ccs

def main():
    if len(sys.argv) < 1:
        return
    arg = " ".join(sys.argv[1:])

    ccs = get_cc_from_string(arg)

    if len(ccs) > 0:
        print "assign-to: %s" % (ccs[0])
        print "cc: %s" % (",".join(ccs[1:]))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print '\n ! Exiting.'
