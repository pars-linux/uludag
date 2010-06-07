# Create your views here.
# -*- coding: utf-8 -*-


from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
from webapp.models import *
from webapp.myforms import *
from django.conf import settings
from django.http import Http404
import pisi

def index(request):
    num_of_sources=len(SourcePktTbl.objects.all())
    num_of_bins=len(BinaryPktTbl.objects.all().distinct())
    num_of_patches=len(PatchPktTbl.objects.values('patchname'))
    num_of_packagers=len(PackagerTbl.objects.values('name').distinct())
    infoli=[]
    d=dict()
    

    keys=("Kaynak paket sayısı", "İkili paket sayısı", "Yama sayısı", "Paketçi sayısı" )
    values=(num_of_sources,num_of_bins,num_of_patches,num_of_packagers)
    
    
    for x in xrange(len(keys)):
        d["explanation"]=keys[x]
        d["detail"]=values[x]
        infoli.append(d)
        d=dict()

    # most patched ones
    limit=5
    count=0
    query_set = PatchPktTbl.objects.extra(select={'count': 'count(patchname)'}, order_by=['-count']).values('count', 'pktname')
    query_set.query.group_by = ['pktname']

    mostpatched=dict()
    mptchli=[]
    for x in query_set:
        if count < limit:
            mostpatched["pktname"]=x["pktname"]
            mostpatched["patchcount"]=x["count"]
            mptchli.append(mostpatched)
            mostpatched=dict()
        else:
            break
        count+=1

    count=0
    lastadded=dict()
    lastli=[]
    last_added=SourcePktTbl.objects.all().order_by("-added_date")
    for x in last_added:
        if count < limit:
            lastadded["pktname"]=x.pktname
            lastadded["added_date"]=x.added_date
            lastli.append(lastadded)
            lastadded=dict()
        else:
            break
        count+=1

    rtrli={"general_information":infoli, "most_patched":mptchli, "last_added":lastli, "base_url":settings.BASE_URL}
    return render_to_response("index.html", rtrli)

def sources(request):
   sourcesli= SourcePktTbl.objects.all()
   
   return render_to_response("source.html",{"sources":sourcesli, "base_url":settings.BASE_URL})

def binaries(request):
    binli=BinaryPktTbl.objects.all()
    return render_to_response("binary.html",{"binaries":binli, "base_url":settings.BASE_URL})

def packagers(request):
    query_set = PackagerTbl.objects.extra(select={'count': 'count(pktname)'}, order_by=['-count']).values('count', 'name')
    query_set.query.group_by = ['name']
    return render_to_response("packager.html", {"packagerli":query_set, "base_url":settings.BASE_URL})


def sourcedetails(request, packagename=None):

    pkg=SourcePktTbl.objects.get(pktname=packagename)
    packager=pkg.packagertbl.name
    histories=pkg.historypkttbl_set.all()
    binaries=pkg.binarypkttbl_set.all()

    return render_to_response("sourcedetails.html", {"pkg":pkg, "packager":packager, "histories":histories, "binaries":binaries, "base_url":settings.BASE_URL})


def binarydetails(request, packagename=None):
    binary_pkg=BinaryPktTbl.objects.get(binarypkt_name=packagename)
    pkg = SourcePktTbl.objects.get(pktname = binary_pkg.sourcepkt_name)
    builddeps=pkg.sourcepktbuilddebstbl_set.all()
    p=pisi.db.packagedb.PackageDB()
    package=p.get_package(packagename)
    version=package.name + " " + package.version
    installedsize=package.installedSize
    packagesize=package.packageSize
    runtimedeps=package.runtimeDependencies()
    revdeps=p.get_rev_deps(packagename)
    tmp=map(lambda x: x[0], revdeps)
    tmp.sort()
    revdeps=tmp
    sourcename=package.source.name

    li=SourcePktBuildDebsTbl.objects.filter(pktname=packagename)
    
    rslt=set([])
    for p in li:
        s=SourcePktTbl.objects.get(pktname=p.sourcepkt_name)
        r=map(lambda x: x.binarypkt_name, s.binarypkttbl_set.all())
        rslt=rslt.union(set(r))

    result=map(lambda x: x, rslt)
    result.sort()

    return render_to_response("binarydetails.html",{"name":packagename, "pkg":version, "sourcename":sourcename, "version":version, "builddeps":builddeps, "runtimedeps":runtimedeps, "revdeps":revdeps, "installedsize":installedsize, "packagesize":packagesize, "reqfortobebuild":result, "base_url":settings.BASE_URL})

def packagersdetails(request, packagername=None):

   packagerli=PackagerTbl.objects.filter(name=packagername)
   email=packagerli[0].email
   #email="aa"

   return render_to_response("packagerdetails.html",{"name":packagername, "email":email, "packagerli": packagerli, "base_url":settings.BASE_URL})

def search(request):
    
    form = KeyWordForm()

    return render_to_response("search.html", {"form":form, "base_url":settings.BASE_URL})

def searchresult(request):

    form = KeyWordForm(request.POST)

    if form.is_valid():

        keyword=request.POST["keyword"]
        binresult=set([])
        sourceresult=set([])
        patchresult=set([])
        fileresult=[]
        if request.POST.has_key("searchinbinpackages"): 
            searchinbinpackages = request.POST["searchinbinpackages"]
            li1=BinaryPktTbl.objects.filter(summary__icontains=keyword)
            li2=BinaryPktTbl.objects.filter(binarypkt_name__icontains=keyword)
            l=map(lambda x: x.binarypkt_name, li1)
            ll=map(lambda x: x.binarypkt_name, li1)
            binresult=set(l).union(set(ll))

        if request.POST.has_key("searchinsourcepackages"): 
            searchinsourcepackages = request.POST["searchinsourcepackages"]
            li1=SourcePktTbl.objects.filter(summary__icontains=keyword)
            li2=SourcePktTbl.objects.filter(pktname__icontains=keyword)
            l=map(lambda x: x.pktname, li1)
            ll=map(lambda x: x.pktname, li2)
            sourceresult=set(l).union(set(ll))

        if request.POST.has_key("searchinpatches"): 
            searchinpatches = request.POST["searchinpatches"]
            li1=PatchPktTbl.objects.filter(patchname__icontains=keyword)
            l=map(lambda x: x.pktname, li1)
            patchresult=set(l)

        if request.POST.has_key("searchinfiles"): 
            filename = request.POST["searchinfiles"]
            f=pisi.db.filesdb.FilesDB()
            fileresult=f.search_file(keyword)

        return render_to_response("searchresult.html", {"binresult":binresult,"sourceresult":sourceresult, "patchresult":patchresult, "fileresult":fileresult, "base_url":settings.BASE_URL})

    form = KeyWordForm(request.POST)
    return render_to_response("search.html", {"form":form, "base_url":settings.BASE_URL})


