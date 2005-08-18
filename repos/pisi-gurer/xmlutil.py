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
ATTRIBUTE = 4

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
    return c.split()[0]

def getByName(parent, childName):
    return [x for x in parent.childNodes if x.nodeType == x.ELEMENT_NODE if x.tagName == childName]

def getNodes(parent, path):
    """Retrieve all nodes that match a given tag path."""
    
    if path == "":
        return [ parent ]
    
    tags = path.split('/')
    
    for tag in tags[:-1]:
        parent = getByName(parent, tag)[0]
        if not parent:
            return None
    
    return getByName(parent, tags[-1])

def getAttribute(node, attrname):
    """get named attribute from DOM node"""
    if not node.hasAttribute(attrname):
        return None
    return node.getAttribute(attrname)


# xml reader

def readXmlFile(inst, fileName):
    try:
        doc = mdom.parse(fileName)
    except ExpatError, inst:
        raise XmlError("File '%s' has invalid XML: %s" % (fileName, str(inst)))
    readXml(inst, fileName, doc.documentElement)


def readXml(inst, fileName, parent):
    for d in inst.xmldefs:
        if d[0] == ROOT:
            if parent.tagName != d[1]:
                raise XmlError("File '%s' root tag is '%s' instead of '%s'", fileName,
                                        parent.tagName, d[1])
        
        elif d[0] == CLASS:
            # flags, tag name, class name, instance attribute
            nodes = getNodes(parent, d[2])
            if len(nodes) > 1 and d[1] & SINGLE:
                raise XmlError("File '%s' tag '%s' must not have more than one '%s' tags" % (fileName, parent.tagName, d[2]))
            if d[1] & SINGLE:
                # single case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        raise XmlError("File '%s' tag '%s' must have a '%s' tag" % (fileName, parent.tagName, d[2]))
                else:
                    inst.__dict__[d[4]] = d[3](nodes[0])
                    readXml(inst.__dict__[d[4]], fileName, nodes[0])
            else:
                # multiple case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        raise XmlError("File '%s' tag '%s' must have at least one '%s' tags" % (fileName, parent.tagName, d[2]))
                else:
                    classes = []
                    for node in nodes:
                        c = d[3](node)
                        readXml(c, fileName, node)
                        classes.append(c)
                    inst.__dict__[d[4]] = classes
        
        elif d[0] == TEXT:
            # flags, tag name, instance attribute
            nodes = getNodes(parent, d[2])
            if len(nodes) > 1 and d[1] & SINGLE:
                raise XmlError("File '%s' tag '%s' must not have more than one '%s' tags" % (fileName, parent.tagName, d[2]))
            if d[1] & SINGLE:
                # single case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        raise XmlError("File '%s' tag '%s' must have a '%s' tag" % (fileName, parent.tagName, d[2]))
                else:
                    c = getText(nodes[0])
                    if not c:
                        raise XmlError("File '%s' tag '%s' should have some text data" % (fileName, d[2]))
                    inst.__dict__[d[3]] = c
            else:
                # multiple case
                if not nodes:
                    if not d[1] & OPTIONAL:
                        raise XmlError("File '%s' tag '%s' must have at least one '%s' tags" % (fileName, parent.tagName, d[2]))
                else:
                    strs = []
                    for node in nodes:
                        c = getText(node)
                        if not c:
                            raise XmlError("File '%s' tag '%s' should have some text data" % (fileName, d[2]))
                        strs.append(c)
                    inst.__dict__[d[3]] = strs
        
        elif d[0] == ATTRIBUTE:
            # flags, tag name, attribute name, instance attribute
            if d[2] != "":
                t = getNodes(parent, d[2])
                if not t:
                    raise XmlError("File '%s' tag '%s' must have a '%s' tag" % (fileName, parent.tagName, d[2]))
                if len(t) > 1:
                    raise XmlError("File '%s' tag '%s' must not have more than one '%s' tags" % (fileName, parent.tagName, d[2]))
                t = t[0]
            else:
                t = parent
            attr = getAttribute(t, d[3])
            if not attr:
                if not d[1] & OPTIONAL:
                    raise XmlError("File '%s' tag '%s' must have a '%s' attribute" % (fileName, t[0].tagName, d[3]))
            inst.__dict__[d[4]] = attr
