#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2006-2009, TUBITAK/UEKAE
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
import logging
from pysqlite2 import dbapi2 as sqlite

class Bookmark:
	def __init__(self):
		self.dom = xml.dom.minidom.getDOMImplementation()
		self.logger = logging.getLogger("migration4.bookmark")
		self.document = self.dom.createDocument(None, "bookmarks", None)
		self.FF3exists = False #if FF3 exists in the source computer(windows), this variable will be changed to True
	def getFFBookmarks(self, path):
		"""Gets Firefox Bookmarks from a bookmarks.html file"""
		#if places.sqlite is found, don't try to import from bookmarks.html
		self.logger.info("Starting getting Firefox Bookmarks")
		path = "/home/cimamoglu/" #TO BE DELETED!!! ONLY FOR DEBUGGING PURPOSES
		
		filename = os.path.join(path, "places.sqlite")
		if os.path.isfile(filename):
			self.FF3exists = True
			self.FF3dblocation = filename # the location of places.sqlite in source computer will be used in setFF3Bookmarks
			return
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

		print "Document:%s" % self.document.toxml()

	def getOperaBookmarks(self, path):
		"""Gets Opera Bookmarks from a opera6.adr file"""
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
		"""Gets IE Bookmarks from a Favourites directory"""
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
		"""Adds bookmarks to firefox"""

		print "setFFBookmarks.path:%s" % path
		if os.path.lexists(os.path.join(path, "lock")):
			raise Exception, "Firefox is in use. Bookmarks could not be saved."
		#if places.sqlite exists, then Pardus has FF3. Set the bookmarks accordingly
		filepath = os.path.join(path, "places.sqlite")
		if os.path.exists(filepath):
			self.setFF3Bookmarks(filepath)
			return

		filepath = os.path.join(path, "bookmarks.html")
		if os.path.exists(filepath):
			self.setFF2Bookmarks(filepath)
			return
		else:
			raise Exception, "Bookmark file cannot be found."

	def setFF2Bookmarks(self, filepath):
		"""Adds bookmarks to firefox using bookmarks.html file"""

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
		"""Adds bookmarks to firefox using places.sqlite database"""
		print "Firefox3 üzerinde işlem yapılıyor...."
		def getText(nodelist):
			rc = ""
			for node in nodelist:
				if node.nodeType == node.TEXT_NODE:
					rc = rc + node.data
			return rc

		def handleNode(node, cursor, parentid, position):
			print "!!!!handleNode!!!!!"
			print "node.tagName:%s" % node.tagName
			if node.tagName == "bookmarks":
				# Handle children:
				children = node.childNodes
				for child in children:
					print "position:%d" % position
					handleNode(child, cursor, parentid, position)
					position += 1
			elif node.tagName == "group":
				# Get group title:
				header = node.getElementsByTagName("header")[0]
				title = getText(header.childNodes)
				# Add group:
				print "parentid1:%d" % parentid
				print "position:%s" % position
				print "title:%s" % title
				print "(parentid:%s, position:%s, title:%s)" % (parentid, position, title)
				cursor.execute("INSERT INTO moz_bookmarks ('type', 'parent', 'position', 'title') VALUES (2, ?, ?, ?)", (parentid, position, title))
				parentid = cursor.lastrowid
				#print "parentid2:%d" % parentid
				if not parentid:    # Hack for lastrowid error
					result = cursor.execute("SELECT max(id) FROM moz_bookmarks")
					parentid = result.fetchone()[0]
					print "parentid3:%d" % parentid
				print "parentid3 basılmadı...."
				# Handle children:
				children = node.childNodes
				position = 0
				for child in children:
					handleNode(child, cursor, parentid, position)
					print "position:%d" % position
					position += 1
			elif node.tagName == "bookmark":
				# Get title and url:
				namenode = node.getElementsByTagName("name")[0]
				#print "namenode:%s" % namenode

				urlnode = node.getElementsByTagName("url")[0]
				#print "urlnode:%s" % urlnode
				title = getText(namenode.childNodes)
				print "bookmark title%s" % title
				url = getText(urlnode.childNodes)
				print "bookmark url:%s" % url

				fk = addURIToPlaces(cursor,url,title)

				cursor.execute("INSERT INTO moz_bookmarks ('type', 'fk', 'parent', 'position', 'title') VALUES (1, ?, ?, ?, ?)", (fk, parentid, position, title))
				#print "buraya gelindi ve eklenmiş olması grekkkk..."
		# TO BE TESTED MORE!!!!
		def addURIToPlaces(cursor,url,title):
			"""This method adds(or finds the id of) a given url from moz.places"""
			result = cursor.execute("SELECT id FROM moz_places WHERE url=?", (url,)).fetchone()
			if result:
				fk = result[0]
				#print "select ile fk = result[0]:%s" % fk
				return fk
			else:
				print "INSERT INTO moz_places ('%s','%s')" % (url, title)
				result = cursor.execute("INSERT INTO moz_places ('url','title') VALUES (?, ?)", (url, title))
				if result:
					fk = cursor.lastrowid
					#the hack below is for situations where lastrowid doesn't work
					if not fk:    # Hack for lastrowid error
						result = cursor.execute("SELECT max(id) FROM moz_places")
						fk = result.fetchone()[0]
					#print "insert ile fk = result[0]:%s" % fk	    
				return fk
			
		# TO BE TESTED MORE!!!!
		def addFromFF3(srcCursor, destCursor, ID, parentID, startingPos):
			curRow = srcCursor.execute("SELECT * from moz_bookmarks where id = ?",(ID,)).fetchone()

			curRow_id = ID # ID of bookmark in moz_bookmarks
			curRow_type = curRow[1] # Type 1 = sites, Type 2 = folders
			curRow_fk = curRow[2] # This is the ID of bookmark's URL in moz_places
			curRow_parent = curRow[3] # ID of parent of bookmark in moz_bookmarks
			curRow_position = curRow[4] # Physical position of the bookmark among others in same directory
			curRow_title = curRow[5] # Title of bookmark
#			print(curRow_title)
			if curRow_id != 2:
				# Find the fk of URL, if cannot be found, assign NULL
				res = srcCursor.execute("SELECT url FROM moz_places WHERE id = ?",(curRow_fk,)).fetchone()
				if res:
					url = res[0]
					fk = addURIToPlaces(destCursor,url,curRow_title)
				else:
					fk = "NULL"
				#position düzelt
				destCursor.execute("INSERT INTO moz_bookmarks ('type', 'fk', 'parent', 'position', 'title') VALUES (?, ?, ?, ?, ?)", (curRow_type, fk, parentID, curRow_position, curRow_title))
				curRow_id = destCursor.lastrowid
			if curRow_type == 2:
				children = srcCursor.execute("SELECT * FROM moz_bookmarks WHERE parent = ? ORDER BY position ASC",(ID,)).fetchall()
				for child in children:
					child_id = child[0]
					child_type = child[1]
					child_fk = child[2]
					child_parent = child[3]
					child_position = child[4]
					child_title = child[5]
					# find the position to put. if under main directory, put next suitable place.
					pos = child_position if curRow_id != 2 else startingPos
					#print("--",[i for i in child])
					
					# For adding the children, branch recursively.
					addFromFF3(srcCursor, destCursor, child_id, curRow_id, pos)
					# increase the counter
					if ID == 2: startingPos += 1

		# Connect to database:
		conn = sqlite.connect(databasepath, 5.0)
		cursor = conn.cursor()
		conn.text_factory = str
		# Find the maximum physical position under main bookmarks directory:
		result = cursor.execute("SELECT max(position) FROM moz_bookmarks WHERE parent=2")
		maxPos_2 = result.fetchone()[0]
		startingPos_2 = maxPos_2 + 1 if maxPos_2 else 0


		# Handle bookmarks:
		# If the Firefox version in source computer is not FF3, process upon bookmarks.html file
		if (not self.FF3exists):
			handleNode(self.document.documentElement, cursor, 2, startingPos_2)

		# If the Firefox version in source computer is FF3, get SQLite data, and put it into Pardus' FF3's SQLite database
		else:
			connection = sqlite.connect(self.FF3dblocation)
			srcCursor = connection.cursor()
			connection.text_factory = str
			addFromFF3(srcCursor, cursor, 2,-1, startingPos_2)

			connection.commit()
			srcCursor.close()	    
		# Close database:
		conn.commit()
		cursor.close()

	def saveXML(self, filename):
		"""Saves Bookmarks to an XML file"""
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
# TO BE DELETED!!!!!!!!!
if __name__ == "__main__":
	bk = Bookmark()
	bk.getFFBookmarks("a")
	bk.setFFBookmarks("/home/cimamoglu/.mozilla/firefox/ztm42wlw.default/")