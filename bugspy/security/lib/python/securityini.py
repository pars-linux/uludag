#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# A configuration library for tracking packages for security.
#
# Its purpose is to add/move entries into tracker file.
#
# Eren Türkay, <eren:pardus.org.tr>. March 27, 2010
#

import os
from configobj import ConfigObj

#FIXME: remove on production
import sys

class IniError(Exception):
    pass


class Struct(object):
    """A container which can be accessed like class objects

    f = Struct(foo="bar", baz="heh", bug=Struct("id": 1))
    f.set("comment", "foobar")

    print f.foo
    print f.bug.id
    print f.comment

    """

    def __init__(self, __str = None, **kwargs):
        self.__str = __str
        self.__dict__.update(kwargs)

    def __str__(self):
        if self.__str:
            return "%s" % self.__str
        else:
            return "<Struct: %s>" % self.__dict__

    def __repr__(self):
        return "<Struct: %s>" % self.__dict__

    def set(self, key, arg):
        self.__dict__.update({key: arg})

    def has(self, key):
        if self.__dict__.has_key(key):
            return True
        else:
            return False

class SecurityINI:
    def __init__(self, filename=None):
        if not filename:
            raise IniError("Filename must be supported")

        self.filename = filename

        # ConfigObj
        self.config = None
        self.readConfig()

    def readConfig(self):
        # FIXME: Do validation before reading it.
        self.config = ConfigObj(os.path.expanduser(self.filename))

    def _controlSection(self, section):
        if not self.has_section(section):
            raise IniError('Section "%s" does not exist' % section)

    def has_section(self, section):
        if self.config.has_key(section):
            return True
        else:
            return False

    def has_entry(self, section, key):
        self._controlSection(section)

        if self.config[section].has_key(key):
            return True
        else:
            return False

    def addEntry(self, section, key, data, comments=None):
        """Adds entry to given section.

        It handles same keys. If the same key is added, it adds "_1" to the
        key. If "_1" also exists, increments it.

        Args:
            section: Section name to add
            key: Key
            data: Data
            comment: Array.(optional) comment to add at the beginning of a key

        Returns:
            True when entry is added.

        Raises:
            IniError
        """

        self._controlSection(section)

        section = self.config[section]

        if isinstance(comments, str):
            if comments.find("\n") > -1:
                comments = comments.split("\n")
                comments.insert(0, '')
                # comment dict's first element should be ''. We do it so that entries have blank chars on top of them.
            else:
                comments = [""]
        else:
            comments = [""]

        # handle individual keys first.
        if not section.has_key(key):
            section[key] = data
            section.comments[key] = comments
        else:
            # now we are dealing with multiple keys. Increment the variable until we hit
            key = "%s_0" % key
            while 1:
                (string, num) = key.split("_")
                key = "%s_%s" % (string, int(num) + 1)
                if not section.has_key(key):
                    # we hit a key
                    break

            section[key] = data
            section.comments[key] = comments

    def getEntry(self, section, key):
        """Gets entry from section.

        It handles multiple keys and returns an array for items which have "_1, _2" suffix. For example: If you have following keys:

            [my-section]
            kernel = denial of service: medium
            kernel_1 = privilage escalation: high
            kernel_2 = foobar

        You get all of them in an array form with:

            kernel = ini.getEntry("my-section", "kernel")
            for i in kernel:
                print i
                print "Comments: %s" % i.comments

        Args:
            section: Section in ini file
            key: Key to get

        Returns:
            An array containing Struct. This struct has comments attribute which includes comments for a key.

        """

        self._controlSection(section)

        section = self.config[section]

        if section.has_key(key):
            # we are not dealing with multiple keys, just return the key
            if not section.has_key("%s_1" % key):
                output = Struct(section[key], comments=section.comments[key], inline_comments=section.inline_comments[key])
                return output
            else:
                output = []
                output.append(Struct(section[key], comments=section.comments[key], inline_comments=section.inline_comments[key]))
                # we know that there exist a key with _1 suffix
                key = "%s_1" % key
                while 1:
                    if not section.has_key(key):
                        # we hit non-existant key
                        break

                    output.append(Struct(section[key], comments=section.comments[key], inline_comments=section.inline_comments[key]))
                    # increment the number
                    (string, num) = key.split("_")
                    key = "%s_%s" % (string, int(num) + 1)

                return output

        else:
            raise IniError("Key '%s' does not exist")

    def moveEntry(self, key, fromSection, toSection):
        """Move entry from one section to another

        Args:
            key: Key to move
            fromSection: Key's section
            toSection: Section to move
        """

        self._controlSection(fromSection)
        self._controlSection(toSection)

        # FIXME: we cannot move multiple packages which have _1, _2 suffixes
        # FIXME: think about them.

        original_entry = self.getEntry(fromSection, key)

        from_section = self.config[fromSection]
        to_section = self.config[toSection]

        if to_section.has_key(key):
            raise IniError("Section '%s' has key '%s'" % (to_section, key))

        to_section[key] = original_entry
        to_section.comments[key] = original_entry.comments
        to_section.inline_comments[key] = original_entry.inline_comments

        del from_section[key]

    def save(self):
        #FIXME: Do validation before writing.
        self.config.write()

def main():
    ini = SecurityINI("test.ini")

    if not ini.has_entry("in bugzilla not fixed", "amarok"):
        print "Amarok is not there, exiting..."
        sys.exit(1)

    ini.moveEntry("amarok", "in bugzilla not fixed", "fixed, needs compiling")
    ini.save()

    #ini.save()

if __name__ == '__main__':
    main()
