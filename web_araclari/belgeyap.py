#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2004, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#

# belgeyap.py
# lyx exporter

# python modules
import sys
import time
import os
import os.path
import string
import re
import codecs
import getopt
import shutil
from stat import *
from svn import core, client

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
	def get_header (self, lines):
		# hevea ciktisinda dokuman basligini bul
		head = []
		for line in lines:
			t = line.find("<!--TOC")
			if t != -1:
				if t > 0:
					head.append(line[:t])
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
				t = line.find("<!--TOC")
				if t != -1:
					line = line[t:]
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
					if line.find("-->") != -1:
						node.name = line [line.find (" ", 8) + 1:line.rfind ("-->")]
						flag = 1
					else:
						node.name = line [line.find(" ", 8):]
						flag = 3
				else:
					node.lines.append (line)
			elif flag == 3:
				if line.find("-->") != -1:
					node.name += line [:line.rfind ("-->")]
					flag = 2
				else:
					node.name += line[:]
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
	
	def write_html(self, lines, file_name):
		# verilen satirlari sablona gore dosyaya yaz
		f = file(file_name, "w")
		fe = codecs.EncodedFile (f, "utf-8", "utf-8")
		fe.write("<html><head>\n")
		fe.write("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\">\n")
		fe.write("</head><body>\n")
		fe.write("<!-- SAYFA İÇERİK BAŞI -->\n")
		fe.write("<div class=\"belge\">\n")
		for line in lines:
			fe.write(line)
		fe.write("</div>\n")
		fe.write("<!-- SAYFA İÇERİK SONU -->\n")
		fe.write("</body></html>\n")
		f.close()
	
	def make_navbar (self, pi, ni):
		# navigasyon butonlari icin html kodu olustur
		t = "<table class='navbar'><tbody><tr>"
		if pi != -1:
			if pi == 0:
				t += "<td class='navbut'><a href='index.html'><img src='" + self.img_path + "/nav_back.png' border=0> Önceki sayfa</a></td>"
			else:
				t += "<td class='navbut'><a href='node_" + str (pi) + ".html'><img src='" + self.img_path + "/nav_back.png' border=0> Önceki sayfa</a></td>"
		else:
			t += "<td class='navhide'><img src='" + self.img_path + "/nav_back.png'> Önceki sayfa</td>"
		t += "<td class='navbut'><a href='index.html'><img src='" + self.img_path + "/nav_home.png' border=0> Başlangıç</a></td>"
		if ni != -1:
			t += "<td class='navbut'><a href='node_" + str (ni) + ".html'><img src='" + self.img_path + "/nav_forward.png' border=0> Sonraki sayfa</a></td>"
		else:
			t += "<td class='navhide'><img src='" + self.img_path + "/nav_forward.png'> Sonraki sayfa</td>"
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

def ensure_dir(dname):
	if not os.path.exists(dname):
		os.mkdir(dname, 0755)
	os.chdir(dname)

def ensure_path(fname):
	if fname.find("/") != -1:
		t = fname.split("/")
		if not os.path.exists(t[0]):
			os.mkdir(t[0], 0755)

def remove_file(name):
	try:
		os.unlink(name)
	except:
		pass

def svn_fetch(repo,fname):
	print "'%s' getiriliyor..." % (repo + fname)
	# init
	core.apr_initialize()
	pool = core.svn_pool_create(None)
	core.svn_config_ensure(None, pool)
	# client context for auth
	ctx = client.svn_client_ctx_t()
	provs = []
	provs.append(client.svn_client_get_simple_provider(pool))
	provs.append(client.svn_client_get_username_provider(pool))
	provs.append(client.svn_client_get_ssl_server_trust_file_provider(pool))
	provs.append(client.svn_client_get_ssl_client_cert_file_provider(pool))
	provs.append(client.svn_client_get_ssl_client_cert_pw_file_provider(pool))
	ctx.auth_baton = core.svn_auth_open(provs, pool)
	ctx.config = core.svn_config_get_config(None, pool)
	# fetch last revision
	rt = core.svn_opt_revision_t()
	rt.kind = core.svn_opt_revision_head
	# stream
	f = file(fname, "w")
	st = core.svn_stream_from_aprfile(f, pool)
	# get commit date
	de = client.svn_client_ls(repo + fname, rt, 0, ctx, pool)
	for a,b in de.iteritems():
		ret = time.strftime("%d/%m/%Y", time.gmtime(b.time / 1000000))
	# fetch
	client.svn_client_cat(st, repo + fname, rt, ctx, pool)
	# cleanup
	f.close()
	core.svn_pool_destroy(pool)
	core.apr_terminate()
	return ret

def retouch_lyx(lyxname):
	print "'%s' düzeltiliyor..." % (lyxname)
	# lyx dosyasini okuyalim
	f = file(lyxname, "r")
	lines = f.readlines()
	f.close()
	yeni = []
	# duzeltmeler
	for line in lines:
		# paragraf aralari bosluk olmali
		if line.find("\\paragraph_separation ") != -1:
			yeni.append("\\paragraph_separation skip\n")
		# kaliteli pdf cikti icin font secimi
		elif line.find("\\fontscheme ") != -1:
			yeni.append("\\fontscheme pslatex\n")
		# alakasiz satir
		else:
			yeni.append(line)
	# degisiklikleri yazalim
	f = file(lyxname, "w")
	f.writelines(yeni)
	f.close()

def fix_hevea():
	ff = [
	"\\newcommand{\\textless}{\\@print{&lt;}}",
	"\\newcommand{\\textgreater}{\\@print{&gt;}}",
	"\\newcommand{\\textbackslash}{\\@print{&#92;}}" ]
	f = file("duzeltmeler.hva", "w")
	f.writelines(ff)
	f.close()

def export(lyxname, dname):
	# pdf ve latex cikti
	print "'%s' oluşturuluyor..." % (dname + ".pdf")
	os.spawnlp(os.P_WAIT, "lyx", "lyx", "-e", "pdf2", lyxname);
	basename = lyxname[:]
	if basename[-4:] == ".lyx":
		basename = basename[0:-4]
	shutil.move(basename + ".pdf", dname + ".pdf")
	texname = basename + ".tex"
	print "'%s' oluşturuluyor..." % (texname)
	os.spawnlp(os.P_WAIT, "lyx", "lyx", "-e", "latex", lyxname);
	# simdi html ciktilar
	print "'%s' oluşturuluyor..." % (dname + ".html")
	fix_hevea()
	os.spawnlp(os.P_WAIT, "hevea", "hevea", "-fix", "duzeltmeler.hva", texname, "-o", dname + ".html")

def bilgibas(name,dname,date):
	pdf_size = str(os.stat(dname + ".pdf")[ST_SIZE] / 1024)
	print ""
	print "<tr>"
	print '<td align="left"><b>%s</b> (%s)</td>' % (name, date)
	print '<td><a href="./%s/index.html">HTML</a></td>' % (dname)
	print '<td><a href="./%s/%s.html">HTML (tek sayfa)</a></td>' % (dname,dname)
	print '<td><a href="./%s/%s.pdf">PDF (%s KB)</a></td>' % (dname,dname,pdf_size)
	print "</tr>"
	print ""

def yap(template,clean_flag):
	ikonlar = "../../images"
	tamir = 1
	# open document template and get information
	f = file(template)
	exec(f)
	f.close()
	# open html template
	c = Cutter()
	c.img_path = ikonlar
	# prepare directory
	ensure_dir(dizin)
	# fetch the document
	dt = svn_fetch(depo,belge)
	# fix some problems if necessary
	if tamir == 1:
		retouch_lyx(belge)
	# fetch images if necessary
	try:
		for t in dosyalar:
			ensure_path(t)
			try:
				svn_fetch(depo,t)
			except:
				print "'%s' getirilemedi!" % (t)
	except:
		pass
	# create documents
	export(belge,dizin)
	# tek ve cok sayfaliya ayir
	c.cut(dizin + ".html")
	# gereksiz dosyaları temizle
	if clean_flag == 1:
		remove_file(dizin + ".haux")
		remove_file(dizin + ".htoc")
		os.unlink(belge)
		basename = belge
		if basename[-4:] == ".lyx":
			basename = basename[0:-4]
		os.unlink(basename + ".tex")
		os.unlink("duzeltmeler.hva")
	# indekse eklemek icin html kodu bas
	bilgibas(isim,dizin,dt)
	# leave directory
	os.chdir("..")

def usage():
	print "Kullanım: belgeyap.py <belgeşablonu>..."
	print "Örnek şablon dosyası içeriği:"
	print "  # -*- coding: utf-8 -*-"
	print "  depo = \"http://svn.uludag.org.tr/uludag/path/\""
	print "  belge = \"örnek.lyx\""
	print "  isim = \"Şablon Örneği Belgesi\""
	print "  dizin = \"ornek\""
	print "Bu örnek, 'ornek' dizini içinde depodan aldığı belgenin"
	print "html (tek sayfa, çok sayfa) ve pdf sürümlerini oluşturur."
	print "Opsiyonel parametreler:"
	print '  dosyalar = [ "dosya1.png", "dosya2.png" ]'
	print '  ikonlar = "../../images/"'
	print "Ek dosyaları depodan almak, ve navigasyon ikonlarının"
	print "yerini belirtmek için kullanabilirsiniz."
	print ""
	print "Hata raporlarını gurer @ uludag.org.tr ye gönderin."
	sys.exit(2)

# main
try:
	opts, args = getopt.gnu_getopt(sys.argv[1:], "hn", ["help", "noclean"])
except:
	usage()

opt_clean = 1

for o, v in opts:
	if o in ("-h", "--help"):
		usage()
	if o in ("-n", "--noclean"):
		opt_clean = 0

if args == []:
	usage()

for name in args:
	yap(name, opt_clean)
