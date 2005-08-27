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
# XmlFile is a halper module for accessing XML files using
# xml.dom.minidom.
#
# XmlFile class that further abstracts a dom object using the
# high-level dom functions provided in xml module (and sorely lacking
# in xml.dom :( )
#
# method names are mixedCase for compatibility with minidom,
# an old library

# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr

import xml.dom.minidom as mdom
from xml.parsers.expat import ExpatError
import codecs

from xmlext import *

import pisi

class Error(pisi.Error):
    pass

import types

mandatory, optional = range(2)

class autoxml(type):

    def __init__(cls, name, bases, dict):

        # add XmlFile as one of the superclasses
        bases = list(bases)
        if not XmlFile in bases:
            bases.append(XmlFile)

        # standard initialization
        super(autoxml, cls).__init__(name, bases, dict)

        # initialize class attribute __xml_tags
        setattr(cls, '__xml_tags', [])

        # find variables that start with x_
        for var in dict:
            if var.startswith('t_'):
                print 'xml tag', var
                autoxml.gen_tag(cls, var[2:])

    def gen_tag(cls, tag):
        # generate readers and writers for the tag
        val = getattr(cls, 't_' + tag)
        tag_type = val[0]
        if type(tag_type) == type(type):
            if val[0] == types.IntType:
                autoxml.gen_int_tag(cls, tag, val)
    #gen_tag = staticmethod(gen_tag)

    def mixed_case(cls, identifier):
        identifier_p = identifier[0].lower() + identifier[1:]
        return identifier_p

    def gen_int_tag(cls, tag, val):
        print tag, val
        name = cls.mixed_case(tag)
        def read_int(self):
            self.name = getNodeText(getNode(node, tag))
        setattr(cls, 'decode' + tag, read_int)

class XmlFile(object):
    """A class for retrieving information from an XML file"""

    def __init__(self, rootTag):
        self.rootTag = rootTag
        self.newDOM()

    def newDOM(self):
        """clear DOM"""
        impl = mdom.getDOMImplementation()
        self.dom = impl.createDocument(None, self.rootTag, None)

    def unlink(self):
        """deallocate DOM structure"""
        self.dom.unlink()

    def readxml(self, fileName):
        try:
            self.dom = mdom.parse(fileName)
        except ExpatError, inst:
            raise XmlError("File '%s' has invalid XML: %s\n" % (fileName, str(inst)))

    def writexml(self, fileName):
        f = codecs.open(fileName,'w', "utf-8")
        f.write(self.dom.toprettyxml())
        f.close()

    def verifyRootTag(self):
        if self.dom.documentElement.tagName != self.rootTag:
            raise XmlError("Root tagname not " + self.rootTag + " as expected")

    # construction helpers

    def newNode(self, tag):
        return self.dom.createElement(tag)

    def newTextNode(self, text):
        return self.dom.createTextNode(text)

    def newAttribute(self, name):
        return self.dom.createAttribute(name)

    # read helpers

    def getNode(self, tagPath):
        """returns the *first* matching node for given tag path."""
        self.verifyRootTag()
        return getNode(self.dom.documentElement, tagPath)

    def getNodeText(self, tagPath):
        """returns the text of *first* matching node for given tag path."""
        node = self.getNode(tagPath)
        if not node:
            return None
        return getNodeText(node)

    def getAllNodes(self, tagPath):
        """returns all nodes matching a given tag path."""
        self.verifyRootTag()
        return getAllNodes(self.dom.documentElement, tagPath)

    def getChildren(self, tagpath):
        """ returns the children of the given path"""
        node = self.getNode(tagpath)
        return node.childNodes

    # get only elements of a given type
    #FIXME:  this doesn't work
    def getChildrenWithType(self, tagpath, type):
        """ returns the children of the given path, only with given type """
        node = self.getNode(tagpath)
        return filter(lambda x:x.nodeType == type, node.childNodes)

    # get only child elements
    def getChildElts(self, tagpath):
        """ returns the children of the given path, only with given type """
        node = self.getNode(tagpath)
        try:
            return filter(lambda x:x.nodeType == x.ELEMENT_NODE, node.childNodes)
        except AttributeError:
            return None

    # write helpers

    def addNode(self, tagPath, newnode = None):
        self.verifyRootTag()
        return addNode(self.dom, self.dom.documentElement, tagPath,
                       newnode)

    def addNodeUnder(self, node, tagPath, newnode = None):
        "this adds the new stuff under node"
        self.verifyRootTag()
        return addNode(self.dom, node, tagPath, newnode)

    def addChild(self, newnode):
        """add a new child node right under root element document"""
        self.dom.documentElement.appendChild(newnode)

    def addText(self, node, text):
        "add text to node"
        node.appendChild(self.newTextNode(text))

    def addTextNode(self, tagPath, text):
        "add a text node with tag path"
        node = self.addNode(tagPath, self.newTextNode(text))
        return node

    def addTextNodeUnder(self, node, tagPath, text):
        "add a text node under given node with tag path (phew)"
        return self.addNodeUnder(node, tagPath, self.newTextNode(text))

        
