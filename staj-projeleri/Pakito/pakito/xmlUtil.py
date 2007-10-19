# -*- coding: utf-8 -*-

import piksemel
import re

commentString = "XmlUtil"

class XmlUtil:
    """ basic xml parsing class with comment keeping support using piksemel"""
    def __init__(self, xmlFileName):
        self.read(xmlFileName)
        
    def getTagByPath(self, *path):
        """ get tag by path. e.g getTagByPath("Source", "Packager", "Name") give the Name tag """
        node = self.doc
        for tag in path:
            node = node.getTag(tag)
            if node == None:
                return None
        return node
    
    def getTagListByPath(self, *path):
        """ get tag(s) with given name by path, returns a list"""
        lst = []
        node = self.getTagByPath(*path)
        if not node:
            return None
        lst.append(node)
        node = node.nextTag()
        while node:
            if node.name() == path[-1]:
                lst.append(node)
            node = node.nextTag()
        return lst        
    
    def getDataOfTag(self, node):
        """ get data of given node """
        data = node.firstChild()
        while (data.type() != piksemel.DATA):
            data = data.next()
        return data.data()
    
    def setDataOfTag(self, node, newData):
        child = node.firstChild()
        if child:
            child.hide()
        node.insertData(newData)
        
    def setDataOfTagByPath(self, newData, *path):
        self.setDataOfTag(self.getTagByPath(*path), newData)
        
    def getChildNode(self, node, name, nth = 1):
        """ get nth child node by name  """
        i = 0
        for tag in node.tags():
            if tag.name() == name:
                i += 1
                if i == nth:
                    return tag
        return None
    
    def addTag(self, node, tagName, data, **attributes):
        """ add a new child tag with given name, data and attributes """
        newTag = node.insertTag(tagName)
        self.setDataOfTag(newTag, data)
        for attr, value in attributes.iteritems():
            newTag.setAttribute(attr, value)
    
    def addTagBelow(self, node, tagName, data, **attributes):
        """ add a new sibling tag after given node with given name, data and attributes """
        newTag = node.appendTag(tagName)
        self.setDataOfTag(newTag, data)
        for attr, value in attributes.iteritems():
            newTag.setAttribute(attr, value)
            
    def addTagAbove(self, node, tagName, data, **attributes):
        """ add a new sibling tag before given node with given name, data and attributes """
        newTag = node.prependTag(tagName)
        self.setDataOfTag(newTag, data)
        for attr, value in attributes.iteritems():
            newTag.setAttribute(attr, value)
    
    def deleteTagByPath(self, *path):
        node = self.getTagByPath(*path)
        if node:
            node.hide()
            return True
        return False
    
    def write(self):
        """ write object tree to file """
        exp = re.compile("<%s>(.*?)</%s>" % (commentString, commentString), re.S)
        newPspec = re.sub(exp, r"<!--\1-->", self.doc.toPrettyString())
        f = open(self.xmlFile, "w")
        f.write(newPspec)
        f.close()
        
    def read(self, xmlFileName = None):
        if xmlFileName:
            self.xmlFile = xmlFileName
            
        xmlFile = open(self.xmlFile)
        
        exp = re.compile("<!--(.*?)-->", re.S)
        newPspec = re.sub(exp, r"<%s>\1</%s>" % (commentString, commentString), xmlFile.read())
        newPspec = newPspec.replace("&", "&amp;")
        
        #TODO: escape all html chars. inside new comment tag
        # and don't forget to revert before write
        
        xmlFile.close()
        self.doc = piksemel.parseString(newPspec)
    