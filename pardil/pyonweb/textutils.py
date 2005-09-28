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
            body.append("<ul>%s</ul>" % formatList(block))
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

def formatList(s):
    depth = 0
    last = [0]
    source = s.strip("\n").split("\n")
    list = []

    for line in source:
        m = re.findall("(\s*)(\*?) (.*)", line)[0]
        if m[1]:
            if len(m[0]) > last[-1]:
                depth += 1
                last.append(len(m[0]))
            elif len(m[0]) < last[-1]:
                while len(m[0]) != last[-1]:
                    depth -= 1
                    last.pop()
            list.append([depth, m[2]])
        else:
            list[-1][1] += " " + m[2]

    new = ""
    for i in range(len(list)):
        ul = 0
        new += "<li>%s" % (list[i][1])
        if i + 1 < len(list) and list[i][0] < list[i+1][0]:
            new += "<ul>"
            ul = 1
        elif i + 1 < len(list) and list[i][0] > list[i+1][0]:
            for j in range(list[i][0] - list[i+1][0]):
                new += "</li>"
                new += "</ul>"
        if not ul:
            new += "</li>"

    if list[-1][0]:
        new += "</ul></li>" * list[-1][0]

    return new
