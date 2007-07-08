#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#

import xml.dom.minidom
import HTMLParser
import ConfigParser
import os

class Bookmark:
    def __init__(self):
        self.dom = xml.dom.minidom.getDOMImplementation()
        self.document = self.dom.createDocument(None, "bookmarks", None)
    
    def getFFBookmarks(self, filename):
        "Gets Firefox Bookmarks from a bookmarks.html file"
        bookmarkfile = open(filename)
        data = bookmarkfile.read()
        bookmarkfile.close()
        parser = FFBookmarkParser(self.document)
        parser.feed(data)
        headernode = self.document.createElement("header")
        textnode = self.document.createTextNode("Firefox Bookmarks")
        headernode.appendChild(textnode)
        mainnode = self.document.documentElement.lastChild
        if mainnode.hasChildNodes():
            mainnode.insertBefore(headernode, mainnode.firstChild)
        else:
            mainnode.appendChild(headernode)
    
    def getIEBookmarks(self, directory):
        "Gets IE Bookmarks from a Favourites directory"
        def searchDirectory(directory, document, node):
            files = os.listdir(directory)
            for filename in files:
                filepath = os.path.join(directory, filename)
                base, ext = os.path.splitext(filename)
                if os.path.isdir(filepath):
                    groupnode = document.createElement("group")
                    headernode = document.createElement("header")
                    textnode = document.createTextNode(filename)
                    headernode.appendChild(textnode)
                    groupnode.appendChild(headernode)
                    node.appendChild(groupnode)
                    searchDirectory(filepath, document, groupnode)
                elif ext == ".url":
                    parser = ConfigParser.ConfigParser()
                    parser.readfp(open(filepath))
                    url = parser.get("InternetShortcut","URL")
                    bookmarknode = document.createElement("bookmark")
                    namenode = document.createElement("name")
                    urlnode = document.createElement("url")
                    textnode = document.createTextNode(base)
                    namenode.appendChild(textnode)
                    textnode = document.createTextNode(url)
                    urlnode.appendChild(textnode)
                    bookmarknode.appendChild(namenode)
                    bookmarknode.appendChild(urlnode)
                    node.appendChild(bookmarknode)
            return xml
        groupnode = self.document.createElement("group")
        headernode = self.document.createElement("header")
        textnode = self.document.createTextNode("Internet Explorer Bookmarks")
        groupnode.appendChild(headernode)
        headernode.appendChild(textnode)
        self.document.documentElement.appendChild(groupnode)
        searchDirectory(directory, self.document, groupnode)
    
    def setFFBookmarks(self, filename):
        def getText(nodelist):
            rc = ""
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc = rc + node.data
            return rc
        def handleNode(node):
            data = ""
            if node.tagName == "bookmarks":
                children = node.childNodes
                for child in children:
                    data += handleNode(child)
            if node.tagName == "group":
                header = node.getElementsByTagName("header")[0]
                data += "<DT><H3>%s</H3>\n<DL><p>\n" % getText(header.childNodes)
                children = node.childNodes
                for child in children:
                    data += handleNode(child)
                data += "</DL><p>\n"
            if node.tagName == "bookmark":
                name = node.getElementsByTagName("name")[0]
                url = node.getElementsByTagName("url")[0]
                data += "<DT><A HREF=\"%s\">%s</A>\n" % (getText(url.childNodes), getText(name.childNodes))
            return data
        bookmarkfile = open(filename)
        data = bookmarkfile.read()
        bookmarkfile.close()
        pairs = data.rsplit("</DL>",1)
        data = handleNode(self.document.documentElement)
        bookmarkfile = open(filename, "w")
        bookmarkfile.write(pairs[0] + data + "</DL>" + pairs[1])
        bookmarkfile.close()
    
    def saveXML(self, filename):
        "Saves Bookmarks to an XML file"
        xmlfile = open(filename, "w")
        data = self.document.toprettyxml()
        xmlfile.write(data)
        xmlfile.close()
        
class FFBookmarkParser(HTMLParser.HTMLParser):
    def __init__(self, document):
        self.document = document
        self.node = document.documentElement
        self.datapart = ""
        self.mode = "item"
        HTMLParser.HTMLParser.__init__(self)
    
    def handle_starttag(self, tag, attr):
        if self.mode == "get dd":
            self.mode = "item"
            newnode = self.document.createElement("description")
            textnode = self.document.createTextNode(self.datapart)
            newnode.appendChild(textnode)
            self.node.lastChild.appendChild(newnode)
            self.datapart = "" 
        if tag == "dl":
            newnode = self.document.createElement("group")
            self.node.appendChild(newnode)
            self.node = newnode
            if self.datapart != "":
                newnode = self.document.createElement("header")
                self.node.appendChild(newnode)
                self.node = newnode
                newnode = self.document.createTextNode(self.datapart)
                self.node.appendChild(newnode)
                self.node = self.node.parentNode
                self.datapart = ""
        elif tag == "a":
            newnode = self.document.createElement("bookmark")
            self.node.appendChild(newnode)
            self.node = newnode
            for at in attr:
                key, value = at
                if key == "href":
                    newnode = self.document.createElement("url")
                    self.node.appendChild(newnode)
                    self.node = newnode
                    newnode = self.document.createTextNode(value)
                    self.node.appendChild(newnode)
                    self.node = self.node.parentNode
                self.mode = "get data"
        elif tag == "h3":
            self.mode = "get data"
        elif tag == "dd" and self.mode != "wait dl":
            self.mode = "get dd"
    
    def handle_endtag(self, tag):
        if self.mode == "get dd":
            self.mode = "item"
            newnode = self.document.createElement("description")
            textnode = self.document.createTextNode(self.datapart)
            newnode.appendChild(textnode)
            self.node.lastChild.appendChild(newnode)
            self.datapart = "" 
        if tag == "dl":
            self.node = self.node.parentNode
        elif tag == "a":
            newnode = self.document.createElement("name")
            self.node.appendChild(newnode)
            self.node = newnode
            newnode = self.document.createTextNode(self.datapart)
            self.node.appendChild(newnode)
            self.node = self.node.parentNode
            self.node = self.node.parentNode
            self.datapart = ""
            self.mode = "item"
        elif tag == "h3":
            self.mode = "wait dl"
    
    def handle_data(self, data):
        if self.mode == "get data" or self.mode == "get dd":
            self.datapart += data
    
    def handle_charref(self, data):
        if self.mode == "get data" or self.mode == "get dd":
            self.datapart += "&#%s;" % data
    
    def handle_entitiyref(self, data):
        if self.mode == "get data" or self.mode == "get dd":
            self.datapart += "&%s;" % data
