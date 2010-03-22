#!/usr/bin/python
# -*- coding: utf-8 -*-

import piksemel
from bugspy.error import ParseError, BugzillaError

class BugStruct(object):
    """A container which can be accessed like class objects

    f = BugStruct(foo="bar", baz="heh", bug=BugStruct("id": 1))
    f.set("comment", "foobar")

    print f.foo
    print f.bug.id
    print f.comment

    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __str__(self):
        # if we are parsing bugzilla data, return bug information
        if self.has("error"):
            if self.error:
                return "<BugStruct: Error: %s>" % self.error
            else:
                return "<BugStruct: %s>" % self.short_desc
        # we are not using it to represent bug parsing. It is in normal use mode now
        else:
            return "<BugStruct: %s>" % self.__dict__

    def set(self, key, arg):
        self.__dict__.update({key: arg})

    def has(self, key):
        if self.__dict__.has_key(key):
            return True
        else:
            return False

class BugParser:
    """Parses xmldata and represents it like class objects"""

    def parse(self, data=None):
        """Parses the data and returns dictionary which can be accessed like class objects.

        It contains all of the information returned from bugzilla. Parser assigns exactly the same tag in XML as keywords. E.g: bugzilla returns these:

              <cclist_accessible>1</cclist_accessible>
              <classification_id>1</classification_id>
              <classification>Unclassified</classification>
              <product>Güvenlik / Security</product>
              <component>guvenlik/security</component>

        These can be accessed via;

            bugparser = BugParser()
            bug = bugparser.parse(data)

            print bug.product
            print bug.component
            print bug.classfication_id

        To get comments:

            for comment in bug.comments:
                print comment.name, comment.time, comment.email, comment.text

        To get CC List:

            for cc in bug.cc:
                print cc.email

        Args:
            data: XML data got from bugzilla to parse

        Returns:
            BugStruct object.

        Raises:
            ParseError: XML data is not supplied.
            BugzillaError: Bugzilla error returned from the site.
        """

        if not data:
            raise ParseError("XML Data is not supplied")

        xml = piksemel.parseString(data)
        bug = xml.getTag("bug")

        # if <bug> has attribute error, we should return error.
        error_msg = bug.getAttribute("error")
        if error_msg:
            return BugStruct(error=error_msg)

        struct = BugStruct()
        struct.set("error", False)

        for i in bug.tags():
            # append all the tags except for "cc" and "long_desc", these will need special care.
            tagName = i.name()
            if tagName == "cc" or tagName == "long_desc":
                continue

            struct.set(tagName, bug.getTag(tagName).firstChild().data())

        assigned_to_name = bug.getTag("assigned_to").getAttribute("name")
        reporter_name = bug.getTag("reporter").getAttribute("name")

        # initial assigned_to and reporter contains e-mail addresses
        struct.assigned_to = BugStruct(name=assigned_to_name, email=struct.assigned_to)
        struct.reporter = BugStruct(name=reporter_name, email=struct.reporter)

        # feed comments
        struct.set("comments", [])
        for comment in bug.tags("long_desc"):
            c_name = comment.getTag("who").getAttribute("name")
            c_email = comment.getTagData("who")
            c_time = comment.getTagData("bug_when")
            c_text = comment.getTagData("thetext")

            struct.comments.append(BugStruct(name=c_name, email=c_email, time=c_time, text=c_text))

        # feed cc
        struct.set("cc", [])
        for cc in bug.tags("cc"):
            cc_email = cc.firstChild().data()

            struct.cc.append(BugStruct(email=cc_email))

        return struct

if __name__ == '__main__':
    data = open("/tmp/bug.xml", "r").read()

    bugparser = BugParser()
    bug = bugparser.parse(data)

    for comment in bug.comments:
        print "%s (%s) - %s\n%s\n-------------------\n" % (comment.name, comment.email, comment.time, comment.text)

    for cc in bug.cc:
        print cc.email
