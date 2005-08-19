#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import xml.dom.minidom as mdom
from xml.parsers.expat import ExpatError

class XmlError(Exception):
    pass

# flags

ROOT = 1
CLASS = 2
TEXT = 3
LOCALTEXT =4
ATTRIBUTE = 5

SINGLE = 1
MULTIPLE = 2
OPTIONAL = 4

# generic xml utilities

def getText(node):
    try:
        c = node.firstChild.data
    except:
        return None
    # strip whitespaces around
    return c.strip()

def getByName(parent, childName):
    return [x for x in parent.childNodes if x.nodeType == x.ELEMENT_NODE if x.tagName == childName]

def getNodes(parent, path):
    """Retrieve all nodes that match a given tag path."""
    
    if path == "":
        return [ parent ]
    
    tags = path.split('/')
    
    for tag in tags[:-1]:
        parent = getByName(parent, tag)
        if not parent:
            return None
        parent = parent[0]
    
    return getByName(parent, tags[-1])

def getAttribute(node, attrname):
    """get named attribute from DOM node"""
    if not node.hasAttribute(attrname):
        return None
    return node.getAttribute(attrname)


# xml reader

def readXmlFile(inst, fileName, language='en'):
    try:
        doc = mdom.parse(fileName)
    except ExpatError, inst:
        raise XmlError("File '%s' has invalid XML: %s\n" % (fileName, str(inst)))
    errs = []
    readXml(errs, inst, doc.documentElement, language)
    if errs != []:
        e = ""
        for err in errs:
            e += err
        raise XmlError("File '%s' has errors:\n%s" % (fileName, e))
    doc.unlink()

def readXml(errs, inst, parent, language='en'):
    for d in inst.xmldefs:
        if d[0] == ROOT:
            if parent.tagName != d[1]:
                errs.append("Root tag is '%s' instead of '%s'\n" % (parent.tagName, d[1]))
                continue
        
        elif d[0] == CLASS:
            # flags, tag name, class name, instance attribute
            nodes = getNodes(parent, d[2])
            if nodes and len(nodes) > 1 and d[1] & SINGLE:
                errs.append("Tag '%s' must not have more than one '%s' tags\n" % (parent.tagName, d[2]))
                continue
            if d[1] & SINGLE:
                # single case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        errs.append("Tag '%s' must have a '%s' tag\n" % (parent.tagName, d[2]))
                        continue
                    inst.__dict__[d[4]] = None
                else:
                    inst.__dict__[d[4]] = d[3](nodes[0])
                    readXml(errs, inst.__dict__[d[4]], nodes[0], language)
            else:
                # multiple case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        errs.append("Tag '%s' must have at least one '%s' tags\n" % (parent.tagName, d[2]))
                        continue
                    inst.__dict__[d[4]] = []
                else:
                    classes = []
                    for node in nodes:
                        c = d[3](node)
                        readXml(errs, c, node, language)
                        classes.append(c)
                    inst.__dict__[d[4]] = classes
        
        elif d[0] == TEXT:
            # flags, tag name, instance attribute
            inst.__dict__[d[3]] = None
            nodes = getNodes(parent, d[2])
            if nodes and len(nodes) > 1 and d[1] & SINGLE:
                errs.append("Tag '%s' must not have more than one '%s' tags\n" % (parent.tagName, d[2]))
                continue
            if d[1] & SINGLE:
                # single case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        errs.append("Tag '%s' must have a '%s' tag\n" % (parent.tagName, d[2]))
                        continue
                else:
                    c = getText(nodes[0])
                    if not c:
                        errs.append("Tag '%s' should have some text data\n" % nodes[0].tagName)
                        continue
                    inst.__dict__[d[3]] = c
            else:
                # multiple case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        errs.append("Tag '%s' must have at least one '%s' tags\n" % (parent.tagName, d[2]))
                        continue
                else:
                    strs = []
                    for node in nodes:
                        c = getText(node)
                        if not c:
                            errs.append("Tag '%s' should have some text data\n" % node.tagName)
                            break
                        strs.append(c)
                    inst.__dict__[d[3]] = strs
        
        elif d[0] == LOCALTEXT:
            # flags, tag name, instance attribute
            inst.__dict__[d[3]] = None
            nodes = getNodes(parent, d[2])
            if not nodes:
                if not d[1] & OPTIONAL:
                    errs.append("Tag '%s' should have at least one '%s' tag\n" % (parent.tagName, d[2]))
                continue
            locs = {}
            for node in nodes:
                lang = getAttribute(node, "xml:lang")
                c = getText(node)
                if not c:
                    errs.append("Tag '%s' should have some text data\n" % node.tagName)
                    break
                # FIXME: check for dups and 'en'
                if not lang:
                    lang = 'en'
                locs[lang] = c
            # FIXME: return full list too
            L = language
            if not locs.has_key(L):
                L = 'en'
            if not locs.has_key(L):
                errs.append("Tag '%s' should have an English version\n" % d[2])
                continue
            inst.__dict__[d[3]] = locs[L]
        
        elif d[0] == ATTRIBUTE:
            # flags, tag name, attribute name, instance attribute
            if d[2] != "":
                t = getNodes(parent, d[2])
                if not t:
                    errs.append("Tag '%s' must have a '%s' tag\n" % (parent.tagName, d[2]))
                    continue
                if len(t) > 1:
                    errs.append("Tag '%s' must not have more than one '%s' tags\n" % (parent.tagName, d[2]))
                    continue
                t = t[0]
            else:
                t = parent
            attr = getAttribute(t, d[3])
            if not attr:
                if not d[1] & OPTIONAL:
                    errs.append("Tag '%s' must have a '%s' attribute\n" % (t.tagName, d[3]))
                    continue
            inst.__dict__[d[4]] = attr
