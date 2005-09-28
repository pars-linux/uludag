# -*- coding: utf-8 -*-

# Copyright (C) 2005, Bahadır Kandemir
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.

import re

def formatText(s):
    source = [i.strip("\n") for i in s.replace("\r", "").split("\n\n")]
    body = []
    links = []

    for i, block in enumerate(source):
        m = re.match("(.*)\n=+", block)
        if m:
            #print "Block %d is a title" % (i + 1)
            #
            f = re.findall("(.*)\n=+", block)
            body.append("<h3>%s</h3>" % f[0])
            #
            continue
        m = re.match("(\s+.*)+", block)
        if m:
            #print "Block %d is a blockquote" % (i + 1)
            #
            f = re.findall("\s+(.*)", block)
            body.append("<blockquote>%s</blockquote>" % " ".join(f))
            #
            continue
        m = re.match("(> .*)+", block)
        if m:
            #print "Block %d is another blockquote" % (i + 1)
            #
            f = re.findall("> (.*)", block)
            body.append("<blockquote>%s</blockquote>" % " ".join(f))
            #
            continue
        m = re.match("(\* .*)+", block)
        if m:
            #print "Block %d is a list" % (i + 1)
            #
            f = re.findall("\* (.*)", block)
            body.append("<ul><li>%s</li></ul>" % "</li><li>".join(f))
            #
            continue
        m = re.match(":.*\n(\s+.*)+", block)
        if m:
            #print "Block %d is a code" % (i + 1)
            #
            f = re.findall("(\s+.*)", block)
            body.append("<code><pre>%s</pre></code>" % "".join(f)[1:])
            #
            continue
        m = re.match("\[[0-9]+\] (.+) <.+>", block)
        if m:
            #print "Block %d is a link" % (i + 1)
            #
            f = re.findall("\[([0-9]+)\] (.+) <(.*)>", block)
            ref = "[%s] %s &lt;<a href=\"%s\">%s</a>&gt;"
            for l in f:
                links.append(ref % (l[0], l[1], l[2], l[2]))
            #
            continue
        m = re.match("\+\-+.*\-+\+", block)
        if m:
            #print "Block %d is a table" % (i + 1)
            #
            body.append("<pre>%s</pre>" % block)
            #
            continue
        m = re.match(".+", block)
        if m:
            #print "Block %d is a paragraph" % (i + 1)
            #
            body.append("<p>%s</p>" % block)
            #
   
    if len(links): 
        body.append("<h3>Referanslar</h3>")
        body.append("<p>%s</p>" % "<br/>".join(links))

    return "\n".join(body)
