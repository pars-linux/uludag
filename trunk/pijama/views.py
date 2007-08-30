from django.shortcuts import render_to_response

from pisi.specfile import SpecFile
import os
import pisi



def showmainpage(request, reponame):
	
	#print reponame
	
	title = _("General Knowledge")
	
	something=__import__("pijama.pijidb.models")
	# number of source packages
	t=something.pijidb.models.__getattribute__("RepoPackages")
	x=t.objects.filter(reponame__exact=reponame).values("pkgname")
	numofsrcs=len(x.distinct())
	
	# number of binary packages
	t=something.pijidb.models.__getattribute__("BinaryPacks")
	x=t.objects.filter(reponame__exact=reponame).values("name")
	numofbins=len(x.distinct())
	
	# num of patchs
	t=something.pijidb.models.__getattribute__("Patch")
	x=t.objects.filter(reponame__exact=reponame)
	numofpatchs=len(x)
	
	# num of packagers
	t=something.pijidb.models.__getattribute__("Packager")
	x=t.objects.filter(id__gt=0).values("name")
	numofpkgrs=len(x.distinct())
	
	# the longest action.py file
	t=something.pijidb.models.__getattribute__("RepoPackages")
	x=t.objects.filter(reponame__exact=reponame).order_by("-actionpylen")
	liactionpy=[]
	for i in xrange(5):
		liactionpy.append((x[i].pkgname, x[i].actionpylen))
		
	# packages that have the maximum pathes
	t=something.pijidb.models.__getattribute__("RepoPackages")
	x=t.objects.filter(reponame__exact=reponame).order_by("-numofpatchs")
	lipatch=[]
	for i in xrange(5):
		lipatch.append((x[i].pkgname, x[i].numofpatchs))
		
	return render_to_response("index.html", {"title": title, "numofsrcs":numofsrcs, "numofbins":numofbins, "numofpatchs":numofpatchs, "numofpkgrs":numofpkgrs, "longestpatch":lipatch, "longestaction":liactionpy, "reponame":reponame})
	
def showsourcepkgs(request, reponame):
	
	title = _("Source Packages")
	
	#print "here"
	
	something=__import__("pijama.pijidb.models")
	t=something.pijidb.models.__getattribute__("RepoPackages")
	x=t.objects.filter(reponame__exact=reponame).order_by("pkgname")
	
	rsltli=[]
	for i in xrange(len(x)):
		pkgname=x[i].pkgname
		print pkgname
		packager=x[i].packager_set.values()
		
		
		spec=SpecFile()
		spec.read(os.path.join(x[i].path, "pspec.xml"))
		li=spec.history
		version=li[0].version
		summary=spec.source.summary
		
		if summary.has_key("en"): smry=summary["en"]
		if summary.has_key("tr"): smry=summary["tr"]
		
		rsltli.append((pkgname, version, packager[0], smry))
	
	return render_to_response("source.html", {"title": title, "srcli":rsltli, "reponame":reponame})
		
def showbinarypkgs(request, reponame):
	
	title = _("Binary Packages")
	
	#print "here"
	
	something=__import__("pijama.pijidb.models")
	t=something.pijidb.models.__getattribute__("BinaryPacks")
	x=t.objects.filter(reponame__exact=reponame).order_by("name")
	
	rsltli=[]
	for i in xrange(len(x)):
		pkgnamemain=x[i].name
		#print pkgnamemain
		pisi.api.init(write=False)
		
		try:
			pkg=pisi.context.packagedb.get_package(pkgnamemain)
			packager=pkg.source.packager.name
			version=pkg.version
			summary=pkg.summary
			pkgname=pkgnamemain
		except:
			#print "girdi"
			flag=False
			pkg=x[i].pkgname.pkgname
			#print type(pkgnamemain), type(pkg)
			if pkgnamemain == pkg:
				print "girdi"
				spec=SpecFile()
				spec.read(os.path.join(x[i].pkgname.path, "pspec.xml"))
				flag=True
				
			#print pkgname
			else: pkg=pisi.context.packagedb.get_package(pkg)
			#print "girdi", pkg
		
			if not flag:
				pkgname=pkg
				packager=pkg.source.packager.name
				version=pkg.version
				summary=pkg.summary
			else:
				li=spec.history
				version=li[0].version
				
				pkgname=spec.source.name
				summary=spec.source.summary
				packager=spec.source.packager.name
			
		
		if summary.has_key("en"): smry=summary["en"]
		if summary.has_key("tr"): smry=summary["tr"]
		
		rsltli.append((pkgname, version, packager, smry))
	
	return render_to_response("binary.html", {"title": title, "srcli":rsltli, "reponame":reponame})