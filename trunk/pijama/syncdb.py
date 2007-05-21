#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version. Please read the COPYING file.
#
# Oğuz Yarımtepe
# oguzy at comu.edu.tr

import os
import datetime

from pisi.specfile import SpecFile
import pisi

class WUpdate:
	
	def __init__(self):
			
		import sys
		os.chdir("..")
		path=os.getcwd()
		sys.path += [path]
		os.environ['DJANGO_SETTINGS_MODULE'] = 'pijama.settings'
		os.chdir("pijama")
		
		pisi.api.init(database=True, write=False)
		
		self.parduspath="/home/oguz/pardus"
		self.contribpath="/home/oguz/contrib"
		
		#self.repos= ["2007","devel"] do it later
		#self.repos=["2007"]
		self.pckgname, self.reponame="", ""
		
		self.spec = SpecFile()
	
	def makedate(self, s):
		li=s.split("-")
		return datetime.date(int(li[0]), int(li[1]), int(li[2]))
		
	
	def tableactions(self, pckgname, reponame, dirs, root):
		
		try:#try whether there exists a package at the repo, if so just edit the repo date edit info
			something=__import__("pijama.pijidb.models")
			#print reponame
			t=something.pijidb.models.__getattribute__("RepoPackages")
			t.objects.get(pkgname=pckgname, reponame=reponame)# if there is not an entry will throw exception
			
			history=self.spec.history
			t=something.pijidb.models.__getattribute__("DepoUpdate")
			y=t.objects.order_by("-editdate")
			#print y
			t1,t2=None,None
			if self.makedate(history[0].date) > y[0].editdate: t2=self.makedate(history[0].date)
			t(updatedate=t1, editdate=t2).save()
					
		except: # the package is not in the table, a new entry
				
			print "buraya girdi"	
			
			x=t(pkgname=pckgname, reponame=reponame, isa=self.spec.source.isA[0], partof=self.spec.source.partOf)
			x.save()
			
			print "RepoPackages done"
			
			p=t.objects.get(pkgname=pckgname, reponame=reponame)
			
			print p
			
			li=self.spec.source.buildDependencies
			for pkg in li:
				
				if len(li) == 0: break
				
				sign, version = None, None
				
				if pkg.version: 
					sign="="
					version=pkg.version
				elif pkg.versionFrom:
					sign=">"
					version=pkg.versionFrom
				elif pkg.versionTo:
					sign="<"
					version=pkg.versionTo
				else:
					sign=""
					
				p.builddeps_set.create(name=pkg.package, version=version, sign=sign)
				
				print ("Builddeps done")
				
			info=self.spec.source.packager
			p.packager_set.create(name=info.name, email=info.email)
			
			print "packager info done"
					
			patches=self.spec.source.patches		
			for patch in patches:
				
				if len(patches)==0: break
				
				p.patch_set.create(name=patch.filename, compressiontype=patch.compressionType, level=patch.level)
				
			print "patches done"
				
			binaries=self.spec.packages
			for binary in binaries:
				p.binarypacks_set.create(name=binary.name)
				
			print "binaries done"
			for pkgknowledge in binaries:			
				for conflict in pkgknowledge.conflicts:
				
					if len(binaries)==0: break
				
					sign, version = None, None
				
					if conflict.version: 
						sign="="
						version=conflict.version
					elif conflict.versionFrom:
						sign=">"
						version=conflict.versionFrom
					elif conflict.versionTo:
						sign="<"
						version=conflict.versionTo
					else:
						sign=""
					
					p.conflicts_set.create(name=conflict.package, version=version, sign=sign)
				
				runtimedeps=pkgknowledge.runtimeDependencies()
				for dep in runtimedeps:
				
					if len(runtimedeps)==0: break
				
					sign, version = None, None
				
					if dep.version: 
						sign="="
						version=dep.version
					elif dep.versionFrom:
						sign=">"
						version=dep.versionFrom
					elif dep.versionTo:
						sign="<"
						version=dep.versionTo
					else:
						sign=""
					
					p.runtimedeps_set.create(name=dep.package, version=version, sign=sign)
				
			print "runtimedeps conflicts done"
				
			history=self.spec.history
			print history[-1].type, history[0].type
			if history[-1].type == None: t1="normal" 
			else: t1=history[-1].type
			if history[0].type == None: t2="normal" 
			else: t2=history[0].type
			p.history_set.create(updatetype=t1, date=self.makedate(history[-1].date))#first relase date
			p.history_set.create(updatetype=t2, date=self.makedate(history[0].date))#last edit date
				
			if "screenshots" in dirs:
				for filename in os.listdir("screenshots"):
					p.screenshot_set.create(filename=filename)
					
			print "screetshots done"		
					
			t=something.pijidb.models.__getattribute__("DepoUpdate")
			x=t.objects.order_by("-updatedate")
			y=t.objects.order_by("-editdate")
			t1,t2=None,None
			if len(x)==0 or self.makedate(history[-1].date) > x[0].updatedate : t1=self.makedate(history[-1].date)
			if len(y)==0 or self.makedate(history[0].date) > y[0].editdate: t2=self.makedate(history[0].date)
			t(updatedate=t1, editdate=t2).save()
		
	def walkthrough(self, path):
		
		for root, dirs, files in os.walk(path):
			
			if root.startswith(os.path.join(self.parduspath, "2007")):
				self.reponame="2007"
				 
			elif root.startswith(os.path.join(self.parduspath, "devel")):
				self.reponame="devel"
				
			elif root.startswith((self.contribpath)):
				self.reponame="contrib"
				
			else: 
				#print root
				continue
			
			if ".svn" in dirs:
            			dirs.remove(".svn")
			#print "root", root, "dirs", dirs		
			
			print root
			
			if "pspec.xml" in files:
				
				index=files.index("pspec.xml")
				self.spec.read(os.path.join(root,files[index]))
				self.pkgname=self.spec.source.name
				print self.pkgname
				self.tableactions(self.pkgname, self.reponame, dirs, root)
				
if __name__ == "__main__":
	
	c=WUpdate()
	c.walkthrough(c.parduspath)
	c.walkthrough(c.contribpath)
				
 
 
