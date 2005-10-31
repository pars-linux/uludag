# Copyright (C) 2005, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import unittest
import os
import xml.dom.minidom as mdom
from xml.parsers.expat import ExpatError
import types

import pisi
import pisi.api
from pisi import xmlfile
import pisi.context as ctx
import pisi.util as util
from pisi.xmlext import *

import testcase

class AutoXmlTestCase(testcase.TestCase):

    def setUp(self):
        testcase.TestCase.setUp(self, database=False)

        class OtherInfo:
            __metaclass__ = xmlfile.autoxml
            t_BirthDate = [types.StringType, xmlfile.mandatory]
            t_Interest = [types.StringType, xmlfile.optional]
            t_CodesWith = [ [types.StringType], xmlfile.optional, 'CodesWith/Person']
        
        class A(xmlfile.XmlFile):
            __metaclass__ = xmlfile.autoxml
            t_Name = [types.StringType, xmlfile.mandatory]
            t_Description = [xmlfile.LocalText, xmlfile.mandatory]
            t_Number = [types.IntType, xmlfile.optional]
            t_Email = [types.StringType, xmlfile.optional]
            a_href = [types.StringType, xmlfile.mandatory]
            t_Projects = [ [types.StringType], xmlfile.mandatory, 'Project']
            t_OtherInfo = [ OtherInfo, xmlfile.optional ]
            s_Comment = [ xmlfile.Text, xmlfile.mandatory]
        
        self.A = A

    def testDeclaration(self):
        self.assertEqual(len(self.A.decoders), 8) # how many fields in A?
        self.assert_(hasattr(self.A, 'encode'))

    def testReadWrite(self):
        a = self.A()
        
        # test initializer
        self.assertEqual(a.href, None)
        
        # test decode
        dom = mdom.parse('tests/a.xml')
        node = getNode(dom, 'A')
        errs = []
        print 'errs', errs
        a.decode(node, errs)
        self.assert_(a.href.startswith('http'))
        self.assertEqual(a.number, 868)
        self.assertEqual(a.name, 'Eray Ozkural')
        self.assertEqual(len(a.projects), 3)
        self.assertEqual(len(a.otherInfo.codesWith), 4)

        #string = a.format(errs)
        #print '*', string
        a.print_text()
        #self.assert_(string.startswith('Name'))
        xml = xmlfile.XmlFile('A')
        xml.newDOM()
        errs2 = []
        a.encode(xml, xml.rootNode(), errs2)
        print 'errs2', errs2
        xml.writexml('/tmp/a.xml')
        print '/tmp/a.xml written'
        xml = xmlfile.XmlFile('A')
        
    def testCopy(self):
        a2 = self.A()
        a2.name = "Baris Metin"
        a2.email = "baris@uludag.org.tr"
        a2.href = 'http://cekirdek.uludag.org.tr/~baris'
        a2.projects = [ 'pisi', 'tasma', 'plasma' ]
        errs3 = []
        xml = xmlfile.XmlFile('A')
        a2.encode(xml, xml.rootNode(), errs3)
        print 'errs3', errs3
        xml.writexml('/tmp/a2.xml')
        print a2.check()
        #string = a2.format(errs3)

suite = unittest.makeSuite(AutoXmlTestCase)
