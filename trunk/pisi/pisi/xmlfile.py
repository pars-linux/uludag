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
#
# Authors:  Eray Ozkural <eray@uludag.org.tr>
#           Gurer Ozen <gurer@uludag.org.tr>
#           Baris Metin <baris@uludag.org.tr>


"""
 xmlfile is a helper module for accessing XML files using
 xml.dom.minidom.

 XmlFile class further abstracts a dom object using the
 high-level dom functions provided in xmlext module (and sorely lacking
 in xml.dom :( )

 autoxml is a metaclass for automatic XML translation, using
 a miniature type system. (w00t!) This is based on an excellent
 high-level XML processing prototype that Gurer prepared.

 Method names are mixedCase for compatibility with minidom,
 an old library. 
"""

# System
import xml.dom.minidom as mdom
from xml.parsers.expat import ExpatError
import codecs
import types

# PiSi
import pisi
from pisi.xmlext import *
import pisi.context as ctx


class Error(pisi.Error):
    pass

    
mandatory, optional = range(2) # poor man's enum

# basic types

Text = types.StringType
Integer = types.IntType

class LocalText(object):
    """Handles XML tags/attributes with localized text"""

    def __init__():
        locs = {}
        
    def decode(nodes, req):
        # flags, tag name, instance attribute
        if not nodes:
            if req == mandatory:
                pass
                #errs.append("Tag '%s' should have at least one '%s' tag\n" % (parent.tagName, d[2]))
        else:
            for node in nodes:
                lang = getAttribute(node, "xml:lang")
                c = getText(node)
                if not c:
                    #errs.append("Tag '%s' should have some text data\n" % node.tagName)
                    break
                # FIXME: check for dups and 'en'
                if not lang:
                    lang = 'en'
                self.locs[lang] = c
            # FIXME: return full list too
            L = language
            if not locs.has_key(L):
                L = 'en'
            if not locs.has_key(L):
                #errs.append("Tag '%s' should have an English version\n" % d[2])
                return ""
            return locs[L]

            
class autoxml(type):
    """High-level automatic XML transformation interface for xmlfile.
    The idea is to declare a class for each XML tag. Inside the
    class the tags and attributes nested in the tag are further
    elaborated. A simple example follows:

    class Employee:
         __metaclass__ = autoxml
         t_Name = [xmlfile.Text, xmlfile.mandatory]
         a_Type = [xmlfile.Integer, xmlfile.optional]
    
    This class defines a tag and an attribute nested in Employee 
    class. Name is a string and type is an integer, called basic
    types.
    While the tag is mandatory, the attribute may be left out.
    
    Other basic types supported are: xmlfile.Float, xmlfile.Double
    and (not implemented yet): xmlfile.Binary

    By default, the class name is taken as the corresponding tag,
    which may be overridden by defining a tag attribute. Thus, 
    the same tag may also be written as:

    class EmployeeXML:
        ...
        tag = 'Employee'
        ...

    In addition to basic types, we allow for two kinds of complex
    types: class types and list types.

    A declared class can be nested in another class as follows

    class Position:
         __metaclass__ = autoxml
         t_Name = [xmlfile.Text, xmlfile.mandatory]
         t_Description = [xmlfile.Text, xmlfile.optional]

    which we can add to our Employee class.

    class Employee:
         __metaclass__ = autoxml
         t_Name = [xmlfile.Text, xmlfile.mandatory]
         a_Type = [xmlfile.Integer, xmlfile.optional]
         t_Position = [Position, xmlfile.mandatory]

    Note some unfortunate redundancy here with Position; this is
    justified by the implementation (kidding). Still, you might
    want to assign a different name than the class name that
    goes in there, which may be fully qualified.

    There is more! Suppose we want to define a company, with
    of course many employees.

    class Company:
        __metaclass__ = autoxml
        t_Employees = [ [Employee], xmlfile.mandatory]

    Logically, inside the Company tag, we will have several Employee
    tags, which are inserted to the Employees instance variable of
    Company in order of appearance.
    The mandatory flag here asserts that at least one such record
    is to be found.

    It is also possible to change the XML path we expect the tag in,
    just like with any other tag.

         t_Employees = [ [Employee], xmlfile.mandatory, 'Employees/Employee']


    You see, it works like magic, when it works of course. All of it
    done without a single brain exploding.
        
    """

    def __init__(cls, name, bases, dict):
        print 'generating class', name

        # add XmlFile as one of the superclasses, we're smart
        bases = list(bases)
        if not XmlFile in bases:
            bases.append(XmlFile)

        # standard initialization
        super(autoxml, cls).__init__(name, bases, dict)

        #TODO: initialize class attribute __xml_tags
        #setattr(cls, 'xml_variables', [])

        # default class tag is class name
        if not dict.has_key('tag'): 
            cls.tag = name

        # generate helper routines, for each XML component
        inits = []
        decoders = []
        encoders = []
        formatters = []
        for var in dict:
            if var.startswith('t_') or var.startswith('a_'):
                name = var[2:]
                print 'generating member', name
                if var.startswith('a_'):
                    x = autoxml.gen_attr_member(cls, name)
                elif var.startswith('t_'):
                    x = autoxml.gen_tag_member(cls, name)
                (init, decoder, encoder, formatter) = x
                inits.append(init)
                decoders.append(decoder)
                encoders.append(encoder)
                formatters.append(formatter)

        # generate top-level helper functions
        cls.initializers = inits
        def initialize(self):
            for init in self.__class__.initializers:
                init(self)
        cls.__init__ = initialize

        cls.decoders = decoders
        def decode(self, node):
            for decoder in self.__class__.decoders:
                decoder(self, node)
        cls.decode = decode

        cls.encoders = encoders
        def encode(self, xml):
            for encoder in self.__class__.encoders:
                encoder(self, xml)
        cls.encode = encode

        cls.formatters = formatters
        def format(self):
            string = ''
            for formatter in self.__class__.formatters:
                string += formatter(self)
            return string
        cls.format = format
        if not dict.has_key('__str__'):
            cls.__str__ = format

    def gen_attr_member(cls, attr):
        """generate readers and writers for an attribute member"""
        print 'attr:', attr
        spec = getattr(cls, 'a_' + attr)
        tag_type = spec[0]
        assert type(tag_type) == type(type)
        def readtext(node, attr):
            return getNodeAttribute(node, attr)
        def writetext(xml, node, attr, value):
            node.setAttribute(attr, value)
        anonfuns = cls.gen_anon_basic(attr, spec, readtext, writetext)
        return cls.gen_named_comp(attr, spec, anonfuns)

    def gen_tag_member(cls, tag):
        """generate helper funs for tag member of class"""
        spec = getattr(cls, 't_' + tag)
        def readtext(node, tag):
            return getNodeText(getNode(node, tag))
        def writetext(xml, node, tag, value):
            xml.addTextNodeUnder(node, tag, value)
        anonfuns = cls.gen_tag(tag, spec, readtext, writetext)
        return cls.gen_named_comp(tag, spec, anonfuns)
                    
    def gen_named_comp(cls, token, spec, anonfuns):
        """generate a named component tag/attr. a decoration of
        anonymous functions that do not bind to variable names"""
        name = cls.mixed_case(token)
        token_type = spec[0]
        req = spec[1]
        (init_a, decode_a, encode_a, format_a) = anonfuns

        def init(self):
            setattr(self, name, init_a())
            
        def decode(self, node):
            setattr(self, name, decode_a(node))
            
        def encode(self, xml):
            if hasattr(self, name):
                value = getattr(self, name)
            else:
                value = None
            encode_a(xml, value)
            
        def format(self):
            if hasattr(self, name):
                value = getattr(self,name)
                return '%s: %s\n' % (token, format_a(value))
            else:
                if req == mandatory:
                    raise Error('Mandatory variable %s not available' % name)
            return ''
            
        return (init, decode, encode, format)

    def gen_tag(cls, tag, spec, readtext, writetext):
        """generate readers and writers for the tag"""
        tag_type = spec[0]
        if type(tag_type) is types.TypeType:
            return cls.gen_anon_basic(tag, spec, readtext, writetext)
        elif type(tag_type) is types.ListType:
            return cls.gen_list_tag(tag, spec)
        elif type(tag_type) is autoxml or type(tag_type) is types.ClassType:
            return cls.gen_class_tag(tag, spec)

    def mixed_case(cls, identifier):
        """helper function to turn token name into mixed case"""
        identifier_p = identifier[0].lower() + identifier[1:]
        return identifier_p

    def parse_spec(cls, token, spec):
        name = cls.mixed_case(token)
        token_type = spec[0]
        req = spec[1]

        if len(spec)>=3:
            path = spec[2]               # an alternative path specified
        else:
            path = token                 # otherwise it's the same name as
                                         # the token
        return name, token_type, req, path

    def gen_anon_basic(cls, token, spec, readtext, writetext):
        """Generate a tag or attribute with one of the basic
        types like integer. This has got to be pretty generic
        so we can invoke it from the complex types such as Class
        and List. The readtext and writetext arguments achieve
        the text input I/O for this datatype."""
        
        name, token_type, req, path = cls.parse_spec(token, spec)
       
        def initialize():
            """default value for all basic types is None"""
            return None

        def decode(node):
            """decode from DOM node, the value, watching the spec"""
            text = readtext(node, token)
            print 'read text ', text
            if text:
                try:
                    value = autoxml.basic_cons_map[token_type](text)
                except Error:
                    raise Error('Type mismatch: read text cannot be decoded')
                return value
            else:
                if req == mandatory:
                    raise Error('Mandatory token %s not available' % token)
                else:
                    return None

        def encode(xml, value):
            """encode given value into xml file"""
            node = xml.newNode(cls.tag)
            if value:
                writetext(xml, node, token, str(value))
            else:
                if req == mandatory:
                    raise Error('Mandatory argument not available')

        def format(value):
            return str(value)

        return initialize, decode, encode, format

    def gen_class_tag(cls, tag, spec):
        """generate a class datatype"""
        name, tag_type, req, path = cls.parse_spec(tag, spec)

        def make_object():
            return tag_type.__new__(tag_type)

        def init():
            return make_object()

        def decode(node):
            node = getNode(node, path)
            if node:
                try:
                    obj = make_object()
                    obj.decode(node)
                    return obj
                except Error:
                    raise Error('Type mismatch: DOM cannot be decoded')
            else:
                if req == mandatory:
                    raise Error('Mandatory argument not available')
                else:
                    return None

        def encode(xml, value):
            pass

        def format(l):
            s = ''
            return s
        
        return (init, decode, encode, format)

    def gen_list_tag(cls, tag, spec):
        """generate a list datatype"""
        name, tag_type, req, path = cls.parse_spec(tag, spec)
        if len(tag_type) != 1:
            raise Error('List type must contain only one element')

        def readtext_item(node, tag):
            return getNodeText(node)
        def writetext_item(xml, node, tag, value):
            xml.addTextNode(node, value)
        x = cls.gen_tag(tag, [tag_type[0], mandatory],
                        readtext_item, writetext_item)
        (init_item, decode_item, encode_item, format_item) = x

        def init():
            return []

        def decode(node):
            l = []
            nodes = getAllNodes(node, path)
            print 'F U', nodes
            if len(nodes) is 0 and req is mandatory:
                raise Error('Mandatory list empty')
            for node in nodes:
                l.append(decode_item(node))
            return l

        def encode(xml, l):
            pass

        def format(l):
            #print 'format:', name
            s = ''
            for ix in range(len(l)):
                s += str(ix+1) + ': ' + format_item(l[ix])
                if ix != len(l)-1:
                    s += ', '
            return s
        
        return (init, decode, encode, format)

    basic_cons_map = {
        types.StringType : str,
        types.IntType : int
        }


class XmlFile(object):
    """A class to help reading and writing an XML file"""

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
            raise Error("File '%s' has invalid XML: %s\n" % (fileName,
                                                             str(inst)))

    def writexml(self, fileName):
        f = codecs.open(fileName,'w', "utf-8")
        f.write(self.dom.toprettyxml())
        f.close()

    def verifyRootTag(self):
        if self.dom.documentElement.tagName != self.rootTag:
            raise Error("Root tagname not " + self.rootTag + " as expected")

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
            return filter(lambda x:x.nodeType == x.ELEMENT_NODE,
                          node.childNodes)
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
