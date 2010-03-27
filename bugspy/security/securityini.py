#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from configobj import ConfigObj

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
        if not self.config.has_key(section):
            raise IniError('Section "%s" does not exist' % section)

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

        # if comments is not array, make it array and also strip \n
        if not isinstance(comments, list):
            if comments.find("\n") > -1:
                comments = comments.split("\n")
                comments.insert(0, '')
                # comment dict's first element should be ''. We do it so that entries have blank chars on top of them.
            else:
                comments = [comments]
                comments.insert(0, '')

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
                output = Struct(section[key], comments=section.comments[key])
                return output
            else:
                output = []
                output.append(Struct(section[key], comments=section.comments[key]))
                # we know that there exist a key with _1 suffix
                key = "%s_1" % key
                while 1:
                    if not section.has_key(key):
                        # we hit non-existant key
                        break

                    output.append(Struct(section[key], comments=section.comments[key]))
                    # increment the number
                    (string, num) = key.split("_")
                    key = "%s_%s" % (string, int(num) + 1)

                return output

        else:
            raise IniError("Key '%s' does not exist")

    def save(self):
        #FIXME: Do validation before writing.
        self.config.write()

def main():
    ini = SecurityINI("test.ini")

    entry = ini.getEntry("in bugzilla not fixed", "kernel")
    print entry

    if len(entry) > 1:
        for i in entry:
            print "%s. Comments: %s" % (i, i.comments)
    else:
        entry = entry[0]
        print "%s. Comments: %s" % (entry, entry.comments)


    #ini.save()

if __name__ == '__main__':
    main()
