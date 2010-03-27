#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from configobj import ConfigObj

class IniError(Exception):
    pass

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

    def addEntry(self, section, key, data, comments=[""]):
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

        # if comments is not array, make it array and also strip \n
        if not isinstance(comments, list):
            print "it is not a string"
            if comments.find("\n") > -1:
                comments = comments.split("\n")
            else:
                comments = [comments]

        # control the section first.
        if not self.config.has_key(section):
            raise IniError('Section "%s" does not exist' % section)

        section = self.config[section]

        # handle individual keys first.
        if not section.has_key(key):
            section[key] = data

            # comment dict's first element should be '', control it. We do it
            if comments[0] != '':
                comments.insert(0, '')

            section.comments[key] = comments
        else:
            # now we are dealing with multiple keys. Iterate 
            print "heh"

    def save(self):
        #FIXME: Do validation before writing.
        self.config.write()

def main():
    ini = SecurityINI("test.ini")
    ini.addEntry("in bugzilla not fixed", "amarok", "1123: medium: qa4",
    "#xmlrpc error")

    ini.save()

if __name__ == '__main__':
    main()
