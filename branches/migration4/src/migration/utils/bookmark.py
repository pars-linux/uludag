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
from pysqlite2 import dbapi2 as sqlite

class Bookmark:
    def __init__(self):
        self.dom = xml.dom.minidom.getDOMImplementation()
        self.document = self.dom.createDocument(None, "bookmarks", None)

    def getFFBookmarks(self, path):
        "Gets Firefox Bookmarks from a bookmarks.html file"
        filename = os.path.join(path, "bookmarks.html")
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

    def getOperaBookmarks(self, path):
        "Gets Opera Bookmarks from a opera6.adr file"
        # open file:
        filename = os.path.join(path, "opera6.adr")
        bookmarkfile = open(filename)
        # create main node:
        groupnode = self.document.createElement("group")
        headernode = self.document.createElement("header")
        textnode = self.document.createTextNode("Opera Bookmarks")
        groupnode.appendChild(headernode)
        headernode.appendChild(textnode)
        self.document.documentElement.appendChild(groupnode)
        # parse file:
        nodetype = None
        nodename = None
        nodeurl = None
        for line in bookmarkfile:
            line = line.strip()
            if not line:
                if nodetype == "FOLDER":
                    newgroup = self.document.createElement("group")
                    headernode = self.document.createElement("header")
                    textnode = self.document.createTextNode(nodename)
                    newgroup.appendChild(headernode)
                    headernode.appendChild(textnode)
                    groupnode.appendChild(newgroup)
                    groupnode = newgroup
                elif nodetype == "URL":
                    newnode = self.document.createElement("bookmark")
                    namenode = self.document.createElement("name")
                    textnode = self.document.createTextNode(nodename)
                    namenode.appendChild(textnode)
                    newnode.appendChild(namenode)
                    urlnode = self.document.createElement("url")
                    textnode = self.document.createTextNode(nodeurl)
                    urlnode.appendChild(textnode)
                    newnode.appendChild(urlnode)
                    groupnode.appendChild(newnode)
                nodetype = None
                nodename = None
                nodeurl = None
            elif line.startswith("#"):
                nodetype = line.replace("#","",1)
            elif line.startswith("NAME="):
                nodename = line.replace("NAME=","",1)
            elif line.startswith("URL="):
                nodeurl = line.replace("URL=","",1)
            elif line == "-":
                groupnode = groupnode.parentNode

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

    def setFFBookmarks(self, path):
        "Adds bookmarks to firefox"
        if os.path.lexists(os.path.join(path, "lock")):
            raise Exception, "Firefox is in use. Bookmarks cannot be saved."
        filepath = os.path.join(path, "places.sqlite")
        if os.path.exists(filepath):
            self.setFF3Bookmarks(filepath)
            return
        filenpath = os.path.join(path, "bookmarks.html")
        if os.path.exists(filepath):
            self.setFF2Bookmarks(filepath)
            return
        raise Exception, "Bookmark file cannot be found."

    def setFF2Bookmarks(self, filepath):
        "Adds bookmarks to firefox using bookmarks.html file"
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

        bookmarkfile = open(filepath)
        data = bookmarkfile.read()
        bookmarkfile.close()
        pairs = data.rsplit("</DL>",1)
        data = handleNode(self.document.documentElement)
        bookmarkfile = open(filename, "w")
        bookmarkfile.write(pairs[0] + data + "</DL>" + pairs[1])
        bookmarkfile.close()

    def setFF3Bookmarks(self, databasepath):
        "Adds bookmarks to firefox using places.sqlite database"
        def getText(nodelist):
            rc = ""
            for node in nodelist:
                if node.nodeType == node.TEXT_NODE:
                    rc = rc + node.data
            return rc

        def handleNode(node, c, parentid, position):
            if node.tagName == "bookmarks":
                # Handle children:
                children = node.childNodes
                for child in children:
                    handleNode(child, c, parentid, position)
                    position += 1
            elif node.tagName == "group":
                # Get group title:
                header = node.getElementsByTagName("header")[0]
                title = getText(header.childNodes)
                # Add group:
                c.execute("INSERT INTO moz_bookmarks ('type', 'parent', 'position', 'title') VALUES (2, ?, ?, ?)", (parentid, position, title))
                parentid = c.lastrowid
                if not parentid:    # Hack for lastrowid error
                    result = c.execute("SELECT max(id) FROM moz_bookmarks")
                    parentid = result.fetchone()[0]
                # Handle children:
                children = node.childNodes
                position = 0
                for child in children:
                    handleNode(child, c, parentid, position)
                    position += 1
            elif node.tagName == "bookmark":
                # Get title and url:
                namenode = node.getElementsByTagName("name")[0]
                urlnode = node.getElementsByTagName("url")[0]
                title = getText(namenode.childNodes)
                url = getText(urlnode.childNodes)
                # Add bookmark:
                result = c.execute("SELECT id FROM moz_places WHERE url=?", (url,)).fetchone()
                if result:
                    fk = result[0]
                else:
                    c.execute("INSERT INTO moz_places ('url','title') VALUES (?, ?)", (url, title))
                    fk = c.lastrowid
                c.execute("INSERT INTO moz_bookmarks ('type', 'fk', 'parent', 'position', 'title') VALUES (1, ?, ?, ?, ?)", (fk, parentid, position, title))

        # Connect to database:
        conn = sqlite.connect(databasepath, 5.0)
        c = conn.cursor()
        # Find the maximum position:
        result = c.execute("SELECT max(position) FROM moz_bookmarks WHERE parent=2")
        maxpos = result.fetchone()[0]
        if maxpos:
            newpos = maxpos+1
        else:
            newpos = 0
        # Hande bookmarks:
        data = handleNode(self.document.documentElement, c, 2, newpos)
        # Close database:
        conn.commit()
        c.close()

    def saveXML(self, filename):
        "Saves Bookmarks to an XML file"
        xmlfile = open(filename, "w")
        data = self.document.toprettyxml()
        xmlfile.write(data)
        xmlfile.close()

    def size(self):
        return len(self.document.getElementsByTagName("bookmark")) * 200

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
