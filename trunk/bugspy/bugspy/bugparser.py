#!/usr/bin/python
# -*- coding: utf-8 -*-

import piksemel
from bugspy.error import ParseError

class Bugdict(dict):
    """A container which can be accessed like class objects

    f = Bugdict({"foo": "bar",
        "baz": "eheh",
        "dummy": Bugdict({"foo": 1, "bar": 2}),
        })

    print f.foo
    print f.dummy.foo

    """

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

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

        Raises:
            ParseError: XML data is not supplied.
        """

        if not data:
            raise ParseError("XML Data is not supplied")

        output = {}

        xml = piksemel.parseString(data)
        bug = xml.getTag("bug")

        # output["creation_ts"] = bug.getTagData("creation_ts")

        for i in bug.tags():
            # append all the tags except for "cc" and "long_desc", these will need special care.
            tagName = i.name()
            if tagName == "cc" or tagName == "long_desc":
                continue

            output[tagName] = bug.getTag(tagName).firstChild().data()

        assigned_to_name = bug.getTag("assigned_to").getAttribute("name")
        reporter_name = bug.getTag("reporter").getAttribute("name")

        # initial assigned_to and reporter contains e-mail addresses
        output["assigned_to"] = Bugdict({"name": assigned_to_name, "email": output["assigned_to"]})
        output["reporter"] = Bugdict({"name": reporter_name, "email": output["reporter"]})

        # feed comments
        # I need to store the array within tmp variable. Somehow, I cannot use output["comments"] = []
        comment_tmp = []
        for comment in bug.tags("long_desc"):
            name = comment.getTag("who").getAttribute("name")
            email = comment.getTagData("who")
            time = comment.getTagData("bug_when")
            text = comment.getTagData("thetext")


            comment_tmp.append(Bugdict({"name": name,
                                        "email": email,
                                        "time": time,
                                        "text": text}))


        output["comments"] = comment_tmp

        # feed cc
        cc_tmp = []
        for cc in bug.tags("cc"):
            email = cc.firstChild().data()
            cc_tmp.append(Bugdict({"email": email}))

        output["cc"] = cc_tmp

        return Bugdict(output)

if __name__ == '__main__':
    data = open("/tmp/bug.xml", "r").read()

    bugparser = BugParser()
    bug = bugparser.parse(data)

    for comment in bug.comments:
        print "%s (%s) - %s\n%s\n-------------------\n" % (comment.name, comment.email, comment.time, comment.text)

    for cc in bug.cc:
        print cc.email
