#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import getopt
import re
import codecs
import os

class CutDocument:
	def __init__ (self):
		self.head = []
		self.lines = []
		self.nodes = []
		self.sects = []

class CutNode:
	def __init__ (self):
		self.head = []
		self.lines = []
		self.name = ""
		self.level = ""
		self.lvl = 0
		self.cut = 0
		self.index = 0

class CutSection:
	def __init__ (self):
		self.lines = []
		self.index = 0
		self.file_name = ""
		self.lvl = 0
		self.toc = 0

class Cutter:
	img_path = "../images"
	
	def __init__ (self, html_tmpl):
		f = file (html_tmpl, "r")
		self.template = f.readlines ()
		f.close ()
	
	def get_header (self, lines):
		# hevea ciktisinda dokuman basligini bul
		head = []
		for line in lines:
			if line [:7] == "<!--TOC":
					break
			head.append (line)
		return head
	
	def fix_levels (self, nodes):
		levels = { "section": 0, "subsection": 1, "subsubsection": 2, "subsubsubsection": 3 }
		for node in nodes:
			if levels.has_key (node.level):
				node.lvl = levels[node.level]
			else:
				print "unknown node", node.level, node.name
	
	def get_nodes (self, lines):
		# hevea ciktisinda dokuman bolumlerini ayir
		nodes = []
		node = None
		flag = 0
		p = re.compile ("<!--SEC END -->")
		for line in lines:
			if flag == 0:
				# ilk bolumu ariyoruz
				if line [:7] == "<!--TOC":
					node = CutNode ()
					node.level = line.split () [1]
					node.name = line [line.find (" ", 8) + 1:line.rfind ("-->")]
					flag = 1
			elif flag == 1:
				# bolum basligi
				t = p.search (line)
				if t:
					node.head.append (line[:t.start ()])
					flag = 2
				else:
					node.head.append (line)
			elif flag == 2:
				# bolum icerigi
				if line[:7] == "<!--TOC":
					nodes.append (node)
					# yeni bolum
					node = CutNode ()
					node.level = line.split () [1]
					node.name = line [line.find (" ", 8) + 1:line.rfind ("-->")]
					flag = 1
				else:
					node.lines.append (line)
		if node:
			nodes.append (node)
		self.fix_levels (nodes)
		return nodes
	
	def make_sect_name (self, index):
		if index == 0:
			return "index.html"
		else:
			return "node_" + str (index) + ".html"
	
	def sub_lines (self, nodes, i):
		t = 0
		lvl = nodes[i].lvl
		while nodes[i]:
			t += len (nodes[i].head) + len (nodes[i].lines)
			i += 1
			if i >= len (nodes) or nodes[i].lvl <= lvl:
				break
		return t
	
	def mark_cut (self, nodes, i):
		lvl = nodes[i].lvl
		while nodes[i]:
			if nodes[i].lvl == (lvl + 1):
				nodes[i].cut = 1
			i += 1
			if i >= len (nodes) or nodes[i].lvl <= lvl:
				break
	
	def make_sects (self, nodes):
		# bolumleri sapta
		t = 0
		for node in nodes:
			t += len (node.head) + len (node.lines)
		if t > 60:
			for node in nodes:
				if node.lvl == 0:
					node.cut = 1
			for i, node in enumerate (nodes):
				size = self.sub_lines (nodes, i)
				if size > 60:
					self.mark_cut (nodes, i)
		# index linkleri icin numaralama
		index = -1
		for node in nodes:
			if node.cut == 1:
				index += 1
			node.index = index
		# bolumleri sayfalara ayir
		sects = []
		index = 0
		sect = None
		for i, node in enumerate (nodes):
			if node.cut == 1:
				if sect != None:
					if sect.toc == 0 and node.lvl > sect.lvl:
						last_lvl = sect.lvl
						while nodes[i]:
							if nodes[i].lvl > last_lvl:
								sect.lines.append ("<UL>")
								last_lvl = nodes[i].lvl
							if nodes[i].lvl < last_lvl:
								sect.lines.append ("</UL>")
								last_lvl = nodes[i].lvl
							if nodes[i].lvl > sect.lvl:
								sect.lines.append ("<LI><A HREF='./%s'>" % self.make_sect_name (nodes[i].index))
								sect.lines.append (nodes[i].name)
								sect.lines.append ("</A></LI>")
							i += 1
							if i >= len (nodes) or nodes[i].lvl <= sect.lvl:
								break
						while last_lvl > sect.lvl:
							sect.lines.append ("</UL>")
							last_lvl -= 1
					sects.append (sect)
				sect = CutSection ()
				sect.index = index
				if node.name == "İçindekiler":
					sect.toc = 1
				sect.lvl = node.lvl
				sect.file_name = self.make_sect_name (index)
				index += 1
			else:
				if sect == None:
					sect = CutSection ()
					sect.index = index
					sect.lvl = node.lvl
					sect.file_name = self.make_sect_name (index)
					index += 1
			sect.lines += node.head
			sect.lines += node.lines
		sects.append (sect)
		return sects
	
	def fix_links (self, doc):
		# linkleri yeni tasindiklari dosyalara yoneltelim
		links = {}
		p = re.compile ("NAME=\"")
		for sect in doc.sects:
			for line in sect.lines:
				t = p.search (line)
				while t:
					url = line[t.end():line.find ("\"", t.end())]
					links[url] = sect.file_name
					t = p.search (line, t.end ())
		p = re.compile ("HREF=\"#")
		for sect in doc.sects:
			lines2 = []
			for line in sect.lines:
				t = p.search (line)
				if t:
					href = line[t.end (): line.find ("\"", t.end())]
					a = line [:t.end () - 1]
					b = line [line.find ("\"", t.end ()):]
					lines2.append (a + links[href] + "#" + href + b)
				else:
					lines2.append (line)
			sect.lines = lines2
	
	def write_html (self, lines, file_name):
		# verilen satirlari sablona gore dosyaya yaz
		f = file (file_name, "w")
		fe = codecs.EncodedFile (f, "utf-8", "utf-8")
		for tline in self.template:
			if tline.find ("$content$") != -1:
				for line in lines:
					fe.write (line)
			else:
				fe.write (tline)
		f.close ()
		# apache ssi xbithack icin gerekli
		os.chmod (file_name, 0755)
	
	def make_navbar (self, pi, ni):
		# navigasyon butonlari icin html kodu olustur
		t = "<table class='navbar'><tbody><tr>"
		if pi != -1:
			if pi == 0:
				t += "<td class='navbut'><a href='index.html'><img src='" + self.img_path + "/nav_back.png' border=0>Önceki sayfa</a></td>"
			else:
				t += "<td class='navbut'><a href='node_" + str (pi) + ".html'><img src='" + self.img_path + "/nav_back.png' border=0>Önceki sayfa</a></td>"
		else:
			t += "<td class='navhide'><img src='" + self.img_path + "/nav_back.png'>Önceki sayfa</td>"
		t += "<td class='navbut'><a href='index.html'><img src='" + self.img_path + "/nav_home.png' border=0>Başlangıç</a></td>"
		if ni != -1:
			t += "<td class='navbut'><a href='node_" + str (ni) + ".html'><img src='" + self.img_path + "/nav_forward.png' border=0>Sonraki sayfa</a></td>"
		else:
			t += "<td class='navhide'><img src='" + self.img_path + "/nav_forward.png'>Sonraki sayfa</td>"
		t += "</tr></tbody></table>\n"
		return t
	
	def write_sects (self, doc):
		# bolumleri yaz
		i = -1
		max = doc.sects[-1].index
		for sect in doc.sects:
			if sect.index < max:
				nb = self.make_navbar (i, sect.index + 1)
				i += 1
			else:
				nb = self.make_navbar (i, -1)
			lines = []
			lines.append (nb)
			lines += doc.head[:]
			lines += sect.lines
			lines.append (nb)
			self.write_html (lines, sect.file_name)
	
	def cut (self, html_name):
		print "Cutting %s..." % (html_name)
		# hevea ciktisini okuyalim
		f = file (html_name, "r")
		fe = codecs.EncodedFile (f, "utf-8", "iso-8859-9")
		lines = fe.readlines ()
		f.close ()
		# gereksiz kisimlari atip, bikac ceviri yapalim
		doc = CutDocument ()
		flag = 0
		p1 = re.compile ("Table of Contents")
		p2 = re.compile ("Abstract")
		for line in lines:
			if flag == 0:
				if line[:7] == "<!--CUT":
					flag = 1
			elif flag == 1:
				if line [:15] == "<!--HTMLFOOT-->":
					break
				t = p1.search (line)
				if t:
					line = line[:t.start()] + "İçindekiler" + line[t.end():]
				t = p2.search (line)
				if t:
					line = line[:t.start()] + "Özet" + line[t.end():]
				doc.lines.append (line)
		# bolumleri ayiralim
		doc.head = self.get_header (doc.lines)
		doc.nodes = self.get_nodes (doc.lines)
		if len (doc.nodes) == 0:
			# ozel durum, bolumsuz belge
			self.write_html (doc.lines, html_name)
			self.write_html (doc.lines, "index.html")
			return
		# hevea ciktisini duzeltelim
		self.write_html (doc.lines, html_name)
		# cok sayfali halini olusturalim
		doc.sects = self.make_sects (doc.nodes)
		# linkleri duzeltelim
		self.fix_links (doc)
		# yazalim bitsin
		self.write_sects (doc)

#
def usage ():
	print "Usage: sayfakes.py <belge.html>..."
	sys.exit (2)

try:
	opts, args = getopt.gnu_getopt (sys.argv[1:], "h", ["help"])
except:
	usage ()

for o, v in opts:
	if o in ("-h", "--help"):
		usage ()

if args == []:
	usage ()

c = Cutter ("../belge.tmpl")
for name in args:
	c.cut (name)
