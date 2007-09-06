# -*- coding: utf-8 -*-

import piksemel
import re

commentString = "PakitoComment"

class XmlUtil:
    """ class with comment support and some utilities"""
    def __init__(self, xmlFileName):
        global commentString
        
        self.xmlFile = xmlFileName
        xmlFile = open(xmlFileName)
        
        exp = re.compile("<!--(.*?)-->", re.S)
        newPspec = re.sub(exp, r"<%s>\1</%s>" % (commentString, commentString), xmlFile.read())
        newPspec = newPspec.replace("&", "&amp;")
        
        #TODO: escape all html chars. inside new comment tag
        # and don't forget to revert before write
        
        xmlFile.close()
        self.doc = piksemel.parseString(newPspec)
        
    def getTagByPath(self, *path):
        """ get tag by path. e.g getTagByPath("Source", "Packager", "Name") give the Name tag """
        node = self.doc
        for tag in path:
            node = node.getTag(tag)
            if node == None:
                return None
        return node
    
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
        exp = re.compile("<PakitoComment>(.*?)</PakitoComment>", re.S)
        newPspec = re.sub(exp, r"<!--\1-->", self.doc.toPrettyString())
        f = open(self.xmlFile, "w")
        f.write(newPspec)
        f.close()
    
    
    
    
    
    
    