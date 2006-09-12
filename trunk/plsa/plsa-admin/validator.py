#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

import piksemel

class validate_plsa:
    once, one_or_more, optional, optional_once = range(4)

    def __init__(self):
        self.errors = []

    def error(self, node, msg):
        self.errors.append("%s: %s" % (node.name(), msg))

    def check(self, node, childs):
        counts = {}
        for tag in node.tags():
            name = tag.name()
            if childs.has_key(name):
                counts[name] = counts.get(name, 0) + 1
            else:
                self.error(node, "unknown tag <%s>" % name)
        for name in childs:
            mode = childs[name]
            if isinstance(mode, tuple):
                mode = mode[0]
            count = counts.get(name, 0)
            if mode == self.once:
                if count == 0:
                    self.error(node, "missing tag <%s>" % name)
                elif count > 1:
                    self.error(node, "tag <%s> should not appear more than once" % name)
            elif mode == self.one_or_more:
                if count == 0:
                    self.error(node, "tag <%s> should appear at least once" % name)
            elif mode == self.optional_once:
                if count > 1:
                    self.error(node, "optional tag <%s> should not appear more than once" % name)
        # recurse for child funcs
        for name in childs:
            arg = childs[name]
            if isinstance(arg, tuple):
                mode = arg[0]
                func = arg[1]
                if mode == self.once or mode == self.optional_once:
                    tag = node.getTag(name)
                    if tag:
                        func(tag)
                else:
                    for tag in node.tags(name):
                        func(tag)

    def check_attr(self, node, attrs):
        for attr in node.attributes():
            if not attrs.has_key(attr):
                self.error(node, "unknown attribute '%s'" % attr)
        for attr in attrs:
            mode = attrs[attr]
            vals = None
            if isinstance(mode, tuple):
                mode, vals = mode
            val = node.getAttribute(attr)
            if mode == self.once and val == None:
                self.error(node, "missing attribute '%s'" % attr)
            if val and vals and not val in vals:
                self.error(node, "keyword '%s' is not accepted for attribute '%s'" % (val, attr))

    def validate(self, xmlfile):
        try:
            doc = piksemel.parse(xmlfile)
        except piksemel.ParseError:
            self.errors.append("Invalid XML")
            return

        if doc.name() != "PLSA":
            self.error(node, "wrong top level tag")

        self.check(
            doc, {
                "Advisory": (self.once, self.validate_advisory),
            }
        )

        return len(self.errors) == 0

    def validate_advisory(self, node):
        self.check(
            node, {
                 "Title": (self.one_or_more, self.validate_title),
                 "Summary": (self.one_or_more, self.validate_title),
                 "Description": (self.one_or_more, self.validate_title),
                 "ReleaseDate": (self.once, self.validate_releasedate),
                 "Severity": (self.once, self.validate_severity),
                 "Packages": (self.once, self.validate_packages),
                 "References": (self.optional_once, self.validate_references)
            }
        )
        self.check_attr(
            node, {
                 "id": (self.once),
            }
        )

        if not node.getAttribute("id").isdigit():
            self.error(node, "id must be an integer")

    def validate_data(self, node):
        self.check(node, {})
        self.check_attr(node, {})

    def validate_title(self, node):
        self.check(node, {})
        self.check_attr(
            node, {
                 "xml:lang": (self.once),
            }
        )

        islangcode = lambda x: x.isalpha() and len(x) == 2
        if "xml:lang" in node.attributes() and not islangcode(node.getAttribute("xml:lang")):
            self.error(node, "wrong language code")

    def validate_releasedate(self, node):
        self.check(node, {})
        self.check_attr(node, {})

        import re
        isdate = lambda x: re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", x)

        if node.firstChild().type() == piksemel.DATA and not isdate(node.firstChild().data()):
            self.error(node, "wrong date format")

    def validate_severity(self, node):
        self.check(node, {})
        self.check_attr(node, {})

        if node.firstChild().type() == piksemel.DATA and not node.firstChild().data().isdigit():
            self.error(node, "wrong severity number")

    def validate_packages(self, node):
        self.check(
            node, {
                 "Package": (self.one_or_more, self.validate_package),
            }
        )
        self.check_attr(node, {})

    def validate_package(self, node):
        self.check(
            node, {
                 "Name": (self.once, self.validate_data),
                 "Release": (self.optional_once, self.validate_data),
            }
        )
        self.check_attr(node, {})

    def validate_references(self, node):
        self.check(
            node, {
                 "Reference": (self.one_or_more, self.validate_reference),
            }
        )
        self.check_attr(node, {})

    def validate_reference(self, node):
        self.check(
            node, {
                 "Name": (self.once, self.validate_data),
                 "Link": (self.once, self.validate_data),
            }
        )
        self.check_attr(node, {})
