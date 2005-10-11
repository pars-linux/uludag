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
    source = [i for i in s.split("\n\n") if i]
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
            new.append("<pre><code>%s</code></pre>" % m)
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
    s = re.sub("\n\s+([^\*\s#].+)", "<<BRK>>\\1", s)

    lines = s.split("\n")

    indent = [0]
    indent_s = []

    new = ""
    if s[0] == "*":
        new += "<ul>"
        indent_s.append("*")
    else:
        new += "<ol>"
        indent_s.append("#")

    regex = lambda x: re.findall("(\s*)([\*|#]?) (.*)", x)[0]

    for i in range(len(lines)):
        r1 = regex(lines[i])
        close = 1

        # Iğrencim
        new += "<li>%s" % escapeHTML(r1[2]).replace("&lt;&lt;BRK&gt;gt;", "<br/>")

        if i + 1 < len(lines):
            r2 = regex(lines[i+1])

            if len(r1[0]) < len(r2[0]):
                if r2[1] == "*":
                    new += "<ul>"
                    indent_s.append("*")
                else:
                    new += "<ol>"
                    indent_s.append("#")
                indent.append(len(r2[0]))
                close = 0

        if close:
            new += "</li>"
        
        if i + 1 < len(lines):
            if len(r1[0]) > len(r2[0]):
                while len(r2[0]) < indent[-1]:
                    indent.pop()
                    if indent_s.pop() == "*":
                        new += "</ul></li>"
                    else:
                        new += "</ol></li>"

    for i in range(len(indent) - 1):
        if indent_s.pop() == "*":
            new += "</ul></li>"
        else:
            new += "</ol></li>"

    if indent_s.pop() == "*":
        new += "</ul>"
    else:
        new += "</ol>"

    return new
