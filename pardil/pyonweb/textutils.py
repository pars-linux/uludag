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

def formatBlock(s):
    s = s.replace("\r", "")
    source = [i for i in s.split("\n\n") if i]
    new = []
    links = []

    for block in source:
        # Titles
        m = re.findall("^(.*)\n=+$", block)
        if m:
            new.append("<h3>%s</h3>" % m[0])
            continue
        # Subtitles
        m = re.findall("^(.*)\n\-+$", block)
        if m:
            new.append("<h4>%s</h4>" % m[0])
            continue
        # Blockquotes - style 1
        if block[0] == " ":
            f = re.findall("\s+(.*)", block)
            new.append("<blockquote><p>%s</p></blockquote>" % "<br/>".join(f))
            continue
        # Blockquotes - style 2
        if block[0] == ">":
            f = re.findall("> (.*)", block)
            new.append("<blockquote><p>%s</p></blockquote>" % "<br/>".join(f))
            continue
        # Code
        if block[:3] == "::\n":
            new.append("<pre><code>%s</code></pre>" % block[3:])
            continue
        # RAW Data
        if block[:6] == ":raw:\n":
            new.append("<pre>%s</pre>" % block[6:])
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
                links.append(ref % (l[0], l[1], l[2], l[2]))
        # Paragraph
        new.append("<p>%s</p>" % block)

    if len(links): 
        new.append("<h3>Referanslar</h3>")
        new.append("<p>%s</p>" % "<br/>".join(links))

    return new

def formatList(s):

    re_spaces = lambda x: len(re.findall("(\s*)([\*|#]?) (.*)", x)[0][0])
    re_content = lambda x: re.findall("(\s*)([\*|#]?) (.*)", x)[0][2]
    re_sign = lambda x: re.findall("(\s*)([\*|#]?) (.*)", x)[0][1]

    s = re.sub("\n\s+([^\*\s#].+)", "<br/>\\1", s)

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

    for i in range(len(lines)):
        m = re_content(lines[i])
        l = re_spaces(lines[i])
        close = 1
        new += "<li>%s" % m
        if i + 1 < len(lines) and re_spaces(lines[i]) < re_spaces(lines[i+1]):
            if re_sign(lines[i+1]) == "*":
                new += "<ul>"
                indent_s.append("*")
            else:
                new += "<ol>"
                indent_s.append("#")
            indent.append(re_spaces(lines[i+1]))
            close = 0

        if close:
            new += "</li>"
        
        if i + 1 < len(lines) and re_spaces(lines[i]) > re_spaces(lines[i+1]):
            while re_spaces(lines[i+1]) < indent[-1]:
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
