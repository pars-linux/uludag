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

# sablonla.py
# html header/footer tool

import sys
import os
import os.path
import string
import getopt

class Sablon:
	def __init__(self,tmplfile):
		self.fake = 0
		self.c_start = "<!-- SAYFA İÇERİK BAŞI -->"
		self.c_end = "<!-- SAYFA İÇERİK SONU -->"
		t = self.get_content(tmplfile)
		if t == None:
			print "'%s' şablon dosyası problemli!" % (tmplfile)
			sys.exit(2)
		self.tmpl_head = t[0]
		self.tmpl_foot = t[2]
		self.tmpl_file = tmplfile
	
	def get_content(self,fname):
		f = file(fname, "r")
		lines = f.readlines()
		f.close()
		head = []
		content = []
		foot = []
		mode = 0
		for line in lines:
			if mode == 0:
				head.append(line)
				if line.find(self.c_start) != -1:
					mode = 1
			elif mode == 1:
				if line.find(self.c_end) != -1:
					foot.append(line)
					mode = 2
				else:
					content.append(line)
			elif mode == 2:
				foot.append(line)
		if mode != 2:
			return None
		return [ head, content, foot ]
	
	def fix_paths(self,fname,lines):
		n = string.count(fname, "/")
		rp = "../" * (n - 1)
		lines2 = []
		for line in lines:
			lines2.append(line.replace("$root$", rp))
		return lines2
	
	def modify_file(self,fname):
		# dont touch template file
		if fname == self.tmpl_file:
			return
		# html files only
		if fname.find(".") == -1:
			return
		if not fname[fname.rfind("."):] in [ ".html" ]:
			return
		fc = self.get_content(fname)
		if fc == None:
			print "'%s' içerik başlangıç/bitiş belirteçlerine sahip değil!" % (fname)
			return
		# modify file according to the new template
		print "'%s' değiştiriliyor..." % (fname)
		if self.fake == 1:
			return
		lines2 = self.fix_paths(fname, self.tmpl_head)
		lines2 += fc[1]
		lines2 += self.fix_paths(fname, self.tmpl_foot)
		f = file(fname, "w")
		f.writelines(lines2)
		f.close()
	
	def modify_dir(self,dirname):
		os.chdir(dirname)
		for root,dirs,files in os.walk("."):
			for file in files:
				self.modify_file(os.path.join(root,file))
			# dont visit subversion or language dirs
			if "eng" in dirs:
				dirs.remove("eng")
			if ".svn" in dirs:
				dirs.remove(".svn")

# usage

def usage():
	print "Kullanım: sablonla.py [dizin] [şablon]"
	sys.exit(2)

# main
try:
	opts, args = getopt.gnu_getopt(sys.argv[1:], "hf", ["help", "fake"])
except:
	usage()

tmpl = "./template.html"
dirname = "."
opt_fake = 0

for o, v in opts:
	if o in ("-h", "--help"):
		usage()
	if o in ("-f", "--fake"):
		opt_fake = 1

if len(args) > 0:
	dirname = args[0]
if len(args) > 1:
	tmpl = args[1]

s = Sablon(tmpl)
s.fake = opt_fake
s.modify_dir(dirname)
