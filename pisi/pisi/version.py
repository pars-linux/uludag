# -*- coding: utf-8 -*-
#
# Copyright (C) 2005 - 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""version structure"""

import re
import string
import exceptions

import pisi
import pisi.util as util

maxdashes = 2

# Basic rule is:
# p > (no suffix) > m > rc > pre > beta > alpha
# m: milestone. this was added for OO.o
# p: patch-level
keywords = {
            "alpha" : 0,
            "beta"  : 1,
            "pre"   : 2,
            "rc"    : 3,
            "m"     : 4,
            "NOKEY" : 5,
            "p"     : 6,
            }

# helper functions
def has_keyword(versionitem):
    if versionitem._keyword != "NOKEY":
        return True

    return False

class VersionException(pisi.Exception):
    def __init__(self, str):
        pisi.Exception.__init__(self, str)

class VersionItem:
    _keyword = "NOKEY"
    _value = 0

    def __init__(self, itemstring):

        # special-case: 1.5p
        # here "p" comes as a separate itemstring and conflicts with
        # keyword "p". But keyword should allways contain an integer prefix.
        # So, skipping looking for keywords if the length() is 1 makes the
        # trick.
        if len(itemstring) > 1:

            for keyword in keywords.keys():
                if itemstring.startswith(keyword):

                    if self._keyword == "NOKEY":
                        self._keyword = keyword
                    else:
                        # longer match is correct
                        if len(keyword) > len(self._keyword):
                            self._keyword = keyword

        if self._keyword == "NOKEY":
            if len(itemstring) == 1 and itemstring in string.ascii_letters:
                # single letter version item ('a' to 'Z')
                self._value = itemstring
            elif len(itemstring) > 1 and itemstring[0] in string.ascii_letters:
                # Unknown keyword
                raise VersionException("")
            else:
                self._value = int(itemstring)
        else:
            # rest is the version item's value. And each must have
            # one!
            self._value = int(itemstring[len(self._keyword):])

    def __str__(self):
        return str(self._value)

    def __lt__(self,rhs):
        l = keywords[self._keyword]
        r = keywords[rhs._keyword]
        if l < r:
            return True
        elif l == r:
            return self._value < rhs._value
        else: # l > r
            return False

    def __le__(self,rhs):
        l = keywords[self._keyword]
        r = keywords[rhs._keyword]
        if l < r:
            return True
        elif l == r:
            return self._value <= rhs._value
        else: # l > r
            return False

    def __gt__(self,rhs):
        l = keywords[self._keyword]
        r = keywords[rhs._keyword]
        if l > r:
            return True
        elif l == r:
            return self._value > rhs._value
        else: # l < r
            return False

    def __ge__(self,rhs):
        l = keywords[self._keyword]
        r = keywords[rhs._keyword]
        if l > r:
            return True
        elif l == r:
            return self._value >= rhs._value
        else: # l < r
            return False

    def __eq__(self,rhs):
        l = keywords[self._keyword]
        r = keywords[rhs._keyword]
        if l == r and self._value == rhs._value:
                return True
        return False

class Version:

    @staticmethod
    def valid(version):
        try:
            pisi.version.Version(version)
        except pisi.version.VersionException, e:
            return False
        return True

    def __init__(self, verstring):
        # PiSi version policy does not allow "-" in version strings.
        # They are special and used for build and release no separation.
        if verstring.count("-") > maxdashes:
            raise VersionException("%s is not a valid PiSi version format" % verstring)

        verchunks = verstring.split("-")
        verchunks.extend("0" * (maxdashes - verstring.count("-")))
        (version, release, build) = verchunks

        self.comps = []
        for i in util.multisplit(version,'._'):
            # some version strings can contain ascii chars at the
            # back. As an example: 2.11a
            # We split '11a' as two items like '11' and 'a'
            s = re.compile("[a-z-A-Z]$").search(i)
            if s:
                head = i[:s.start()]
                tail = s.group()
                self.comps.append(VersionItem(head))
                self.comps.append(VersionItem(tail))
            else:
                self.comps.append(VersionItem(i))

        self.verstring = verstring
        self.release = VersionItem(release)
        self.build = VersionItem(build)

    def string(self):
        return self.verstring

    def compare(self, ver):
        """this comparison routine is essentially a comparison routine
        for two rationals in (0,1) interval. we compare two sequences
        of digits one by one. We start with the leftmost digit
        in the expansion. If they are equal, we proceed to the next. If
        not we use the comparison operator. And we iterate to the left.
        The result is, 0 if two are equal, -1 if self < rhs, and +1
        if self>rhs"""

        if isinstance(ver, basestring):
            ver = pisi.version.Version(ver)

        lhs = self.comps
        rhs = ver.comps
        # pad the short version string with zeros
        if len(lhs) < len(rhs):
            lhs.extend( [VersionItem('0')] * (len(rhs) - len(lhs)) )
        elif len(lhs) > len(rhs):
            rhs.extend( [VersionItem('0')] * (len(lhs) - len(rhs)) )
        # now let's iterate from left to right in version items
        for (litem, ritem) in zip(lhs, rhs):
            if litem < ritem:
                return -1
            elif litem > ritem:
                return +1
        # now let's compare release and build
        lhs = (self.release, self.build)
        rhs = (ver.release, ver.build)
        for (litem, ritem) in zip(lhs, rhs):
            if litem < ritem:
                return -1
            elif litem > ritem:
                return +1
        return 0

    # premature optimization is the root of all evil

    def __lt__(self,rhs):
        return self.compare(rhs) < 0

    def __le__(self,rhs):
        return self.compare(rhs) <= 0

    def __gt__(self,rhs):
        return self.compare(rhs) > 0

    def __ge__(self,rhs):
        return self.compare(rhs) >= 0

    def __eq__(self,rhs):
        return self.compare(rhs) == 0

    def __str__(self):
        return self.verstring
