#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import os
import os.path
import string
import re
import codecs
from stat import *
from svn import core, client

class Document:
	svn_name = ""
	lyx_name = ""
	base_name = ""
	title = ""
	date = ""
	pdf_size = ""
	
	def __init__ (self, name):
		self.svn_name = name
		tmp = name[name.rfind ('/') + 1:len (name)]
		self.lyx_name = tmp
		if tmp[-4:] == ".lyx":
			self.base_name = tmp[0:-4]
		else:
			self.base_name = tmp
	
	def ensure_dir (self):
		if not os.path.exists (self.base_name):
			os.mkdir (self.base_name, 0755)
		os.chdir (self.base_name)
	
	def fetch (self):
		# lyx dosyasini alip lyx dizinine koyar
		print "Fetching '%s'..." % (self.svn_name)
		Document.ensure_dir (self)
		# init
		core.apr_initialize ()
		pool = core.svn_pool_create (None)
		core.svn_config_ensure (None, pool)
		# client context for auth
		ctx = client.svn_client_ctx_t ()
		provs = []
		provs.append (client.svn_client_get_simple_provider (pool))
		provs.append (client.svn_client_get_username_provider (pool))
		provs.append (client.svn_client_get_ssl_server_trust_file_provider (pool))
		provs.append (client.svn_client_get_ssl_client_cert_file_provider (pool))
		provs.append (client.svn_client_get_ssl_client_cert_pw_file_provider (pool))
		ctx.auth_baton = core.svn_auth_open (provs, pool)
		ctx.config = core.svn_config_get_config (None, pool)
		# fetch last revision
		rt = core.svn_opt_revision_t ()
		rt.kind = core.svn_opt_revision_head
		# stream
		f = file (self.lyx_name, "w")
		st = core.svn_stream_from_aprfile (f, pool)
		# get commit date
		de = client.svn_client_ls (self.svn_name, rt, 0, ctx, pool)
		for a,b in de.iteritems ():
			ret = time.strftime ("%d/%m/%Y", time.gmtime (b.time / 1000000))
		self.date = ret
		# fetch
		client.svn_client_cat (st, self.svn_name, rt, ctx, pool)
		# cleanup
		f.close ()
		core.svn_pool_destroy (pool)
		core.apr_terminate ()
		os.chdir ("..")
	
	def convert (self, text):
		# lyx dosyasi 8859-9, cevirmek lazim
		# bunun duzgun yolu bu degil saniyorum
		a = codecs.getdecoder ("iso-8859-9")
		b = codecs.getencoder ("utf-8")
		tmp = a (text)
		return b (tmp[0]) [0]
	
	def get_title (self):
		# title cekmek icin .tex i parse etmek daha kolay
		title = None
		f = file (self.base_name + ".tex", "r")
		lines = f.readlines ()
		for line in lines:
			if line[0:7] == "\\title{":
				title = line[7:]
				title = string.rstrip (title, "\\{}\r\n")
				break
		else:
			print "ERROR: no title"
		f.close ()
		return Document.convert (self, title)
	
	def get_info (self):
		# yaratilan dosyalardan bilgi cikar
		self.pdf_size = str (os.stat(self.base_name + ".pdf")[ST_SIZE] / 1024)
		self.title = Document.get_title (self)
	
	def retouch_lyx (self):
		# lyx dosyasini okuyalim
		f = file (self.lyx_name, "r")
		lines = f.readlines ()
		f.close ()
		yeni = []
		# duzeltmeler
		for line in lines:
			# paragraf aralari bosluk olmali
			if line.find ("\\paragraph_separation ") != -1:
				yeni.append ("\\paragraph_separation skip\n")
			# kaliteli pdf cikti icin font secimi
			elif line.find ("\\fontscheme ") != -1:
				yeni.append ("\\fontscheme pslatex\n")
			# alakasiz satir
			else:
				yeni.append (line)
		# degisiklikleri yazalim
		f = file (self.lyx_name, "w")
		f.writelines (yeni)
		f.close ()
	
	def export (self):
		# lyx dosyasindan diger formatlari yaratir
		print "Exporting '%s'..." % (self.lyx_name)
		Document.ensure_dir (self)
		# lyx dosyasini standartlastiralim
		Document.retouch_lyx (self)
		# pdf ve html icin latex cikti
		os.spawnlp (os.P_WAIT, "lyx", "lyx", "-e", "pdf2", self.lyx_name);
		os.spawnlp (os.P_WAIT, "lyx", "lyx", "-e", "latex", self.lyx_name);
		# title html dosyasina eklenecek, o yuzden get_info burda
		Document.get_info (self)
		# simdi html ciktilar
		html_name = self.base_name + ".html"
		os.spawnlp (os.P_WAIT, "hevea", "hevea", "-fix", self.base_name + ".tex", "-o", html_name)
		os.spawnlp (os.P_WAIT, "../sayfakes.py", "../sayfakes.py", html_name)
		# html header footer duzeltmeleri
		os.chdir ("..")

class Index:
	docs = []
	
	def __init__ (self, name, doc_tmpl):
		# sablonu oku
		f = file (name, "r")
		lines = f.readlines ()
		f.close ()
		self.template = lines
		# belge sablonunu oku
		f = file (doc_tmpl, "r")
		dtlines = f.readlines ()
		f.close ()
		# sablon icinden belge nesneleri cikar
		p = re.compile ("\$doc=.*\$")
		for line in lines:
			tmp = p.search (line)
			if tmp != None:
				doc = Document (tmp.group()[5:-1])
				doc.template = dtlines
				self.docs.append (doc)
	
	def make_docs (self):
		# belgeleri hazirla
		for doc in self.docs:
			doc.fetch ()
		for doc in self.docs:
			doc.export ()
	
	def make_index (self, name):
		# indeksi hazirla
		print "Generating '%s'..." % (name)
		f = file (name, "w")
		p = re.compile("\$[^$]*\$")
		i = -1
		for line in self.template:
			tmp = p.search (line)
			while tmp != None:
				tag = tmp.group ()[1:-1]
				value = ""
				if tag.find ("doc") != -1:
					i = i + 1
				elif tag == "title":
					value = self.docs[i].title
				elif tag == "date":
					value = self.docs[i].date
				elif tag == "html_link":
					t = self.docs[i].base_name
					value = t + "/index.html"
				elif tag == "html_single_link":
					t = self.docs[i].base_name
					value = t + "/" + t + ".html"
				elif tag == "pdf_link":
					t = self.docs[i].base_name
					value = t + "/" + t + ".pdf"
				elif tag == "pdf_size":
					value = self.docs[i].pdf_size
				line = line[:tmp.start ()] + value + line[tmp.end ():]
				tmp = p.search (line)
			f.write (line)
		f.close ()
		os.chmod (name, 0755)

# bos durani Allah sevmez, belge sayfasi hazirlayalim
index = Index ("belgeler.tmpl", "belge.tmpl")
index.make_docs ()
index.make_index ("belgeler.html")
print "DONE."
