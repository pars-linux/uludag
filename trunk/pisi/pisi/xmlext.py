# -*- coding: utf-8 -*-
#
# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

# some helper functions for using minidom
# works well enough for now... :/

# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr


class XmlError(Exception):
    pass

def getNodeAttribute(node, attrname):
    """get named attribute from DOM node"""
    for i in range(node.attributes.length):
        attr = node.attributes.item(i)
        if attr.name == attrname:
            return attr.childNodes[0].data
    return None

def getNodeText(node, tagpath = ""):
    """get the first child and expect it to be text!"""
    if tagpath!="":
        node = getNode(node, tagpath)
    try:
        child = node.childNodes[0]
    except IndexError:
        return None
    except AttributeError: # no node by that name
        return None
    if child.nodeType == child.TEXT_NODE:
        # in any case, strip whitespaces...
        return child.data.strip()
    else:
        raise XmlError("getNodeText: Expected text node, got something else!")

def getChildText(node_s, tagpath):
    """get the text of a child at the end of a tag path"""
    node = getNode(node_s, tagpath)
    if not node:
        return None
    return getNodeText(node)

def getChildElts(node):
    """get only child elements"""
    return filter(lambda x:x.nodeType == x.ELEMENT_NODE, node.childNodes)

def getNode(node, tagpath):
    """returns the *first* matching node for given tag path."""

    assert type(tagpath)==str
    tags = tagpath.split('/')
    assert len(tags)>0

    # iterative code to search for the path
        
    # get DOM for top node
    nodeList = node.getElementsByTagName(tags[0])
    if len(nodeList) == 0:
        return None                 # not found

    node = nodeList[0]              # discard other matches
    for tag in tags[1:]:
        nodeList = node.getElementsByTagName(tag)
        if len(nodeList) == 0:
            return None
        else:
            node = nodeList[0]

    return node

def getAllNodes(node, tagPath):
    """retrieve all nodes that match a given tag path."""

    tags = tagPath.split('/')

    if len(tags) == 0:
        return []

    nodeList = node.getElementsByTagName(tags[0])
    if len(nodeList) == 0:
        return []

    for tag in tags[1:]:
        results = map(lambda x: x.getElementsByTagName(tag),nodeList)
        nodeList = []
        for x in results:
            nodeList.extend(x)
            pass # emacs indentation error, keep it here

        if len(nodeList) == 0:
            return []

    return nodeList


def createTagPath(dom, node, tags):
    """create new child at the end of a tag chain starting from node
    no matter what"""
    if len(tags)==0:
        return node
    for tag in tags:
        node = node.appendChild(dom.createElement(tag))
    return node

def addTagPath(dom, node, tags, newnode=None):
    """add newnode at the end of a tag chain, smart one"""
    node = createTagPath(dom, node, tags)
    if newnode:                     # node to add specified
        node.appendChild(newnode)
    return node    

def addNode(dom, node, tagpath, newnode = None):
    """add a new node at the end of the tree"""

    assert type(tagpath)==str
    tags = []
    if tagpath != "":
        tags = tagpath.split('/')           # tag chain
    assert len(tags)>0                  # we want a chain

    # iterative code to search for the path
        
    # get DOM for top node
    nodeList = node.getElementsByTagName(tags[0])
    
    if len(nodeList) == 0:
        return addTagPath(dom, node, tags, newnode)
    
    node = nodeList[len(nodeList)-1]              # discard other matches
    tags.pop(0)
    while len(tags)>0:
        tag = tags.pop(0)
        nodeList = node.getElementsByTagName(tag)
        if len(nodeList) == 0:          # couldn't find
            tags.insert(0, tag)         # put it back in
            return addTagPath(dom, node, tags, newnode)
        else:
            node = nodeList[len(nodeList)-1]
    else:
        # had only one tag..
        return addTagPath(dom, node, tags, newnode)

    return node
