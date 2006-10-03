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
    return "".join(formatBlock(s))

def escapeHTML(s):
  s2 = s.replace('&', '&amp;')
  list = {
          '"': '&quot;',
          "'": '&apos;',
          '<': '&lt;',
          '>': '&gt;'
          }
  for f, t in list.items():
    s2 = s2.replace(f, t)
  return s2

def formatBlock(s):
    s = s.replace("\r", "")
    source = [i.strip("\n") for i in s.split("\n\n") if i]
    new = []
    links = []

    for block in source:
        # Titles
        m = re.findall("^(.*)\n=+$", block)
        if m:
            new.append("<h3>%s</h3>" % escapeHTML(m[0]))
            continue
        # Subtitles
        m = re.findall("^(.*)\n\-+$", block)
        if m:
            new.append("<h4>%s</h4>" % escapeHTML(m[0]))
            continue
        # Blockquotes - style 1
        if block[0] == " ":
            f = re.findall("\s+(.*)", block)
            nf = [escapeHTML(i) for i in f]
            new.append("<blockquote><p>%s</p></blockquote>" % "<br/>".join(nf))
            continue
        # Blockquotes - style 2
        if block[0] == ">":
            f = re.findall("> (.*)", block)
            nf = [escapeHTML(i) for i in f]
            new.append("<blockquote><p>%s</p></blockquote>" % "<br/>".join(nf))
            continue
        # Code
        if block[:3] == "::\n":
            m = escapeHTML(block[3:])
            new.append("<pre class=\"code\"><code>%s</code></pre>" % m)
            continue
        # RAW Data
        if block[:6] == ":raw:\n":
            m = escapeHTML(block[6:])
            new.append("<pre>%s</pre>" % m)
            continue
        # Unordered list
        if block[0] in ["*", "#"]:
            new.append(formatList(block))
            continue
        # Reference
        m = re.match("\[[0-9]+\] (.+) <.+>", block)
        if m:
            f = re.findall("\[([0-9]+)\] (.+) <(.*)>", block)
            ref = "[%s] %s &lt;<a href=\"%s\">%s</a>&gt;"
            for l in f:
                nl = [escapeHTML(i) for i in l]
                links.append(ref % (nl[0], nl[1], nl[2], nl[2]))
            continue
        # Paragraph
        m = escapeHTML(block)
        new.append("<p>%s</p>" % m)

    if len(links): 
        new.append("<h3>Referanslar</h3>")
        new.append("<p>%s</p>" % "<br/>".join(links))

    return new

def formatList(s):
    t = s.strip()

    if t[0] == "*":
        tag = "ul"
    else:
        tag = "ol"

    r = "<%s>" % tag
    r += formatList_r("\n" + t)
    r += "</%s>" % tag

    return r

def formatList_r(s, d=0):
    r = ""
    t = re.sub("\n\s+([^\*\s#].+)", "<br>\\1", s)
    list = [i.strip() for i in re.split("\n\s{%d}[\*#]" % d, t) if i.strip()]
    for i in list:
        tnl = i.split("\n")
        r += "<li>%s" % tnl[0]
        if len(tnl) > 1:
            if tnl[1].strip()[0] == "*":
                r += "<ul>"
            else:
                r += "<ol>"
            r += formatList_r("\n" + "\n".join(tnl[1:]), d+2)
            if tnl[1].strip()[0] == "*":
                r += "</ul>"
            else:
                r += "</ol>"
        r += "</li>"
    return r
